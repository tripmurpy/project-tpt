#main.py adalah file utama yang akan dijalankan untuk menjalankan semua komponen ASKY
import os
from dotenv import load_dotenv #baca file .env (tempat nyimpen password).
from sheets_manager import SheetsManager #ruang penyimpanan data via google sheets
from ai_agent import AIAgent #ai yang dapat mengenali tugas dan menambahkan ke google sheets
from telegram import ASKYBot #interface bot telegram

load_dotenv() #memuat  environment dari file .env

# bagian 2 , eksekusi project bot (maib.py)
if __name__ == "__main__":
    # Inisialisasi komponen inti dengan efisiensi tinggi
    sm, ai = SheetsManager(), AIAgent()
    app = ASKYBot(ai, sm)

    # Jalankan bot utama   
    try:
        app.run()
    except Exception as e:
        print(f"CRITICAL_STOP: {e}")