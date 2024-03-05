import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

st.title('BIKE SHARING DATASET')
main_df = pd.read_csv("main_data.csv")
hour_df = pd.read_csv("hour_csv")

# Mengubah label kategori
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
weathersit_labels = {1: 'Clear', 2: 'Mist', 3: 'Light_rain', 4: 'Heavy_rain'}
weekday_labels = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

# Assuming you have 'hour' and 'day' columns
main_df['season_hour'] = main_df['season_hour'].map(season_labels)
main_df['mnth_hour'] = main_df['mnth_hour'].map(month_labels)
main_df['weathersit_hour'] = main_df['weathersit_hour'].map(weathersit_labels)
main_df['weekday_hour'] = main_df['weekday_hour'].map(weekday_labels)

main_df['season_day'] = main_df['season_day'].map(season_labels)
main_df['mnth_day'] = main_df['mnth_day'].map(month_labels)
main_df['weathersit_day'] = main_df['weathersit_day'].map(weathersit_labels)
main_df['weekday_day'] = main_df['weekday_day'].map(weekday_labels)

# Fungsi untuk visualisasi Pertanyaan 1
def pertanyaan_1(main_df):
    st.header("Perbandingan Tren Peminjaman Sepeda pada Hari Libur dan Hari Kerja dalam Satu Hari Berdasarkan Jam")
    filtered_holiday_df = main_df[(main_df['workingday_hour'] == 0) & (main_df['holiday_hour'] == 1)]
    filtered_workingday_df = main_df[(main_df['workingday_hour'] == 1) & (main_df['holiday_hour'] == 0)]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='cnt_hour', data=filtered_holiday_df, color='blue', label='Holiday 1, Workingday 0', ax=ax)
    sns.barplot(x='hr', y='cnt_hour', data=filtered_workingday_df, color='orange', label='Holiday 0, Workingday 1', ax=ax)

    ax.set_title('Hourly Count Comparison: Holiday 1 vs Workingday 0')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Count')
    ax.legend()
    st.pyplot(fig)
    st.header("Conclusion:")
    st.markdown("""Berdasarkan barplot, dapat terlihat perbedaan tren penyewaan sepeda
                yang terjadi di hari libur dan hari kerja. Peminjaman sepeda
                cenderung lebih banyak pada hari kerja dibandingkan di hari 
                libur. Kemudian untuk jam peminjaman sepeda pun lebih banyak di 
                jam-jam kerja seperti jam 8 dan jam pulang kerja seperti jam 5 sore hingga
                6 sore. Sementara di hari libur, peminjaman sepeda cenderung lebih banyak
                pada jam 9, 10, 11, 12, 1 siang, hingga 3 sore.""")

# Fungsi untuk visualisasi Pertanyaan 2 - Boxplot per hari
def pertanyaan_2_boxplot(main_df):
    st.header("Distribusi Penggunaan Sepeda per Hari")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='weekday_day', y='cnt_day', data=main_df, ax=ax)
    plt.title('Distribusi penggunaan sepeda per hari')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

# Fungsi untuk visualisasi Pertanyaan 2 - Barplot per jam
def pertanyaan_2_barplot(main_df):
    st.header("Distribusi Penggunaan Sepeda per Jam dalam Satu Hari")
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='cnt_hour', data=main_df, ci=None, color='skyblue', ax=ax)
    plt.title('Distribusi Penggunaan Sepeda per Jam (Barplot)')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

# Fungsi untuk visualisasi Pertanyaan 3
def pertanyaan_3_tren_sepeda(hour_df):
    st.header("Tren Peminjaman Sepeda Setiap Bulan Berdasarkan Cuaca")
    sns.set(style="whitegrid")

    # Create a line chart for bike rental counts trend by month and weathersit
    plt.figure(figsize=(14, 8))
    monthly_weathersit_counts = hour_df.groupby(['mnth', 'weathersit'])['cnt'].sum().reset_index()

    # Change the order of months to January-December
    monthly_weathersit_counts['mnth'] = pd.Categorical(monthly_weathersit_counts['mnth'], categories=range(1, 13), ordered=True)

    # Create line chart for each weathersit
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=monthly_weathersit_counts, palette='viridis', marker='o')

    for weathersit, color in zip(monthly_weathersit_counts['weathersit'].unique(), sns.color_palette('viridis', n_colors=len(monthly_weathersit_counts['weathersit'].unique()))):
        subset = monthly_weathersit_counts[monthly_weathersit_counts['weathersit'] == weathersit]
        for i, point in subset.iterrows():
            plt.annotate(f'{int(point["cnt"])}', (point['mnth'], point['cnt']), color=color, fontsize=9, ha='center', va='bottom')

    # Add title and axis labels
    plt.title('Bike Rental Counts Trend by Month and Weathersit')
    plt.xlabel('Month')
    plt.ylabel('Count')

    # Display the plot using st.pyplot()
    st.pyplot(plt)
    st.header("Conclusion:")
    st.markdown("""Berdasarkan gambar grafik, dapat dilihat peminjaman 
                sepeda mengalami kenaikan dan penurunan tergantung dari 
                cuaca. Berdasarkan grafik dapat diketahui peminjaman sepeda
                paling banyak terjadi ketika cuaca dalam kondisi yang cerah.
                Disusul oleh hujan ringa, berkabut, dan hujan deras yang memiliki
                jumlah peminjam sepeda yang paling sedikit. Dapat dilihat juga
                Pengguna sepeda terbanyak terjadi ketika cuaca cerah di bulan Mei dan Juni""")

def pertanyaan_4_barplot(main_df):
    st.header("Rata-Rata Suhu Setiap Bulan")

    # Mengelompokkan data berdasarkan 'mnth' dan 'weathersit', kemudian menghitung jumlah penyewaan ('cnt') untuk setiap kelompok
    monthly_avg_feel_temp = main_df.groupby('mnth_hour')['atemp_hour'].mean().reset_index()

    # Mengubah urutan bulan menjadi Januari-Desember
    monthly_avg_feel_temp['mnth_hour'] = pd.Categorical(monthly_avg_feel_temp['mnth_hour'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

    # Membuat bar plot untuk feeling temperature per bulan
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x='mnth_hour', y='atemp_hour', data=monthly_avg_feel_temp, color='skyblue')

    # Handling NaN values in the pointplot
    sns.pointplot(x='mnth_hour', y='atemp_hour', data=monthly_avg_feel_temp, color='black', scale=0.5, markers='o', dodge=True)

    plt.title('Average Feeling Temperature Trend by Month')
    plt.xlabel('Month')
    plt.ylabel('Average Feeling Temperature')

    st.pyplot(fig)

def pertanyaan_4_boxplot(main_df):
    st.header("Distribusi Pengguna Sepeda berdasarkan Temperatur dalam Satu Tahun")

    # Membuat box plot untuk feeling temperature per bulan
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.boxplot(x='mnth_hour', y='cnt_hour', data=main_df, palette='viridis')

    # Mengelompokkan data berdasarkan 'mnth' dan 'weathersit', kemudian menghitung jumlah penyewaan ('cnt') untuk setiap kelompok
    monthly_avg_feel_temp = main_df.groupby('mnth_hour')['atemp_hour'].mean().reset_index()
    
    sns.pointplot(x='mnth_hour', y='atemp_hour', data=monthly_avg_feel_temp, color='black', scale=0.5)

    # Menambahkan title dan x,y label
    plt.title('Bike Usage Distribution by Feeling Temperature and Month')
    plt.xlabel('Month')
    plt.ylabel('Bike Usage Count (cnt)')

    # Menampilkan Plot
    st.pyplot(fig)

st.sidebar.title("Muhammad Sultan Nurrochman")

# Sidebar untuk memilih opsi visualisasi
selected_option = st.sidebar.selectbox("Pilih Opsi", ["Perbandingan Tren Peminjaman Sepeda pada Hari Libur dan Hari Kerja dalam Satu Hari Berdasarkan Jam","Distribusi Peminjaman Sepeda per Hari dan per Jam","Tren Peminjaman Sepeda Setiap Bulan Berdasarkan Cuaca","Distribusi Pengguna Sepeda berdasarkan Temperatur dalam Satu Tahun"])

# Tampilkan visualisasi sesuai opsi yang dipilih
if selected_option == "Perbandingan Tren Peminjaman Sepeda pada Hari Libur dan Hari Kerja dalam Satu Hari Berdasarkan Jam":
    pertanyaan_1(main_df)
elif selected_option == "Distribusi Peminjaman Sepeda per Hari dan per Jam":
    pertanyaan_2_boxplot(main_df)
    pertanyaan_2_barplot(main_df)
    st.header("Conclusion:")
    st.markdown("""Berdasarkan kedua plot tersebut, dapat terlihat banyaknya dan tren peminjaman 
                sepeda yang terjadi dalam satu minggu dan dapat terlihat
                kira-kira peminjaman sepeda per jam dalam satu hari. Dapat terlihat
                peminjaman sepeda terbanyak yaitu ada pada hari Sabtu, Minggu, dan Rabu 
                dengan kira-kira rentang peminjam sepeda dalam satu hari sebanyak 4000 hingga
                8000 peminjam. Untuk peminjam sepeda per jamnya, paling banyak sepeda dipinjam
                pada jam 8, 5 sore, dan 6 sore. Dengan peminjam sebanyak 300 hingga 400 
                lebih peminjam.""")
elif selected_option == "Tren Peminjaman Sepeda Setiap Bulan Berdasarkan Cuaca":
    pertanyaan_3_tren_sepeda(hour_df)
elif selected_option == "Distribusi Pengguna Sepeda berdasarkan Temperatur dalam Satu Tahun":
    pertanyaan_4_barplot(main_df)
    pertanyaan_4_boxplot(main_df)
    st.header("Conclusion:")
    st.markdown("""Setiap batang pada bar plot menunjukkan rata-rata 
                feeling temperature per bulan. Pada contoh ini, 
                sumbu y menunjukkan nilai rata-rata feeling 
                temperature. Grafik menunjukkan adanyan tren kenaikan dan 
                penurunan yang terjadi pada peminjaman/penyewaan sepeda 
                dalam satu tahun berdasarkan suhu yang dirasakan oleh 
                pengguna. Dapat terlihat jumlah peminjam mengalami kenaikan 
                pada bulan Januari hingga Juli karena berbanding lurus dengan 
                kenaikan suhu. Kemudian jumlah peminjam sepeda mengalami penurunan 
                pada bulan Juli hingga Januari, karena suhu juga mengalami penurunan. 
                Namun dapat dilihat pada bulan Mei hingga Oktober pengguna sepeda 
                terlihat konsisten yang menandakan terdapat kemungkinan suhu yang
                masih bisa ditoleransi oleh pesepeda""")
