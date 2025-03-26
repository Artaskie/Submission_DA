import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")

# Konversi kolom tanggal ke format datetime **(DILAKUKAN SEKALI SAJA)**
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

# Mapping untuk season dan cuaca
season_mapping = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}

df_day["season_label"] = df_day["season"].map(season_mapping)
df_day["weather_label"] = df_day["weathersit"].map(weather_mapping)

# Sidebar - Fitur Interaktif
st.sidebar.header("📅 Filter Data Berdasarkan Tanggal")
start_date = pd.to_datetime(st.sidebar.date_input("Mulai Tanggal", df_day["dteday"].min()))
end_date = pd.to_datetime(st.sidebar.date_input("Sampai Tanggal", df_day["dteday"].max()))

# Filter interaktif tambahan berdasarkan musim dan cuaca
selected_season = st.sidebar.multiselect("Pilih Musim", df_day["season_label"].unique(), df_day["season_label"].unique())
selected_weather = st.sidebar.multiselect("Pilih Cuaca", df_day["weather_label"].unique(), df_day["weather_label"].unique())

# Validasi rentang tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

# Filter dataset
filtered_df = df_day[(df_day["dteday"] >= start_date) & (df_day["dteday"] <= end_date) &
                      (df_day["season_label"].isin(selected_season)) &
                      (df_day["weather_label"].isin(selected_weather))]

# Menampilkan Data Terfilter
st.subheader("📊 Data Penyewaan Sepeda Terfilter")
st.write(f"Menampilkan data dari **{start_date}** hingga **{end_date}** dengan musim {', '.join(selected_season)} dan cuaca {', '.join(selected_weather)}.")
st.dataframe(filtered_df[["dteday", "season_label", "weather_label", "cnt"]])

# 1. Pola Penyewaan Sepeda Sepanjang Hari
st.subheader("⏳ Pola Penyewaan Sepeda Sepanjang Hari")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=df_hour["hr"], y=df_hour["cnt"], marker="o", color="b", ax=ax)
ax.set_title("Pola Jumlah Penyewaan Sepeda Sepanjang Hari")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.grid(True)
st.pyplot(fig)

# 2. Distribusi Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan
st.subheader("📅 Distribusi Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
df_day["day_type"] = df_day["weekday"].apply(lambda x: "Weekday" if x < 5 else "Weekend")
day_type_counts = df_day["day_type"].value_counts()

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(day_type_counts, labels=day_type_counts.index, autopct="%1.1f%%", colors=["lightcoral", "lightskyblue"])
ax.set_title("Distribusi Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
st.pyplot(fig)

# 3. Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
st.subheader("📆 Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
day_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
               4: "Thursday", 5: "Friday", 6: "Saturday"}
df_day["weekday_label"] = df_day["weekday"].map(day_mapping)

weekly_trend = df_day.groupby("weekday_label")["cnt"].mean().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=weekly_trend.index, y=weekly_trend.values, palette="coolwarm", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# 4. Rata-rata Penyewaan Sepeda Berdasarkan Suhu
st.subheader("🌡️ Rata-rata Penyewaan Sepeda Berdasarkan Suhu")
df_day["temp_bin"] = pd.cut(df_day["temp"], bins=5, labels=["Sangat Dingin", "Dingin", "Sedang", "Hangat", "Panas"])
temp_trend = df_day.groupby("temp_bin")["cnt"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=temp_trend.index, y=temp_trend.values, palette="Blues", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Suhu")
ax.set_xlabel("Kategori Suhu")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
st.pyplot(fig)

st.caption("🚴‍♂️ Dashboard ini dibuat menggunakan Streamlit")
