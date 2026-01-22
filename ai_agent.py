import os
import json
import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        # Menggunakan model Llama 3.3 70B yang aktif
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile" 
        self.context = (
            f"Hari ini: {datetime.date.today()}. Tugas: Ekstrak hingga 10 poin tugas "
            "dari input user ke dalam format JSON dengan key 'tasks'. "
            "Setiap item: {'task': str, 'date': 'YYYY-MM-DD', 'category': str}. "
            "Jika tanggal tidak disebut, gunakan hari ini. Balas HANYA JSON murni."
        )

    def parse(self, text: str) -> list:
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "system", "content": self.context}, {"role": "user", "content": text}],
                model=self.model,
                response_format={"type": "json_object"}
            )
            res = json.loads(completion.choices[0].message.content)
            # Menjamin output berupa list dari key 'tasks'
            data = res.get('tasks', [])
            if not isinstance(data, list):
                data = [data] if data else []
            return data[:10]
        except Exception as e:
            print(f"Error in AIAgent: {e}")
            return []
