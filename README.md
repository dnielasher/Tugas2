# Tugas2

# Kapita Selekta - Users Module (FastAPI)

Instruksi:
1. Buat virtualenv:
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate

2. Install:
   pip install -r requirements.txt

3. Jalankan server (dev):
   uvicorn app.main:app --reload

4. Jalankan unit tests:
   pytest -q

Auth (simple untuk tugas):
- Header `X-Username` dan `X-Role` digunakan untuk simulasi otentikasi.
- Tidak menggunakan JWT (sesuai soal).

Catatan:
- Cara auth ini **tidak aman** di produksi — hanya untuk memenuhi syarat tugas.
