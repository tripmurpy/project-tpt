#telegram.py
import os, telebot # Baca settingan sistem (biar bisa ambil token rahasia)
from telebot import types # Alat buat bikin tombol-tombol di chat.
from telebot.apihelper import ApiTelegramException
from dotenv import load_dotenv #baca file .env (tempat nyimpen password).

#konfigurasi dan env (telegram.py)
load_dotenv()#memuat  environment dari file .env

class ASKYBot:
    def __init__(self, ai, sm):
        #inisialisasi api 
        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"), parse_mode='HTML')#html untuk format tebal/miring
        self.ai, self.sm = ai, sm #menyimpan refrensi modul lain,ai=ai agent,sm=sheetsmanager
        #state manager , 
        self.user_modes = {} # Untuk melacak apakah user sedang 'adding'
        self.temp_add = {}   # Simpan hasil parsing AI sementara
        self.temp_done = {}  # Simpan pilihan tugas yang akan diselesaikan


    #bagian 1 = interface (telegram)
    def show_selection_menu(self, chat_id, tasks, message_id=None):
        """Menu dengan centang ✅ dan proteksi Error 400."""
        selected = self.temp_done.get(chat_id, []) #ambil daftar tugas
        markup = types.InlineKeyboardMarkup() #untuk tombol

        #---tombol--
        for t in tasks:
            name = t['Nama Tugas']
            status = "✅ " if name in selected else "" 
            markup.add(types.InlineKeyboardButton(f"{status}{name}", callback_data=f"select_{name}"))
        
        markup.row(types.InlineKeyboardButton("🚀 Konfirmasi Selesai", callback_data="confirm_bulk"),
                   types.InlineKeyboardButton("❌ Batal", callback_data="cancel_done"))
        
        text = "<b>Pilih tugas yang selesai (Bisa pilih 2-3 sekaligus):</b>"

        #mekanisme update 
        try:
            if message_id:
                self.bot.edit_message_text(text, chat_id, message_id, reply_markup=markup)
            else:
                self.bot.send_message(chat_id, text, reply_markup=markup)
        except ApiTelegramException as e:
            if "message is not modified" not in e.description: print(f"ERR: {e}")

     #-- bagian 2  main fitur (telegram.py) 

    def run(self):
        #fitur start 
        @self.bot.message_handler(commands=['start'])
        def start(m):
            self.user_modes[m.chat.id] = None # Reset status user
            # Membuat Menu Keyboard Bawah
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("➕ Tambah Tugas")
            markup.row("📋 Cek Tugas", "✅ Selesaikan Tugas")
            self.bot.send_message(m.chat.id, "<b>Haloo ,ASKY siap mencatat tugasmu.</b>", reply_markup=markup)

        # ---  Perintah /stop ---
        @self.bot.message_handler(commands=['stop'])
        def stop(m):
            self.user_modes[m.chat.id] = None
            markup = types.ReplyKeyboardRemove()
            self.bot.send_message(m.chat.id, "<b>Bot Berhenti.</b> Sampai jumpa!", reply_markup=markup)

        # --- Menu Tambah Tugas ---
        @self.bot.message_handler(func=lambda m: m.text == "➕ Tambah Tugas")
        def ask_task(m):
            # Mengaktifkan mode interaktif
            self.user_modes[m.chat.id] = 'waiting_task'
            self.bot.send_message(m.chat.id, "<b>Tugas apa yang ingin Anda tambahkan hari ini?</b>\n(Bisa masukkan banyak tugas sekaligus)")

        # ---  Menu Cek Tugas ---
        @self.bot.message_handler(func=lambda m: m.text == "📋 Cek Tugas")
        def check(m):
            tasks = self.sm.get_tasks(30)[:10]
            res = "<b>📋 Daftar 10 Tugas Terdekat:</b>\n" + "\n".join([f"• {t['Nama Tugas']} ({t['Tanggal Tugas']})" for t in tasks])
            self.bot.send_message(m.chat.id, res if tasks else "Tidak ada tugas aktif.")

        # ---  Menu Selesaikan Tugas --- (telegram.py)
        @self.bot.message_handler(func=lambda m: m.text == "✅ Selesaikan Tugas")
        def done_list(m):
            tasks = self.sm.get_tasks(30)[:10]
            if not tasks:
                self.bot.send_message(m.chat.id, "Tidak ada tugas aktif.")
                return
            self.temp_done[m.chat.id] = [] # Reset pilihan
            self.show_selection_menu(m.chat.id, tasks)


        # ---  Menangkap Teks  ---
        @self.bot.message_handler(func=lambda m: True)
        def handle_text(m):
            # Hanya proses jika user dalam mode 'waiting_task'
            if self.user_modes.get(m.chat.id) == 'waiting_task':
                tasks = self.ai.parse(m.text)
                if not isinstance(tasks, list) or not tasks:
                    self.bot.send_message(m.chat.id, "Maaf, ASKY gagal mengenali tugas tersebut.")
                    return
                
                self.temp_add[m.chat.id] = tasks
                self.user_modes[m.chat.id] = None # Reset mode
                
                msg = f"<b>Konfirmasi {len(tasks)} Tugas Baru:</b>\n" + "\n".join([f"- {t.get('task')}" for t in tasks])
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✅ Simpan", callback_data="save_task"),
                           types.InlineKeyboardButton("❌ Batal", callback_data="cancel_task"))
                self.bot.send_message(m.chat.id, msg, reply_markup=markup)

        # --- Klik Tombol Inline (Callback Query) ---
        @self.bot.callback_query_handler(func=lambda c: True)
        def cb(c):
            uid = c.message.chat.id
            
            # LOGIC 1: User klik nama tugas (untuk dicentang/hapus centang)
            if c.data.startswith("select_"):
                name = c.data[7:] # Ambil nama tugas (buang prefix 'select_')
                selected = self.temp_done.get(uid, [])
                
                # Toggle Logic: Kalau ada -> hapus. Kalau belum -> tambah.
                if name in selected: selected.remove(name)
                else: selected.append(name)
                
                self.temp_done[uid] = selected
                # Refresh tampilan menu (render ulang tombol)
                self.show_selection_menu(uid, self.sm.get_tasks(30)[:10], c.message.message_id)
            
            # LOGIC 2: User klik 'Konfirmasi Selesai'
            elif c.data == "confirm_bulk":
                selected = self.temp_done.get(uid, [])
                if not selected:
                    self.bot.answer_callback_query(c.id, "⚠️ Pilih minimal 1 tugas!", show_alert=True)
                    return
                
                if self.sm.mark_done_bulk(selected):
                    try:
                        self.bot.edit_message_text(f"✅ <b>{len(selected)} Tugas berhasil diselesaikan!</b>", uid, c.message.message_id)
                    except ApiTelegramException as e:
                        if "message is not modified" not in e.description: print(f"ERR: {e}")
                self.temp_done.pop(uid, None)
            
            # LOGIC 3: User klik 'Simpan' (Hasil AI)
            elif c.data == "save_task":
                if self.sm.save_tasks(self.temp_add.get(uid, [])):
                    try:
                        self.bot.edit_message_text("✅ <b>Berhasil disimpan ke Sheets!</b>", uid, c.message.message_id)
                    except ApiTelegramException as e:
                        if "message is not modified" not in e.description: print(f"ERR: {e}")
                self.temp_add.pop(uid, None)
            
            # LOGIC 4: Tombol Batal
            elif c.data in ["cancel_done", "cancel_task"]:
                try:
                    self.bot.edit_message_text("❌ <b>Dibatalkan.</b>", uid, c.message.message_id)
                except ApiTelegramException as e:
                    if "message is not modified" not in e.description: print(f"ERR: {e}")

        # --- Menjalankan Polling ---
        print("[LOG] Bot ASKY active ...")
        self.bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=20)