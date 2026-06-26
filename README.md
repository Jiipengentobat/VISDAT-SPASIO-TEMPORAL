# 🌍 Visualisasi Sebaran Gempa Bumi Indonesia 2008-2023

**Mata Kuliah**: Visualisasi Data Spasio-Temporal  
**Topik**: Visualisasi Sebaran dan Tren Gempa Bumi Indonesia  
**Data**: KAGGLE Katalog Gempa (92,415 kejadian)  
**Periode**: November 2008 - Januari 2023  
**Teknologi**: HTML5 + Leaflet.js + Chart.js + Python ML

---

## 📋 Daftar Isi
1. [Ringkasan Proyek](#ringkasan-proyek)
2. [Struktur Folder](#struktur-folder)
3. [Instalasi & Setup](#instalasi--setup)
4. [Cara Menjalankan](#cara-menjalankan)
5. [Fitur Aplikasi](#fitur-aplikasi)
6. [Komponen Machine Learning](#komponen-machine-learning)
7. [Data & Analisis](#data--analisis)
8. [Luaran & Pengumpulan](#luaran--pengumpulan)

---

## 📚 Ringkasan Proyek

### Latar Belakang
Indonesia merupakan negara dengan tingkat seismisitas tertinggi di dunia, berada di jalur Cincin Api Pasifik (Ring of Fire). Gempa bumi merupakan fenomena spasio-temporal kompleks yang memiliki dimensi geografis (lokasi epicenter) dan temporal (waktu kejadian) yang dapat dianalisis untuk mengidentifikasi pola, tren, dan anomali.

### Tujuan
Proyek ini mengembangkan **aplikasi visualisasi interaktif berbasis web** yang memungkinkan eksplorasi pola spasio-temporal gempa bumi Indonesia serta mengintegrasikan teknik **machine learning untuk deteksi anomali** dalam aktivitas seismik.

### Capaian Pembelajaran
✓ Identifikasi dan akuisisi data spasio-temporal terbuka (BMKG Open Data)  
✓ Pra-pemrosesan dan feature engineering untuk data seismik  
✓ Perancangan & implementasi aplikasi visualisasi interaktif  
✓ Integrasi machine learning (Isolation Forest) untuk deteksi anomali  
✓ Pendokumentasian metodologi dalam format artikel ilmiah

---

## 📁 Struktur Folder

```
gempa-indonesia/
├── data/
│   ├── katalog_gempa_raw.csv          # Data mentah (92,887 records)
│   ├── katalog_gempa_clean.csv        # Data bersih hasil preprocessing
│   └── gempa_anomalies.csv            # Hasil deteksi anomali ML
│
├── web/
│   ├── index.html                     # Aplikasi web interaktif utama
│   └── data/
│       ├── earthquakes_sample.geojson # Sampel gempa untuk peta (GeoJSON)
│       ├── timeline.json              # Data timeline untuk grafik
│       ├── summary.json               # Statistik ringkasan
│       └── anomalies.geojson          # Top 10 anomali (GeoJSON)
│
├── analysis/
│   ├── 1_data_preprocessing.py        # Script pembersihan & feature engineering
│   ├── 2_anomaly_detection.py         # Script ML deteksi anomali
│   ├── 3_data_conversion.py           # Konversi ke format web (GeoJSON, JSON)
│   └── exploratory_analysis.ipynb     # Notebook analisis eksplorasi (opsional)
│
├── article/
│   ├── Gempa_Bumi_Indonesia_Article.docx
│   ├── Gempa_Bumi_Indonesia_Article.pdf
│   └── references.bib
│
└── README.md                           # File ini
```

---

## 🔧 Instalasi & Setup

### Persyaratan Sistem
- **Python 3.8+** (untuk preprocessing dan ML)
- **Browser modern** dengan JavaScript support (Chrome, Firefox, Edge)
- **Internet connection** (untuk CDN libraries: Leaflet, Chart.js)

### Step 1: Clone/Download Proyek
```bash
cd gempa-indonesia
```

### Step 2: Install Python Dependencies (Opsional, jika ingin regenerate data)
```bash
pip install pandas numpy scikit-learn scipy
```

### Step 3: Verifikasi Struktur Data
Pastikan file berikut ada di folder `web/data/`:
- `earthquakes_sample.geojson`
- `timeline.json`
- `summary.json`
- `anomalies.geojson`

Jika belum ada, jalankan script preprocessing:
```bash
cd analysis
python 1_data_preprocessing.py
python 2_anomaly_detection.py
python 3_data_conversion.py
cd ..
```

---

## ▶️ Cara Menjalankan

### Opsi 1: Browser Lokal (Recommended)
1. Buka terminal/command prompt
2. Navigate ke folder `web/`
```bash
cd web
```
3. Jalankan simple HTTP server:

**Windows (Python):**
```bash
python -m http.server 8000
```

**macOS/Linux (Python):**
```bash
python3 -m http.server 8000
```

**Alternatif dengan Node.js:**
```bash
npx http-server -p 8000
```

4. Buka browser dan akses:
```
http://localhost:8000
```

### Opsi 2: Buka File Langsung
- Double-click file `web/index.html` (Note: beberapa fitur mungkin terbatas)

### Opsi 3: Deploy Online
Untuk deployment, gunakan:
- **Vercel**: `vercel deploy`
- **Netlify**: Upload folder `web/`
- **GitHub Pages**: Push ke repository

---

## ✨ Fitur Aplikasi

### 1. Peta Interaktif
- **Base Map**: OpenStreetMap dengan zoom hingga level 19
- **Marker Clustering**: Otomatis cluster gempa untuk performance
- **Circle Markers**: Ukuran & warna berdasarkan magnitude
  - Blue: Minor (< 3)
  - Green: Light (3-4)
  - Orange: Moderate (4-5)
  - Red: Strong (5-6)
  - Dark Red: Major (≥ 6)

### 2. Kontrol Temporal
- **Year Slider**: Filter data hingga tahun tertentu (2008-2023)
- Peta otomatis update saat slider bergerak
- Menampilkan gempa yang terjadi dari 2008 hingga tahun yang dipilih

### 3. Layer Management
- **Gempa Bumi**: Toggle untuk menampilkan/menyembunyikan marker gempa
- **Anomali Seismik**: Tampilkan lokasi/periode dengan aktivitas abnormal
- **Heat Map** (future): Visualisasi kepadatan aktivitas

### 4. Popup Informatif
Klik marker gempa untuk melihat:
- Lokasi (nama wilayah)
- Magnitude
- Kedalaman (km)
- Tanggal & waktu kejadian

### 5. Grafik Timeline
- **Bar Chart**: Jumlah gempa per tahun (2008-2023)
- Update responsif terhadap perubahan data
- Bantuan visualisasi tren temporal

### 6. Ringkasan Statistik
- Total gempa
- Magnitude minimum, maksimum, rata-rata
- Kedalaman rata-rata
- Distributif magnitude & kedalaman

### 7. Legenda
- Penjelasan warna marker berdasarkan magnitude
- Referensi kategori:
  - Minor: < 3
  - Light: 3-4
  - Moderate: 4-5
  - Strong: 5-6
  - Major: ≥ 6

---

## 🤖 Komponen Machine Learning

### Algoritma: Isolation Forest + Z-Score

#### Metodologi
1. **Feature Engineering**: Agregasi data per grid cell & bulan
   - Event count (jumlah gempa)
   - Maximum magnitude
   - Mean magnitude
   - Mean depth

2. **Isolation Forest** (Unsupervised Anomaly Detection)
   - Contamination: 5% (expected anomalies)
   - Deteksi pola yang unusual dalam multi-dimensi
   - Output: Anomaly score (-1 hingga +1)

3. **Z-Score Validation**
   - Threshold: |Z| > 2 (95% confidence level)
   - Validasi hasil Isolation Forest
   - Kombinasi untuk robust anomaly detection

#### Interpretasi Hasil
Anomali terdeteksi pada:
- Periode dengan **magnitude tinggi** yang tidak biasa
- Lokasi dengan **aktivitas gempa meningkat drastis**
- Grid cells dengan **kombinasi unik** magnitude dan kedalaman

Contoh top anomalies:
```
1. Periode: 2020-08, Lokasi: Flores Sea
   - Magnitude Max: 6.7, Anomaly Score: -0.769
   
2. Periode: 2017-01, Lokasi: Sulawesi
   - Magnitude Max: 7.2, Anomaly Score: -0.769
```

---

## 📊 Data & Analisis

### Sumber Data
- **BMKG Open Data**: Katalog Gempa Bumi Indonesia
- **Format**: CSV (13 kolom)
- **Records**: 92,415 (setelah cleaning)
- **Periode**: November 2008 - Januari 2023 (14+ tahun)

### Cakupan Spasial
- **Latitude**: -11° hingga 7°
- **Longitude**: 95° hingga 141°
- **Area**: Seluruh kepulauan Indonesia

### Variabel Utama
| Variabel | Deskripsi |
|----------|-----------|
| `tgl` | Tanggal kejadian (YYYY-MM-DD) |
| `ot` | Origin time (waktu kejadian) |
| `lat` | Latitude epicenter |
| `lon` | Longitude epicenter |
| `depth` | Kedalaman hiposenter (km) |
| `mag` | Magnitude (Richter Scale) |
| `remark` | Nama wilayah/lokasi |
| `strike1, dip1, rake1` | Focal mechanism parameters |

### Preprocessing Steps
1. **Parsing**: Konversi datetime strings ke format standar
2. **Validation**: Verifikasi koordinat dalam bounds Indonesia
3. **Outlier removal**: Filter magnitude 0-10, kedalaman 0-700 km
4. **Feature engineering**: Kategori magnitude, kategori kedalaman, grid ID
5. **Temporal indexing**: Extract tahun, bulan, hari, jam

### Statistik Deskriptif
```
Total Gempa: 92,415
Magnitude:
  - Min: 1.0, Max: 7.9, Mean: 3.59, Median: 3.50
  - Minor (< 3): 23.5%
  - Light (3-4): 44.0%
  - Moderate (4-5): 27.0%
  - Strong (5-6): 5.0%
  - Major (≥ 6): 0.4%

Kedalaman:
  - Min: 2 km, Max: 700 km, Mean: 48.8 km
  - Shallow (< 70 km): 79.1%
  - Intermediate (70-300 km): 19.2%
  - Deep (> 300 km): 1.7%

Top Regions:
  1. Minahassa Peninsula - Sulawesi: 9,428 events
  2. Sulawesi - Indonesia: 7,893 events
  3. Sumbawa Region - Indonesia: 7,312 events
```

---

## 📄 Luaran & Pengumpulan

### Komponen Luaran
✅ **1. Aplikasi Visualisasi** (`web/index.html`)
- Peta interaktif dengan Leaflet.js
- Slider temporal (2008-2023)
- Chart timeline dengan Chart.js
- Layer management & popup informatif
- Deteksi anomali terintegrasi

✅ **2. Kode Sumber & Analisis**
- `analysis/1_data_preprocessing.py` - Pembersihan data
- `analysis/2_anomaly_detection.py` - ML implementation
- `analysis/3_data_conversion.py` - Format conversion
- `analysis/exploratory_analysis.ipynb` - Notebook eksplorasi

✅ **3. Dokumentasi Data**
- `data/katalog_gempa_clean.csv` - Data bersih
- `data/gempa_anomalies.csv` - Hasil ML
- Web JSON files: GeoJSON, timeline, summary, anomalies

✅ **4. Artikel Ilmiah**
- Format: 4,000-6,000 kata
- Struktur: Abstrak, Pendahuluan, Tinjauan Pustaka, Metodologi, Hasil & Pembahasan, Kesimpulan, Daftar Pustaka
- Minimal 15 referensi
- 3+ screenshot aplikasi
- Tersedia dalam format .docx & .pdf

✅ **5. Video Penjelasan**
- Durasi: Max 5 menit
- Konten: Demo aplikasi, penjelasan ML, interpretasi hasil
- Format: MP4, H.264 codec

✅ **6. README & Dokumentasi**
- File ini: Dokumentasi lengkap proyek
- Instruksi instalasi & menjalankan
- Penjelasan fitur & metodologi

---

## 🔍 Troubleshooting

### Data file tidak terload
**Solusi**:
1. Pastikan file ada di folder `web/data/`
2. Jalankan conversion scripts:
```bash
cd analysis
python3 1_data_preprocessing.py
python3 2_anomaly_detection.py
python3 3_data_conversion.py
```
3. Refresh browser (Ctrl+F5 untuk hard refresh)

### Browser error "CORS policy"
**Solusi**:
1. Jangan buka file langsung dengan double-click
2. Gunakan HTTP server (lihat section "Cara Menjalankan")
3. Pastikan tidak ada blocking dari antivirus/firewall

### Chart tidak muncul
**Solusi**:
1. Check console browser (F12 > Console)
2. Pastikan Chart.js CDN accessible (perlu internet)
3. Refresh halaman

### Peta kosong/marker tidak muncul
**Solusi**:
1. Tunggu hingga data selesai loading (cek console)
2. Klik tombol "Reset Peta"
3. Periksa browser console untuk error messages

---

## 📖 Referensi Singkat

### Publikasi & Dataset
- BMKG. (2024). *Katalog Gempa Bumi Indonesia*. Badan Meteorologi Klimatologi dan Geofisika.
- Lay, T., & Wallace, T. C. (1995). *Modern Global Seismology*. Academic Press.
- Bird, P. (2003). An updated digital model of plate boundaries. Geochemistry, Geophysics, Geosystems, 4(3).

### Tools & Libraries
- **Leaflet.js**: Interactive mapping library
- **Chart.js**: Data visualization
- **scikit-learn**: Machine learning
- **Pandas**: Data manipulation
- **GeoPandas**: Spatial data analysis

---

## 👤 Informasi Penulis
- **Mata Kuliah**: Visualisasi Data Spasio-Temporal
- **Semester**: [Your semester]
- **Tahun**: 2024

---

## 📝 License
Dataset BMKG digunakan untuk tujuan pendidikan dan penelitian. Aplikasi ini dibuat sebagai tugas akhir.

---

**Last Updated**: Januari 2024  
**Status**: ✅ Ready for Submission
