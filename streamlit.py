import streamlit as st
import pandas as pd
import mysql.connector

# Fungsi untuk menghubungkan ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_presence"
    )

# Fungsi untuk mendapatkan data presensi dari database
def fetch_presence():
    db = connect_db()
    cursor = db.cursor()
    query = """
    SELECT m.nama_mhs, m.foto, p.waktu 
    FROM mahasiswa m
    JOIN presensi p ON m.id_mhs = p.id_mhs
    GROUP BY m.id_mhs
    """
    cursor.execute(query)
    presence = cursor.fetchall()
    cursor.close()
    db.close()
    return presence

# Fungsi untuk mendapatkan daftar ruangan dari database
def fetch_rooms():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT id_ruangan FROM temp_control")
    rooms = cursor.fetchall()
    cursor.close()
    db.close()
    return rooms

# Fungsi untuk mendapatkan data suhu dari tabel temp_control berdasarkan ruangan yang dipilih
def fetch_temperature_data(room_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT current_temp FROM temp_control WHERE id_ruangan = %s", (room_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return [result[0] for result in results]

def streamlit_app():
    # Set page config
    st.set_page_config(
        page_title="Dasbor Pemantauan Presensi dan Suhu Ruangan",
        page_icon="🌡️",
        layout="wide",
    )

    # Title and description
    st.title("Dasbor Pemantauan Presensi dan Suhu Ruangan")
    st.markdown("""
         Dasbor ini didukung oleh Streamlit dan Flask. Data dikumpulkan secara real-time dari perangkat ESP32 
            yang dilengkapi dengan sensor DHT22 dan ditampilkan di sini untuk tujuan pemantauan absensi biometrik pengenalan wajah.
    """)

    # Fetch and display room options
    rooms = fetch_rooms()
    room_options = {f"Kelas {room[0]}": room[0] for room in rooms}
    selected_room = st.selectbox("Pilih Kelas", list(room_options.keys()))

    # Initialize empty lists to store data
    temperature_data = []

    if st.button('Lihat Data Suhu'):
        room_id = room_options[selected_room]
        temperature_data = fetch_temperature_data(room_id)
        if temperature_data:
            avg_temp = sum(temperature_data) / len(temperature_data)
            current_temp = temperature_data[-1]

            col1, col2, col3 = st.columns(3)
            col1.metric("Suhu Saat Ini", f"{current_temp:.2f} °C")
            col2.metric("Rata-Rata Suhu", f"{avg_temp:.2f} °C")

            # Temperature chart
            st.line_chart(pd.DataFrame({
                'Suhu (°C)': temperature_data
            }, index=range(1, len(temperature_data) + 1)))

            # Display temperature data in DataFrame
            st.header("Detail Data")
            df = pd.DataFrame({
                'Waktu': range(1, len(temperature_data) + 1),
                'Suhu (°C)': temperature_data
            })
            st.dataframe(df)
        else:
            st.write("Tidak ada data suhu yang ditemukan untuk ruangan/kelas ini.")

   # Display presence data
    st.header("Data Presensi")
    presence_data = fetch_presence()
    presence_df = pd.DataFrame(presence_data, columns=["Nama Mahasiswa", "Foto", "Waktu Presensi"])
    presence_df.index = range(1, len(presence_df) + 1)  # Reset index starting from 1
    st.dataframe(presence_df)
            
if __name__ == '__main__':
    streamlit_app()
