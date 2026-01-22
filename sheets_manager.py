import os, gspread
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

class SheetsManager:
    def __init__(self):
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file("creds.json", scopes=scope)
        self.sheet = gspread.authorize(creds).open_by_key(os.getenv("SPREADSHEET_ID")).sheet1
        
        # Inisialisasi Header Otomatis jika sheet kosong
        try:
            if not self.sheet.get_all_values():
                self.sheet.append_row(["Timestamp", "Tanggal Tugas", "Nama Tugas", "Status", "Category"])
        except: pass

    def save_tasks(self, tasks: list):
        """Menyimpan banyak tugas sekaligus ke Sheets."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [[now, t.get('date'), t.get('task'), "Pending", t.get('category', 'Umum')] 
                for t in tasks if isinstance(t, dict)]
        return self.sheet.append_rows(data, value_input_option='USER_ENTERED') if data else False

    def get_tasks(self, days=30):
        """Mengambil daftar tugas aktif (Status != Done)."""
        tasks = []
        try:
            all_v = self.sheet.get_all_values()
            if len(all_v) <= 1: return []
            
            limit = (datetime.now() + timedelta(days=days)).date()
            
            for r in all_v[1:]:
                # Pastikan baris memiliki kolom yang cukup
                if len(r) < 4: continue
                
                try:
                    # Validasi format tanggal YYYY-MM-DD
                    task_date = datetime.strptime(r[1], "%Y-%m-%d").date()
                    if task_date <= limit and r[3] != "Done":
                        tasks.append({"Nama Tugas": r[2], "Tanggal Tugas": r[1]})
                except (ValueError, TypeError):
                    continue # Lewati baris yang format tanggalnya salah
                    
            return tasks
        except Exception as e:
            print(f"Error Sheets: {e}")
            return []

    def mark_done_bulk(self, task_names: list):
        """Menghapus/Menandai banyak tugas selesai sekaligus."""
        try:
            for name in task_names:
                cell = self.sheet.find(name)
                if cell:
                    self.sheet.update_cell(cell.row, 4, "Done")
            return True
        except: return False