REZA.DEV — PERSONAL PORTFOLIO (STABLE COLOR PULL 2.1)
=====================================================

APA YANG DIPERBAIKI
- Menggunakan port 5051 agar tidak tertukar dengan server versi lama di port 5000.
- Nama tab browser ditandai Reza Portfolio v2.1.
- Aksen ungu dan foto polaroid berwarna.
- Tali foto mempunyai area klik yang lebih lebar, sehingga lebih mudah ditarik.
- Foto dapat diayun ke kiri/kanan dan ditarik turun untuk memanjangkan tali.
- Saat dilepas, foto tetap memiliki momentum lalu kembali perlahan.
- Konten tetap terlihat jika JavaScript tidak berjalan; animasi scroll hanya aktif setelah JavaScript siap.
- Layout desktop dua kolom dan berubah menjadi satu kolom pada layar kecil.

CARA MENJALANKAN DI WINDOWS
1. Ekstrak ZIP ke folder BARU.
2. Jika server versi lama masih berjalan, buka terminal lamanya lalu tekan Ctrl+C.
3. Di VS Code pilih File > Open Folder, lalu pilih folder hasil ekstrak yang bernama reza_portfolio_stable_21.
4. Buka Terminal > New Terminal.
5. Jalankan: python -m pip install -r requirements.txt
6. Jalankan: python app.py
7. Buka browser ke: http://127.0.0.1:5051

PENTING
Jangan membuka lagi alamat lama http://127.0.0.1:5000. Versi ini menggunakan 5051 supaya browser tidak menampilkan server portfolio lama.

MENGGANTI FOTO PROFIL
- Buka folder static.
- Ganti profile.jpg dengan foto milikmu.
- Pertahankan nama file profile.jpg.
- Foto ditampilkan berwarna; tidak ada filter grayscale.
- Refresh browser dengan Ctrl+F5.

MENGUBAH DATA DIRI
Edit dictionary PROFILE di bagian atas app.py. Skill, proyek, pendidikan, dan minat juga dapat diubah di daftar SKILLS, PROJECTS, EDUCATION, dan INTERESTS.

DATABASE
portfolio.db dibuat otomatis saat aplikasi dijalankan. Pesan formulir kontak disimpan di SQLite. Form ini belum mengirim email otomatis.

TROUBLESHOOTING
- Jika perintah python tidak dikenali, coba python3 -m pip install -r requirements.txt dan python3 app.py.
- Jika port 5051 sedang dipakai, hentikan program lama yang memakai port tersebut atau ubah port pada baris app.run di app.py.
- Jika CSS lama masih terlihat, tekan Ctrl+F5.

Catatan: ini proyek lokal untuk pembelajaran. Sebelum dipublikasikan, ganti SECRET_KEY dan gunakan server deployment yang sesuai.
