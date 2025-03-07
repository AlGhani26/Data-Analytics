import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Load data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Sidebar
with st.sidebar:
    st.title("Muhamad Naufal Al Ghani")
    st.image("dashboard/logo.png")

    # Fitur iteratif: Pilih Tahun
    year_option = st.radio("Pilih Tahun", ["2011", "2012", "Semua"], index=2)

# Konversi tahun
year_map = {"2011": 0, "2012": 1}
if year_option != "Semua":
    day_df = day_df[day_df["yr"] == year_map[year_option]]
    hour_df = hour_df[hour_df["yr"] == year_map[year_option]]

# Main
st.title("Dashboard Penyewaan Sepeda 🚲")

# --- 1. Tren Penyewaan Sepeda per Bulan ---
st.subheader("📈 Tren Penyewaan Sepeda per Bulan")
monthly_rentals = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
monthly_rentals['year'] = monthly_rentals['yr'].map({0: 2011, 1: 2012})
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='mnth', y='cnt', hue='year', data=monthly_rentals, marker='o', palette='tab10', ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penyewaan')
ax.set_title(f'Tren Penyewaan Sepeda Per Bulan ({year_option})')
st.pyplot(fig)

# --- 2. Total Penyewaan Sepeda per Jam ---
st.subheader("⏰ Total Penyewaan Sepeda per Jam")
hourly_rentals = hour_df.groupby('hr')['cnt'].sum().reset_index()
colors = ['orange'] * len(hourly_rentals)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', data=hourly_rentals, ax=ax, palette=colors)
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Total Penyewaan')
ax.set_title(f'Total Penyewaan Sepeda untuk Setiap Jam dalam Sehari ({year_option})')
st.pyplot(fig)

# --- 3. Penyewaan Sepeda Berdasarkan Musim ---
st.subheader("🍂 Penyewaan Sepeda Berdasarkan Musim")
season_rentals = day_df.groupby('season')['cnt'].sum().reset_index()
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_rentals['season'] = season_rentals['season'].map(season_labels)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='cnt', data=season_rentals, ax=ax, palette='coolwarm')
ax.set_xlabel('Musim')
ax.set_ylabel('Total Penyewaan')
ax.set_title(f'Total Penyewaan Sepeda Berdasarkan Musim ({year_option})')
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)

# --- 4. Perbandingan Penyewaan Sepeda pada Holiday, Workday, dan Weekend ---
st.subheader("🏖️ Perbandingan Penyewaan Sepeda")
day_df['day_type'] = day_df.apply(lambda row: 'Holiday' if row['holiday'] == 1 else ('Workday' if row['workingday'] == 1 else 'Weekend'), axis=1)
day_type_rentals = day_df.groupby('day_type')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='day_type', y='cnt', data=day_type_rentals, ax=ax, palette='viridis')
ax.set_xlabel('Tipe Hari')
ax.set_ylabel('Total Penyewaan')
ax.set_title(f'Perbandingan Penyewaan Sepeda pada Holiday, Workday, dan Weekend ({year_option})')
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)

st.write("Copyright © Naufal Al Ghani 2025")
