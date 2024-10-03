import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    data = pd.read_csv('https://drive.usercontent.google.com/u/0/uc?id=1D8i0FEUtSBaPvqfd9A77BsG8VxZZXE_7&export=download')
    return data

day = load_data()

st.title("Proyek Analisis Data : Bike Sharing")
st.markdown("""
- **Nama:** Raihan Akmal Darmawan
- **Email:** m312b4ky3644@bangkit.academy
- **ID Dicoding:** raihan_akmal_d
""")
st.header("Pertanyaan Bisnis")
st.markdown("""
- Pertanyaan 1 : Pada musim apa penyewaan sepeda paling ramai?
- Pertanyaan 2 : Berapa total penyewaan sepeda pada bulan Maret 2012?
""")

st.subheader("")
st.subheader("Dataset yang digunakan:")
st.write(day.head(15))
st.write("**Atribut Dataset**")

attributes = """
- **instant**: index
- **dteday** : tanggal penyewaan sepeda
- **season** : musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Salju)
- **yr** : tahun (0: 2011, 1: 2012)
- **mnth** : bulan (1 hingga 12)
- **hr** : jam (0 hingga 23)
- **holiday** : hari libur
- **weekday** : hari dalam seminggu
- **workingday** : hari kerja (jika hari kerja nilainya 1, jika libur nilainya 0)
- **weathersit** :
  - 1: Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian
  - 2: Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
  - 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar
  - 4: Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut
- **temp**: Suhu dalam Celcius
- **atemp**: Suhu yang dirasakan dalam Celsius.
- **hum**: Kelembaban yang dinormalkan. Nilainya dibagi menjadi 100 (maks)
- **windspeed**: Kecepatan angin yang dinormalkan. Nilainya dibagi menjadi 67 (maks)
- **casual**: jumlah peminjam sepeda biasa, yang tidak berlangganan
- **registered**: jumlah peminjam sepeda yang terdaftar keanggotaan
- **cnt**: total jumlah peminjam sepeda (total peminjam sepeda baik itu casual ataupun registered)
"""

st.write(attributes)

def remove_outliers(df):
    df_numeric = df.select_dtypes(include=['number'])
    
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    mask = (df_numeric >= lower_bound) & (df_numeric <= upper_bound)
    df_filtered = df_numeric[mask.all(axis=1)]
    
    return df[df.index.isin(df_filtered.index)]
day_cleaned = remove_outliers(day)
day['dteday'] = pd.to_datetime(day['dteday'])

st.subheader("Perbandingan Tren Penyewaan Sepeda Tahun 2011 & 2012")

def display_yearly_rental_trend(day):
    yearly_rental_trend = day.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=yearly_rental_trend, hue_order=[0, 1])
    plt.title('Tren Penyewaan Sepeda per Bulan (2011 & 2012)')
    plt.xlabel('Bulan')
    plt.ylabel('Total Penyewaan Sepeda')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Tahun', labels=['2011', '2012'])
    st.pyplot(plt)
    
display_yearly_rental_trend(day)
st.write("Dari grafik diatas, kita bisa melihat pada tahun 2011 dari rentang bulan Januari hingga ke Mei jumlah penyewaan sepeda mengalami peningkatan pesat, namun pada rentang bulan Oktober hingga akhir tahun mengalami penurunan.  ")


day_2012 = day[day['yr'] == 1]

st.subheader("Tren Penyewaan Sepeda per Bulan pada Tahun 2012")
monthly_rental_2012 = day_2012.groupby('mnth')['cnt'].sum()

fig2, ax2 = plt.subplots()
plt.plot(monthly_rental_2012.index, monthly_rental_2012.values, marker='o')
plt.title('Total Penyewaan Sepeda per Bulan pada Tahun 2012')
plt.xlabel('Bulan')
plt.ylabel('Total Penyewaan')
plt.xticks(monthly_rental_2012.index, ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True)
st.pyplot(fig2)

st.write("Jika kita lihat lebih lanjut pada tahun 2012, peningkatan yang signifikan terjadi pada bulan Februari-Maret, dan puncak nya berada pada bulan September. Namun menjelang bulan Oktober, terjadi penurunan tajam hingga menjelang akhir tahun.")

total_rental_march_2012 = day_2012[day_2012['mnth'] == 3]['cnt'].sum()
st.write(f"Total penyewaan sepeda pada bulan Maret 2012: {total_rental_march_2012}")

st.subheader("Total Penyewaan Sepeda Berdasarkan Musim")
season_counts = day.groupby('season')['cnt'].sum().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(x='season', y='cnt', data=season_counts, ax=ax1)
ax1.set_title('Total Penyewaan Sepeda Berdasarkan Musim')
ax1.set_xlabel('Musim')
ax1.set_ylabel('Total Penyewaan')
ax1.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=45)
st.pyplot(fig1)

st.write ("Jika kita kelompokkan jumlah peminjaman sepeda berdasarkan musimnya, dapat dilihat bahwa musim gugur (Fall) menjadi musim dengan jumlah peminjaman sepeda tertinggi dibandingkan musim lainnya.")

ramai_index = season_counts['season'][season_counts['cnt'].idxmax()]
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
ramai = season_mapping[ramai_index]

st.write(f"Musim dengan pinjaman sepeda paling ramai: {ramai}")

st.header("Kesimpulan")
st.write("- Pertanyaan 1 : Musim dengan penyewaan sepeda paling ramai adalah musim gugur (Fall)")
st.write(f"- Pertanyaan 2 : Total penyewaan sepeda pada bulan Maret 2012: {total_rental_march_2012}")

