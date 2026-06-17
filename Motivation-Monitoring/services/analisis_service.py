def get_penyebab(data):
    mapping = {
        "K1": "Kurang aktif bertanya",
        "K2": "Jarang menjawab pertanyaan",
        "K3": "Tidak aktif dalam diskusi",
        "K4": "Jarang menyampaikan pendapat",

        "D1": "Sering terlambat hadir",
        "D2": "Sering terlambat mengumpulkan tugas",
        "D3": "Kurang disiplin terhadap aturan",
        "D4": "Tidak membawa perlengkapan belajar",

        "T1": "Mudah menyerah saat kesulitan",
        "T2": "Tidak menyelesaikan tugas",
        "T3": "Kurang fokus saat belajar",
        "T4": "Tidak belajar mandiri",

        "M1": "Kurang antusias mengikuti pelajaran",
        "M2": "Rasa ingin tahu rendah",
        "M3": "Tidak menikmati pembelajaran",
        "M4": "Tidak mencari sumber belajar tambahan"
    }

    penyebab = []

    for key, value in data.items():
        if key != "id_siswa" and value:
            try:
                if int(value) <= 2:
                    penyebab.append(mapping.get(key, key))
            except:
                pass  # biar tidak error kalau value aneh

    return penyebab


def get_rekomendasi(penyebab_list):
    mapping = {
        "Kurang aktif bertanya": "Guru perlu memberikan pertanyaan pemantik",
        "Jarang menjawab pertanyaan": "Berikan kesempatan siswa menjawab secara bergiliran",
        "Tidak aktif dalam diskusi": "Gunakan metode diskusi kelompok kecil",
        "Jarang menyampaikan pendapat": "Ciptakan suasana kelas yang lebih terbuka",

        "Sering terlambat hadir": "Perlu pengawasan kedisiplinan kehadiran",
        "Sering terlambat mengumpulkan tugas": "Berikan reminder tugas secara berkala",
        "Kurang disiplin terhadap aturan": "Tegaskan aturan kelas secara konsisten",
        "Tidak membawa perlengkapan belajar": "Biasakan checklist perlengkapan sebelum belajar",

        "Mudah menyerah saat kesulitan": "Berikan motivasi dan pendampingan belajar",
        "Tidak menyelesaikan tugas": "Berikan tugas bertahap dan monitoring",
        "Kurang fokus saat belajar": "Gunakan metode pembelajaran interaktif",
        "Tidak belajar mandiri": "Berikan tugas eksplorasi mandiri",

        "Kurang antusias mengikuti pelajaran": "Gunakan media pembelajaran menarik",
        "Rasa ingin tahu rendah": "Berikan stimulus berupa pertanyaan terbuka",
        "Tidak menikmati pembelajaran": "Gunakan metode belajar yang variatif",
        "Tidak mencari sumber belajar tambahan": "Arahkan ke sumber belajar tambahan"
    }

    rekomendasi = []

    for p in penyebab_list:
        if p in mapping:
            rekomendasi.append(mapping[p])

    return rekomendasi