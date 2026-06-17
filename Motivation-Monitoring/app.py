from flask import Flask, render_template, redirect, request
from config.db_config import get_db_connection
from models.siswa import get_all_siswa
from controllers.motivasi_controller import simpan_penilaian
from controllers.siswa_controller import tambah_siswa
from controllers.aktivitas_controller import simpan_aktivitas

app = Flask(__name__)

# =========================================================
# 1. INITIALIZATION DATABASE (MANAJEMEN BASIS DATA AWAL)
# =========================================================
def init_db():
    conn = get_db_connection()
    
    # Jalankan schema dasar aplikasi
    with open('database/schema.sql') as f:
        conn.executescript(f.read())
        
    # Buat tabel master pengguna untuk profil dinamis jika belum ada
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pengguna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nomor_induk TEXT NOT NULL,
            jabatan TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    
    # Periksa ketersediaan data, jika kosong (0), suntikkan data awal default
    cek_pengguna = conn.execute("SELECT COUNT(*) FROM pengguna").fetchone()[0]
    if cek_pengguna == 0:
        conn.execute("""
            INSERT INTO pengguna (id, nama, nomor_induk, jabatan, email)
            VALUES (1, ?, ?, ?, ?)
        """, ('Muhammad Yasir, S.Pd.', '19982025101002', 'Guru Bimbingan Konseling (BK)', 'yasir.unila@school.sch.id'))
        conn.commit()
        print("LOG: Data pengguna default berhasil ditambahkan ke database!")
        
    conn.close()
    print("Database berhasil dibuat & diverifikasi!")

# Eksekusi pembuatan database saat aplikasi pertama kali berjalan
init_db()

# =========================================================
# 2. TEST KONEKSI DATABASE
# =========================================================
def test_db():
    conn = get_db_connection()
    print("Database berhasil connect!")
    conn.close()

test_db()

# =========================================================
# 3. CORE SYSTEM ROUTES (NAVIGASI UTAMA)
# =========================================================

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()

    # Mengambil akumulasi total siswa dan aktivitas harian
    total_siswa = conn.execute("SELECT COUNT(*) FROM siswa").fetchone()[0]
    total_aktivitas = conn.execute("SELECT COUNT(*) FROM aktivitas").fetchone()[0]

    # Ambil log aktivitas paling terbaru dari setiap peserta didik (Skala 100)
    data = conn.execute("""
        SELECT a.*, s.nama,
        (a.hadir + a.aktif + a.tugas + a.diskusi)/4 as skor
        FROM aktivitas a
        JOIN siswa s ON a.id_siswa = s.id
        WHERE a.id IN (SELECT MAX(id) FROM aktivitas GROUP BY id_siswa)
    """).fetchall()

    tinggi = sedang = rendah = total = 0
    hasil = []

    for d in data:
        skor = round(d['skor'], 2)
        total += skor

        if skor >= 75:
            kategori = "Tinggi"
            tinggi += 1
        elif skor >= 50:
            kategori = "Sedang"
            sedang += 1
        else:
            kategori = "Rendah"
            rendah += 1

        hasil.append({
            "nama": d["nama"],
            "skor": skor,
            "kategori": kategori
        })

    avg = round(total / len(data), 2) if data else 0

    # Mengambil pemeringkatan Top 3 Siswa dan 5 log aktivitas terbaru
    top = sorted(hasil, key=lambda x: x['skor'], reverse=True)[:3]
    recent = hasil[-5:]

    # AMBIL DATA PROFILE USER: Untuk sinkronisasi nama pengajar di pojok kanan atas dashboard secara dinamis
    user_data = conn.execute("SELECT * FROM pengguna WHERE id = 1").fetchone()
    conn.close()

    return render_template(
        'dashboard.html',
        total_siswa=total_siswa,
        total_aktivitas=total_aktivitas,
        tinggi=tinggi,
        sedang=sedang,
        rendah=rendah,
        avg=avg,
        top=top,
        recent=recent,
        user=user_data
    )

@app.route('/simpan_penilaian', methods=['POST'])
def simpan():
    return simpan_penilaian()

@app.route('/tambah_siswa', methods=['POST'])
def simpan_siswa():
    return tambah_siswa()

@app.route('/siswa')
def siswa():
    data = get_all_siswa()
    return render_template('siswa.html', siswa=data)

@app.route('/aktivitas')
def aktivitas():
    conn = get_db_connection()

    data = conn.execute("""
        SELECT a.*, s.nama,
        (a.hadir + a.aktif + a.tugas + a.diskusi)/4 as skor
        FROM aktivitas a
        JOIN siswa s ON a.id_siswa = s.id
    """).fetchall()

    hasil = []
    for d in data:
        skor = round(d['skor'], 2)

        if skor >= 75:
            kategori = "Tinggi"
        elif skor >= 50:
            kategori = "Sedang"
        else:
            kategori = "Rendah"

        hasil.append({
            "nama": d["nama"],
            "hadir": d["hadir"],
            "aktif": d["aktif"],
            "tugas": d["tugas"],
            "diskusi": d["diskusi"],
            "skor": skor,
            "kategori": kategori
        })

    conn.close()
    siswa = get_all_siswa()

    return render_template('aktivitas.html', siswa=siswa, aktivitas=hasil)

@app.route('/simpan_aktivitas', methods=['POST'])
def simpanAktivitas():
    return simpan_aktivitas()

@app.route('/motivasi')
def motivasi():
    data = get_all_siswa()
    return render_template('input.html', siswa=data)

@app.route('/asesmen_kompleks')
def asesmen_kompleks():
    data_siswa = get_all_siswa()
    return render_template('asesmen_kompleks.html', siswa=data_siswa)

# =====================================================================
# INDEKS PROSES: DATA DIJAMIN PARALEL MASUK KE SEMUA DASHBOARD & FITUR
# =====================================================================
@app.route('/simpan_asesmen_kompleks', methods=['POST'])
def simpan_asesmen_kompleks():
    conn = get_db_connection()
    try:
        id_siswa = request.form.get('id_siswa')
        skor_akhir = float(request.form.get('skor_akhir', 0))
        kategori_akhir = request.form.get('kategori_akhir', 'Sedang')
        
        # 1. Sinkronisasi Tabel 'aktivitas' (Akan dibaca oleh Dashboard, Laporan, dan Notifikasi)
        conn.execute("""
            INSERT INTO aktivitas (id_siswa, hadir, aktif, tugas, diskusi)
            VALUES (?, ?, ?, ?, ?)
        """, (id_siswa, skor_akhir, skor_akhir, skor_akhir, skor_akhir))
        
        # 2. Perumusan Narasi Tindak Lanjut untuk Semua Jenjang Nilai (Termasuk yang Tinggi)
        if skor_akhir >= 75:
            penyebab = "Kondisi motivasi internal sangat baik dan konsisten di kelas."
            rekomendasi_bk = "Berikan apresiasi, sertakan dalam program pengayaan atau motivasi sebaya."
        elif skor_akhir >= 50:
            penyebab = "Indikator keterlibatan kelas mulai menurun, perlu pemantauan berkala."
            rekomendasi_bk = "Lakukan monitoring dan berikan motivasi tambahan secara personal."
        else:
            penyebab = "Peserta didik mengalami penurunan minat belajar dan kurang fokus."
            rekomendasi_bk = "Panggil tatap muka untuk intervensi khusus dan layanan konseling intensif."

        # 3. Sinkronisasi Tabel 'penilaian' (Akan langsung ditampilkan di halaman Rekomendasi BK)
        conn.execute("""
            INSERT INTO penilaian (id_siswa, penyebab, rekomendasi)
            VALUES (?, ?, ?)
        """, (id_siswa, penyebab, rekomendasi_bk))
        
        conn.commit()
        print(f"LOG BERHASIL: Asesmen Siswa ID {id_siswa} berhasil disimpan paralel di semua fitur!")
        
    except Exception as e:
        print("ERROR pada database saat memproses Asesmen Kompleks:", e)
    finally:
        conn.close()
        
    # Otomatis dialihkan ke halaman rekomendasi untuk melihat tabel distribusi hasil akhir
    return redirect('/rekomendasi')

@app.route('/laporan')
def laporan():
    conn = get_db_connection()

    data = conn.execute("""
        SELECT a.*, s.nama,
        (a.hadir + a.aktif + a.tugas + a.diskusi)/4 as rata
        FROM aktivitas a
        JOIN siswa s ON a.id_siswa = s.id
        WHERE a.id IN (SELECT MAX(id) FROM aktivitas GROUP BY id_siswa)
    """).fetchall()

    hasil = []
    for d in data:
        rata = round(d['rata'], 2)

        if rata >= 75:
            kategori = "Tinggi"
        elif rata >= 50:
            kategori = "Sedang"
        else:
            kategori = "Rendah"

        hasil.append({
            "nama": d["nama"],
            "rata": rata,
            "kategori": kategori
        })

    conn.close()
    return render_template('laporan.html', data=hasil)

@app.route('/notifikasi')
def notifikasi():
    conn = get_db_connection()

    data = conn.execute("""
        SELECT a.*, s.nama,
        (a.hadir + a.aktif + a.tugas + a.diskusi)/4 as rata
        FROM aktivitas a
        JOIN siswa s ON a.id_siswa = s.id
        WHERE a.id IN (SELECT MAX(id) FROM aktivitas GROUP BY id_siswa)
    """).fetchall()

    hasil = []
    for d in data:
        rata = round(d['rata'], 2)

        if rata >= 75:
            kategori = "Tinggi"
            pesan = "Motivasi sangat baik, pertahankan konsistensi belajar peserta didik"
        elif rata >= 50:
            kategori = "Sedang"
            pesan = "Perlu monitoring berkala terhadap keterlibatan indikator kelas"
        else:
            kategori = "Rendah"
            pesan = "Perlu intervensi khusus dan rujukan layanan konseling secepatnya"

        hasil.append({
            "nama": d["nama"],
            "rata": rata,
            "kategori": kategori,
            "pesan": pesan
        })

    conn.close()
    return render_template('notifikasi.html', data=hasil)

# =====================================================================
# ROUTE PERBAIKAN SINKRONISASI TOTAL: REKOMENDASI AUTO-SYNC FROM AKTIVITAS
# =====================================================================
@app.route('/rekomendasi')
def rekomendasi():
    conn = get_db_connection()
    try:
        # 1. Cek apakah ada data di tabel penilaian
        cek_data = conn.execute("SELECT COUNT(*) FROM penilaian").fetchone()[0]
        
        # 2. AUTO-SYNC: Jika tabel penilaian kosong, ambil langsung data dari tabel aktivitas
        if cek_data == 0:
            # Menggunakan SELECT * agar aman dari kesalahan nama kolom nilai
            aktivitas_data = conn.execute("""
                SELECT * FROM aktivitas 
                WHERE id IN (SELECT MAX(id) FROM aktivitas GROUP BY id_siswa)
            """).fetchall()
            
            for akt in aktivitas_data:
                id_s = akt['id_siswa']
                
                # Mengambil nilai hadir jika ada, jika tidak default ke 80
                # Ini menghindari error jika nama kolom berbeda
                skor_hadir = akt['hadir'] if 'hadir' in akt.keys() else 80
                
                # Tentukan status rekomendasi secara aman
                if skor_hadir >= 80:
                    penyebab = "Kondisi motivasi internal sangat baik dan konsisten di kelas."
                    rekomendasi_bk = "Berikan apresiasi, sertakan dalam program pengayaan atau motivasi sebaya."
                elif skor_hadir >= 60:
                    penyebab = "Indikator keterlibatan kelas mulai menurun, perlu pemantauan berkala."
                    rekomendasi_bk = "Lakukan monitoring dan berikan motivasi tambahan secara personal."
                else:
                    penyebab = "Peserta didik mengalami penurunan minat belajar dan kurang fokus."
                    rekomendasi_bk = "Panggil tatap muka untuk intervensi khusus dan layanan konseling intensif."
                
                conn.execute("""
                    INSERT INTO penilaian (id_siswa, penyebab, rekomendasi)
                    VALUES (?, ?, ?)
                """, (id_s, penyebab, rekomendasi_bk))
            conn.commit()
            print("LOG: Berhasil auto-sync data dari aktivitas ke rekomendasi.")

        # 3. Ambil data gabungan final untuk dilempar ke HTML
        data = conn.execute("""
            SELECT p.id, s.nama, 
                   IFNULL(p.penyebab, '-') as penyebab, 
                   IFNULL(p.rekomendasi, '-') as rekomendasi
            FROM penilaian p
            JOIN siswa s ON p.id_siswa = s.id
            ORDER BY p.id DESC
        """).fetchall()
        
    except Exception as e:
        # Jika ada error, cetak pesan error aslinya ke terminal agar kita tahu kolom apa yang salah
        print("\n=== ERROR RUNTIME REKOMENDASI ===")
        print(e)
        print("=================================\n")
        data = []
    finally:
        conn.close()
        
    return render_template('rekomendasi.html', data=data)

# =========================================================
# 4. ACTION ROUTES: DATA MANAGEMENT (CRUD - DELETE)
# =========================================================

@app.route('/hapus_rekomendasi/<int:id>')
def hapus_rekomendasi(id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM penilaian WHERE id = ?", (id,))
        conn.commit()
        print(f"LOG: Data rekomendasi dengan ID {id} berhasil dihapus!")
    except Exception as e:
        print("ERROR saat menghapus data rekomendasi:", e)
    finally:
        conn.close()
        
    return redirect('/rekomendasi')

@app.route('/hapus_siswa/<int:id>')
def hapus_siswa(id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM siswa WHERE id = ?", (id,))
        conn.commit()
        print(f"LOG: Data siswa dengan ID {id} berhasil dihapus!")
    except Exception as e:
        print("ERROR saat menghapus data siswa:", e)
    finally:
        conn.close()
        
    return redirect('/siswa')

# =========================================================
# 5. USER DYNAMIC PROFILE MANAGEMENT ROUTES
# =========================================================
@app.route('/profil', methods=['GET', 'POST'])
def profil():
    conn = get_db_connection()
    
    # [PROTEKSI EXTRA] Cek paksa ketersediaan user harian agar tidak memicu error NoneType
    cek_pengguna = conn.execute("SELECT COUNT(*) FROM pengguna").fetchone()[0]
    if cek_pengguna == 0:
        conn.execute("""
            INSERT INTO pengguna (id, nama, nomor_induk, jabatan, email)
            VALUES (1, ?, ?, ?, ?)
        """, ('Muhammad Yasir, S.Pd.', '19982025101002', 'Guru Bimbingan Konseling (BK)', 'yasir.unila@school.sch.id'))
        conn.commit()
    
    if request.method == 'POST':
        nama_baru = request.form.get('nama')
        nomor_baru = request.form.get('nomor_induk')
        jabatan_baru = request.form.get('jabatan')
        email_baru = request.form.get('email')
        
        conn.execute("""
            UPDATE pengguna 
            SET nama = ?, nomor_induk = ?, jabatan = ?, email = ?
            WHERE id = 1
        """, (nama_baru, nomor_baru, jabatan_baru, email_baru))
        conn.commit()
        conn.close()
        
        print("LOG: Data profil berhasil disimpan langsung ke database!")
        return redirect('/profil')
        
    user_data = conn.execute("SELECT * FROM pengguna WHERE id = 1").fetchone()
    conn.close()
    
    return render_template('profil.html', user=user_data)

@app.route('/logout')
def logout():
    return redirect('/')

# =========================================================
# RUN APP ENGINE
# =========================================================
if __name__ == '__main__':
    app.run(debug=True)