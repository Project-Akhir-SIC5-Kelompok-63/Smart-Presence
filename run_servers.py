import subprocess
import socket

# Dapatkan IP address lokal
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Jalankan server Flask dengan IP address lokal
flask_process = subprocess.Popen(['flask', 'run', '-h', local_ip])

# Jalankan Streamlit
streamlit_process = subprocess.Popen(['streamlit', 'run', 'main.py'])

# Tunggu sampai kedua proses selesai
flask_process.wait()
streamlit_process.wait()