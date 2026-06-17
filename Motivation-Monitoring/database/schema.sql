CREATE TABLE IF NOT EXISTS siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    kelas TEXT
);

CREATE TABLE IF NOT EXISTS indikator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT
);

CREATE TABLE IF NOT EXISTS penilaian (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_siswa INTEGER,
    tanggal TEXT,
    penyebab TEXT,
    rekomendasi TEXT
);

CREATE TABLE IF NOT EXISTS detail_penilaian (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_penilaian INTEGER,
    indikator TEXT,
    nilai INTEGER
);

CREATE TABLE IF NOT EXISTS aktivitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_siswa INTEGER,
    hadir INTEGER,
    aktif INTEGER,
    tugas INTEGER,
    diskusi INTEGER
);
