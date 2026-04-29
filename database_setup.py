import sqlite3
import pandas as pd
import yfinance as yf

# 1. Koneksi ke Database SQLite lokal
conn = sqlite3.connect('data/historical_tick_data.db')
cursor = conn.cursor()

# 2. Membuat tabel penyimpanan data saham
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_volume (
        date TEXT,
        ticker TEXT,
        close_price REAL,
        volume INTEGER,
        whale_power_index REAL
    )
''')

# 3. Dummy Data Ingestion (Mengambil data simulasi BBCA)
data = yf.download('BBCA.JK', period='1mo')
data['whale_power_index'] = 65.5 # Nilai simulasi awal
data = data.reset_index()

# 4. Memasukkan data ke database
data[['Date', 'Close', 'Volume', 'whale_power_index']].to_sql('stock_volume', conn, if_exists='replace', index=False)
print("Database Setup & Data Ingestion BERHASIL!")
conn.close()
