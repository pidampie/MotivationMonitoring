// ================== DATA ==================
let siswa = JSON.parse(localStorage.getItem("siswa")) || [];
let data = JSON.parse(localStorage.getItem("data")) || [];

// ================== SISWA ==================
function tambahSiswa() {
  let input = document.getElementById("namaSiswa");
  if (!input) return;

  let nama = input.value.trim();

  if (nama === "") {
    alert("Nama tidak boleh kosong!");
    return;
  }

  siswa.push(nama);
  localStorage.setItem("siswa", JSON.stringify(siswa));

  input.value = "";
  tampilSiswa();
}

function tampilSiswa() {
  let list = document.getElementById("listSiswa");
  if (!list) return;

  list.innerHTML = "";

  siswa.forEach((s, index) => {
    list.innerHTML += `
      <tr>
        <td>${s}</td>
        <td>
          <button class="btn-delete" onclick="hapusSiswa(${index})">
            Hapus
          </button>
        </td>
      </tr>
    `;
  });
}

function hapusSiswa(index) {
  if (confirm("Yakin ingin menghapus siswa ini?")) {
    siswa.splice(index, 1);
    localStorage.setItem("siswa", JSON.stringify(siswa));
    tampilSiswa();
  }
}

// ================== MOTIVASI ==================
function hitung() {
  let nama = document.getElementById("nama")?.value;
  let k = +document.getElementById("k")?.value || 0;
  let a = +document.getElementById("a")?.value || 0;
  let t = +document.getElementById("t")?.value || 0;
  let d = +document.getElementById("d")?.value || 0;

  if (!nama) {
    alert("Nama harus diisi!");
    return;
  }

  let skor = 0.3 * k + 0.25 * a + 0.25 * t + 0.2 * d;

  let kategori = skor >= 80 ? "Tinggi" : skor >= 60 ? "Sedang" : "Rendah";

  let hasil = document.getElementById("hasil");
  if (hasil) {
    hasil.innerText = skor.toFixed(1) + " (" + kategori + ")";
  }

  data.push({ nama, skor, kategori });
  localStorage.setItem("data", JSON.stringify(data));
}

// ================== LOAD SEMUA HALAMAN ==================
window.onload = function () {
  // SISWA
  tampilSiswa();

  // LAPORAN
  let table = document.getElementById("data");
  if (table) {
    table.innerHTML = "";
    data.forEach((d) => {
      table.innerHTML += `
        <tr>
          <td>${d.nama}</td>
          <td>${d.skor.toFixed(1)}</td>
          <td>${d.kategori}</td>
        </tr>
      `;
    });
  }

  // DASHBOARD
  let total = document.getElementById("total");
  let tinggi = document.getElementById("tinggi");
  let rendah = document.getElementById("rendah");

  if (total) total.innerText = siswa.length;
  if (tinggi)
    tinggi.innerText = data.filter((d) => d.kategori === "Tinggi").length;
  if (rendah)
    rendah.innerText = data.filter((d) => d.kategori === "Rendah").length;

  // NOTIFIKASI
  let notif = document.getElementById("notif");
  if (notif) {
    notif.innerHTML = "";
    data
      .filter((d) => d.kategori === "Rendah")
      .forEach((d) => {
        notif.innerHTML += `
          <div class="notif rendah">
            ${d.nama} memiliki motivasi rendah
          </div>
        `;
      });
  }

  // REKOMENDASI
  let rekom = document.getElementById("rekom");
  if (rekom) {
    rekom.innerHTML = "";
    data.forEach((d) => {
      let saran =
        d.kategori === "Rendah"
          ? "Konseling"
          : d.kategori === "Sedang"
            ? "Pendampingan"
            : "Apresiasi";

      rekom.innerHTML += `
        <div class="card">
          ${d.nama} → ${saran}
        </div>
      `;
    });
  }
};
// ================== AKTIVITAS ==================
let aktivitas = JSON.parse(localStorage.getItem("aktivitas")) || [];

/* LOAD DROPDOWN SISWA */
function loadSiswaDropdown() {
  let select = document.getElementById("namaAktif");
  if (!select) return;

  select.innerHTML = "<option value=''>Pilih Siswa</option>";

  siswa.forEach((s) => {
    select.innerHTML += `<option value="${s}">${s}</option>`;
  });
}

/* PREVIEW MOTIVASI */
function previewMotivasi() {
  let k = +document.getElementById("hadir").value || 0;
  let a = +document.getElementById("aktif").value || 0;
  let t = +document.getElementById("tugas").value || 0;
  let d = +document.getElementById("diskusi").value || 0;

  let skor = 0.3 * k + 0.25 * a + 0.25 * t + 0.2 * d;

  let kategori = skor >= 80 ? "Tinggi" : skor >= 60 ? "Sedang" : "Rendah";

  document.getElementById("preview").innerText =
    "Skor: " + skor.toFixed(1) + " (" + kategori + ")";
}

/* SIMPAN AKTIVITAS */
function simpanAktivitas() {
  let nama = document.getElementById("namaAktif").value;
  let k = +document.getElementById("hadir").value;
  let a = +document.getElementById("aktif").value;
  let t = +document.getElementById("tugas").value;
  let d = +document.getElementById("diskusi").value;

  if (!nama) {
    alert("Pilih siswa!");
    return;
  }

  let skor = 0.3 * k + 0.25 * a + 0.25 * t + 0.2 * d;
  let kategori = skor >= 80 ? "Tinggi" : skor >= 60 ? "Sedang" : "Rendah";

  aktivitas.push({ nama, k, a, t, d, skor, kategori });
  localStorage.setItem("aktivitas", JSON.stringify(aktivitas));

  tampilAktivitas();
}

/* TAMPILKAN AKTIVITAS */
function tampilAktivitas() {
  let list = document.getElementById("aktivitasList");
  if (!list) return;

  list.innerHTML = "";

  aktivitas.forEach((d, i) => {
    let warna =
      d.kategori === "Tinggi"
        ? "status-tinggi"
        : d.kategori === "Sedang"
          ? "status-sedang"
          : "status-rendah";

    list.innerHTML += `
      <tr>
        <td>${d.nama}</td>
        <td>${d.k}</td>
        <td>${d.a}</td>
        <td>${d.t}</td>
        <td>${d.d}</td>
        <td>${d.skor.toFixed(1)}</td>
        <td class="${warna}">${d.kategori}</td>
        <td>
          <button class="btn-delete" onclick="hapusAktivitas(${i})">
            Hapus
          </button>
        </td>
      </tr>
    `;
  });

  updateRingkasan();
}

/* HAPUS */
function hapusAktivitas(i) {
  if (confirm("Hapus data ini?")) {
    aktivitas.splice(i, 1);
    localStorage.setItem("aktivitas", JSON.stringify(aktivitas));
    tampilAktivitas();
  }
}

/* RINGKASAN */
function updateRingkasan() {
  document.getElementById("totalAktivitas").innerText = aktivitas.length;

  let avg =
    aktivitas.reduce((sum, d) => sum + d.k, 0) / (aktivitas.length || 1);

  document.getElementById("avgKehadiran").innerText = avg.toFixed(1) + "%";

  let low = aktivitas.filter((d) => d.kategori === "Rendah").length;
  document.getElementById("lowCount").innerText = low;
}

// ================== NOTIFIKASI ==================
function tampilNotifikasi() {
  let aktivitas = JSON.parse(localStorage.getItem("aktivitas")) || [];
  let list = document.getElementById("notifList");

  if (!list) return;

  list.innerHTML = "";

  let rendah = 0,
    sedang = 0,
    tinggi = 0;

  aktivitas.forEach((d, i) => {
    let html = "";

    if (d.kategori === "Rendah") {
      rendah++;

      html = `
        <div class="notif rendah">
          🔴 <b>${d.nama}</b> memiliki motivasi rendah (${d.skor.toFixed(1)})
          <br>Rekomendasi: Konseling
        </div>
      `;
    } else if (d.kategori === "Sedang") {
      sedang++;

      html = `
        <div class="notif sedang">
          ⚠️ <b>${d.nama}</b> memiliki motivasi sedang (${d.skor.toFixed(1)})
          <br>Rekomendasi: Monitoring
        </div>
      `;
    } else {
      tinggi++;

      html = `
        <div class="notif tinggi">
          ✅ <b>${d.nama}</b> memiliki motivasi tinggi (${d.skor.toFixed(1)})
          <br>Rekomendasi: Apresiasi
        </div>
      `;
    }

    list.innerHTML += html;
  });

  // UPDATE CARD
  document.getElementById("notifRendah").innerText = rendah;
  document.getElementById("notifSedang").innerText = sedang;
  document.getElementById("notifTinggi").innerText = tinggi;
  document.getElementById("totalNotif").innerText = aktivitas.length;
}

// ================== LAPORAN ==================
function tampilLaporan() {
  let aktivitas = JSON.parse(localStorage.getItem("aktivitas")) || [];
  let list = document.getElementById("laporanList");

  if (!list) return;

  list.innerHTML = "";

  let tinggi = 0,
    sedang = 0,
    rendah = 0,
    total = 0;

  aktivitas.forEach((d) => {
    total += d.skor;

    if (d.kategori === "Tinggi") tinggi++;
    else if (d.kategori === "Sedang") sedang++;
    else rendah++;

    let warna =
      d.kategori === "Tinggi"
        ? "status-tinggi"
        : d.kategori === "Sedang"
          ? "status-sedang"
          : "status-rendah";

    list.innerHTML += `
      <tr>
        <td>${d.nama}</td>
        <td>${d.k}</td>
        <td>${d.a}</td>
        <td>${d.t}</td>
        <td>${d.d}</td>
        <td>${d.skor.toFixed(1)}</td>
        <td class="${warna}">${d.kategori}</td>
      </tr>
    `;
  });

  // RINGKASAN
  document.getElementById("totalData").innerText = aktivitas.length;

  let avg = total / (aktivitas.length || 1);
  document.getElementById("avgSkor").innerText = avg.toFixed(1);

  document.getElementById("lapTinggi").innerText = tinggi;
  document.getElementById("lapRendah").innerText = rendah;

  // INSIGHT
  let insight = "Belum ada data";

  if (rendah > sedang && rendah > tinggi) {
    insight =
      "Mayoritas siswa memiliki motivasi rendah, perlu intervensi segera.";
  } else if (sedang > tinggi) {
    insight =
      "Sebagian besar siswa memiliki motivasi sedang, perlu peningkatan.";
  } else {
    insight = "Sebagian besar siswa memiliki motivasi tinggi.";
  }

  document.getElementById("lapInsight").innerText = insight;

  // REKOMENDASI
  let rekom = document.getElementById("lapRekom");
  rekom.innerHTML = "";

  if (rendah > 0) {
    rekom.innerHTML +=
      "<li>Lakukan konseling untuk siswa dengan motivasi rendah</li>";
  }

  if (sedang > 0) {
    rekom.innerHTML += "<li>Lakukan monitoring dan pendampingan belajar</li>";
  }

  if (tinggi > 0) {
    rekom.innerHTML += "<li>Berikan apresiasi untuk siswa berprestasi</li>";
  }
}

// ================== FILTER ==================
function filterData() {
  let keyword = document.getElementById("searchNama").value.toLowerCase();
  let kategori = document.getElementById("filterKategori").value;

  let aktivitas = JSON.parse(localStorage.getItem("aktivitas")) || [];
  let list = document.getElementById("laporanList");

  list.innerHTML = "";

  aktivitas
    .filter(
      (d) =>
        d.nama.toLowerCase().includes(keyword) &&
        (kategori === "" || d.kategori === kategori),
    )
    .forEach((d) => {
      let warna =
        d.kategori === "Tinggi"
          ? "status-tinggi"
          : d.kategori === "Sedang"
            ? "status-sedang"
            : "status-rendah";

      list.innerHTML += `
        <tr>
          <td>${d.nama}</td>
          <td>${d.k}</td>
          <td>${d.a}</td>
          <td>${d.t}</td>
          <td>${d.d}</td>
          <td>${d.skor.toFixed(1)}</td>
          <td class="${warna}">${d.kategori}</td>
        </tr>
      `;
    });
}
// ================== REKOMENDASI ==================
function tampilRekomendasi() {
  let aktivitas = JSON.parse(localStorage.getItem("aktivitas")) || [];
  let list = document.getElementById("rekomList");

  if (!list) return;

  list.innerHTML = "";

  let rendah = 0,
    sedang = 0,
    tinggi = 0;

  aktivitas.forEach((d) => {
    let rekom =
      d.kategori === "Rendah"
        ? "Konseling & Pendampingan Intensif"
        : d.kategori === "Sedang"
          ? "Monitoring & Motivasi Tambahan"
          : "Apresiasi & Pengembangan Prestasi";

    let warna =
      d.kategori === "Tinggi"
        ? "status-tinggi"
        : d.kategori === "Sedang"
          ? "status-sedang"
          : "status-rendah";

    if (d.kategori === "Rendah") rendah++;
    else if (d.kategori === "Sedang") sedang++;
    else tinggi++;

    list.innerHTML += `
      <tr>
        <td>${d.nama}</td>
        <td>${d.skor.toFixed(1)}</td>
        <td class="${warna}">${d.kategori}</td>
        <td>${rekom}</td>
      </tr>
    `;
  });

  // RINGKASAN
  document.getElementById("rekTotal").innerText = aktivitas.length;
  document.getElementById("rekRendah").innerText = rendah;
  document.getElementById("rekSedang").innerText = sedang;
  document.getElementById("rekTinggi").innerText = tinggi;

  // INSIGHT
  let insight = "Belum ada data";

  if (rendah > sedang && rendah > tinggi) {
    insight =
      "Sebagian besar siswa membutuhkan konseling dan perhatian khusus.";
  } else if (sedang > tinggi) {
    insight =
      "Mayoritas siswa berada pada tahap motivasi sedang, perlu peningkatan.";
  } else {
    insight =
      "Sebagian besar siswa memiliki motivasi tinggi, pertahankan strategi pembelajaran.";
  }

  document.getElementById("rekInsight").innerText = insight;

  // GLOBAL
  let global = document.getElementById("rekGlobal");
  global.innerHTML = "";

  if (rendah > 0) {
    global.innerHTML +=
      "<li>Lakukan konseling individu bagi siswa dengan motivasi rendah</li>";
  }

  if (sedang > 0) {
    global.innerHTML += "<li>Tingkatkan metode pembelajaran interaktif</li>";
  }

  if (tinggi > 0) {
    global.innerHTML += "<li>Berikan penghargaan kepada siswa berprestasi</li>";
  }
}
// ================== MOTIVASI VIEW ==================
function tampilMotivasi() {
  let aktivitas = JSON.parse(localStorage.getItem("aktivitas")) || [];
  let list = document.getElementById("motivasiList");

  if (!list) return;

  list.innerHTML = "";

  let tinggi = 0,
    sedang = 0,
    rendah = 0,
    total = 0;

  aktivitas.forEach((d) => {
    total += d.skor;

    let status = "";
    let rekom = "";

    if (d.kategori === "Tinggi") {
      tinggi++;
      status = "Sangat Baik";
      rekom = "Apresiasi";
    } else if (d.kategori === "Sedang") {
      sedang++;
      status = "Cukup";
      rekom = "Monitoring";
    } else {
      rendah++;
      status = "Perlu Perhatian";
      rekom = "Konseling";
    }

    let warna =
      d.kategori === "Tinggi"
        ? "status-tinggi"
        : d.kategori === "Sedang"
          ? "status-sedang"
          : "status-rendah";

    list.innerHTML += `
      <tr>
        <td>${d.nama}</td>
        <td>${d.skor.toFixed(1)}</td>
        <td class="${warna}">${d.kategori}</td>
        <td>${status}</td>
        <td>${rekom}</td>
      </tr>
    `;
  });

  // ================= CARD =================
  let tinggiEl = document.getElementById("tinggiCount");
  let sedangEl = document.getElementById("sedangCount");
  let rendahEl = document.getElementById("rendahCount");
  let avgEl = document.getElementById("avgMotivasi");

  if (tinggiEl) tinggiEl.innerText = tinggi;
  if (sedangEl) sedangEl.innerText = sedang;
  if (rendahEl) rendahEl.innerText = rendah;

  let avg = total / (aktivitas.length || 1);
  if (avgEl) avgEl.innerText = avg.toFixed(1);

  // ================= INSIGHT =================
  let insight = "Belum ada data";

  if (aktivitas.length > 0) {
    if (rendah > sedang && rendah > tinggi) {
      insight =
        "Sebagian besar siswa memiliki motivasi rendah, perlu intervensi segera.";
    } else if (sedang > tinggi) {
      insight =
        "Sebagian besar siswa memiliki motivasi sedang, perlu peningkatan.";
    } else {
      insight = "Sebagian besar siswa memiliki motivasi tinggi, pertahankan.";
    }
  }

  let insightEl = document.getElementById("insightText");
  if (insightEl) insightEl.innerText = insight;

  // ================= RANKING =================
  let ranking = document.getElementById("rankingList");
  if (!ranking) return;

  ranking.innerHTML = "";

  let sorted = [...aktivitas].sort((a, b) => b.skor - a.skor);

  sorted.forEach((d) => {
    ranking.innerHTML += `<li>${d.nama} (${d.skor.toFixed(1)})</li>`;
  });
}
window.onload = function () {
  if (document.getElementById("listSiswa")) tampilSiswa();
  if (document.getElementById("aktivitasList")) tampilAktivitas();
  if (document.getElementById("motivasiList")) tampilMotivasi();
  if (document.getElementById("notifList")) tampilNotifikasi();
  if (document.getElementById("laporanList")) tampilLaporan();
  if (document.getElementById("rekomList")) tampilRekomendasi();
};
