from flask import request, redirect
from config.db_config import get_db_connection

def simpan_aktivitas():
    conn = get_db_connection()
    cursor = conn.cursor()

    id_siswa = request.form['id_siswa']
    hadir = request.form['hadir']
    aktif = request.form['aktif']
    tugas = request.form['tugas']
    diskusi = request.form['diskusi']

    cursor.execute("""
        INSERT INTO aktivitas (id_siswa, hadir, aktif, tugas, diskusi)
        VALUES (?, ?, ?, ?, ?)
    """, (id_siswa, hadir, aktif, tugas, diskusi))

    conn.commit()
    conn.close()

    return redirect('/aktivitas')