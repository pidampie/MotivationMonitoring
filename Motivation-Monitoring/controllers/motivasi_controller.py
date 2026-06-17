from services.analisis_service import get_rekomendasi
from services.analisis_service import get_penyebab
from flask import request, redirect
from config.db_config import get_db_connection
from datetime import datetime

def simpan_penilaian():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ambil data siswa
    data = request.form.to_dict()
    penyebab = get_penyebab(data)
    rekomendasi = get_rekomendasi(penyebab)
    id_siswa = request.form['id_siswa']
    tanggal = datetime.now().strftime("%Y-%m-%d")

    # 🔥 PERBAIKAN DI SINI (TAMBAH PENYEBAB)
    cursor.execute("""
        INSERT INTO penilaian (id_siswa, tanggal, penyebab)
        VALUES (?, ?, ?)
    """, (id_siswa, tanggal, ", ".join(penyebab)))

    id_penilaian = cursor.lastrowid

    # Semua indikator dari form
    indikator_list = [
        'K1','K2','K3','K4',
        'D1','D2','D3','D4',
        'T1','T2','T3','T4',
        'M1','M2','M3','M4'
    ]

    # Simpan ke detail_penilaian
    for indikator in indikator_list:
        nilai = request.form.get(indikator)

        if nilai:
            cursor.execute("""
                INSERT INTO detail_penilaian (id_penilaian, indikator, nilai)
                VALUES (?, ?, ?)
            """, (id_penilaian, indikator, int(nilai)))

    conn.commit()
    conn.close()

    return redirect('/dashboard')