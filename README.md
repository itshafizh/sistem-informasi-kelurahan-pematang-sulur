# SIAK PKK — Sistem Informasi Administrasi Kelurahan

Setup awal (Tahap 2) project Django untuk digitalisasi surat masuk/keluar dan
pelaporan kegiatan PKK.

## Cara Menjalankan (Setup Awal)

1. **Buat & aktifkan virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

2. **Install dependency**
   ```bash
   pip install -r requirements.txt
   ```

3. **Isi file `.env`**
   Edit file `.env` yang sudah ada (isinya salinan dari `.env.example`),
   sesuaikan `SECRET_KEY` dan kredensial MySQL Anda.

4. **Buat database MySQL**
   ```sql
   CREATE DATABASE siak_pkk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   (Sesuaikan nama database dengan `DB_NAME` di `.env` jika berbeda.)

5. **Jalankan migrasi & server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Buka `http://127.0.0.1:8000/` — jika muncul halaman default Django tanpa
   error koneksi database, setup berhasil.

## Struktur Project

```
siak_pkk/
├── manage.py
├── requirements.txt
├── .env / .env.example
├── config/          # settings, urls, wsgi, asgi
├── apps/            # setiap modul (accounts, surat_masuk, dst) akan ditambahkan bertahap
├── static/          # css, js, img
├── media/           # tempat file upload surat & dokumentasi PKK
└── templates/       # base.html & partials (ditambahkan di tahap dashboard)
```

## Tahap Selanjutnya

- Tahap 3: Buat database/model (`roles`, `users/profile`, `jenis_surat`, `pokja`, dst)
- Tahap 4: Autentikasi & role (app `accounts`)
