from flask import request, redirect
from config.db_config import get_db_connection

def tambah_siswa():
    nama = request.form['nama']
    kelas = request.form['kelas']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO siswa (nama, kelas) VALUES (?, ?)",
        (nama, kelas)
    )

    conn.commit()
    conn.close()

    return redirect('/siswa')