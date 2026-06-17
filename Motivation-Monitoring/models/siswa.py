from config.db_config import get_db_connection

def get_all_siswa():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM siswa").fetchall()
    conn.close()
    return data