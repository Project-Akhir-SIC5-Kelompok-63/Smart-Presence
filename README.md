
# Smart Air Presence System (S.M.A.R.T)

Sistem presensi berbasis face recognition yang terintegrasi dengan kontrol suhu AC menggunakan esp32
## Features

- Presensi menggunakan face recognition
- Kontrol suhu Otomatis berdasarkan orang yang presensi 
- Monitoring suhu real-time


## Tech Stack

**Client:** Streamlit

**Server:** Flask


## Run Locally

Clone the project

```bash
  git clone https://github.com/Project-Akhir-SIC5-Kelompok-63/Smart-Presence.git
```

Go to the project directory

```bash
  cd smart-Presence
```

Install libary
```bash
pip install -r requirements.txt
```

Running file save_encoding.py
```bash
  py save_encoding.py
```

Start the server
```bash
  py run_servers.py
```

## Appendix
nb :
- disarankan menggunakan virtual environment
- untuk menambahkan datasets bisa langsung taruh gambar di folder "datasets" yang sudah disediakan
- jangan lupa ganti ip address pada file temp_check.ino
