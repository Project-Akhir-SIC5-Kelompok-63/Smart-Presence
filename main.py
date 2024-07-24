import streamlit as st
import cv2
import face_recognition
import pickle
import numpy as np
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
    SELECT u.name, u.face_id, a.timestamp 
    FROM users u
    JOIN attendance a ON u.id = a.user_id
    GROUP BY u.id, a.timestamp
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
    cursor.execute("SELECT id, name FROM rooms")
    rooms = cursor.fetchall()
    cursor.close()
    db.close()
    return rooms

# Fungsi untuk mendapatkan data suhu dari tabel room_conditions berdasarkan ruangan yang dipilih
def fetch_room_conditions(room_id):
    db = connect_db()
    cursor = db.cursor()
    query = """
    SELECT rc.temperature, rc.humidity, rc.recorded_at, r.name 
    FROM room_conditions rc
    JOIN rooms r ON rc.room_id = r.id
    WHERE rc.room_id = %s
    """
    cursor.execute(query, (room_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def streamlit_app():
    # Set page config
    st.set_page_config(
        page_title="Dasbor Pemantauan Presensi dan Suhu Ruangan",
        page_icon="🌡️",
        layout="wide",
    )
    # Title and description
    st.title("Website Pemantauan Presensi dan Suhu Ruangan")
    st.markdown("""
            Website ini didukung oleh Streamlit dan Flask. Data dikumpulkan secara real-time dari perangkat ESP32 
                yang dilengkapi dengan sensor DHT11 dan ditampilkan di sini untuk tujuan pemantauan absensi biometrik pengenalan wajah.
        """)
    
    # Set page tabs
    tab1, tab2, tab3 = st.tabs(["Presensi Face-Recognition","Pemantauan Presensi", "Pemantauan Suhu"])
    
    with tab1:
        # Load the encodings and names from the file
        with open('face_encodings.pkl', 'rb') as f:
            known_face_encodings, known_face_names = pickle.load(f)

        # Set up Streamlit
        st.title("Face Recognition App")
        run = st.checkbox('Run')

        FRAME_WINDOW = st.image([])
        video_capture = cv2.VideoCapture(0)

        while run:
            ret, frame = video_capture.read()
            
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown Person"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
            FRAME_WINDOW.image(frame)

        video_capture.release()
        cv2.destroyAllWindows()
    
    with tab2:
        # Display presence data
        st.header("Data Presensi")
        presence_data = fetch_presence()
        presence_df = pd.DataFrame(presence_data, columns=["Nama Mahasiswa", "Foto", "Waktu Presensi"])
        presence_df.index = range(1, len(presence_df) + 1)  # Reset index starting from 1
        st.dataframe(presence_df)
    
    with tab3:
        # Fetch and display room options
        rooms = fetch_rooms()
        room_options = {room[1]: room[0] for room in rooms}
        selected_room = st.selectbox("Pilih Kelas", list(room_options.keys()))

        # Initialize empty lists to store data
        temperature_data = []
        humidity_data = []
        time_data = []
        room_names = []

        if st.button('Lihat Data Suhu'):
            room_id = room_options[selected_room]
            room_conditions = fetch_room_conditions(room_id)
            if room_conditions:
                for condition in room_conditions:
                    temperature_data.append(condition[0])
                    humidity_data.append(condition[1])
                    time_data.append(condition[2])
                    room_names.append(condition[3])

                current_temp = temperature_data[-1]
                current_humidity = humidity_data[-1]

                col1, col2 = st.columns(2)
                col1.metric("Suhu Saat Ini", f"{current_temp:.2f} °C")
                col2.metric("Kelembaban Saat Ini", f"{current_humidity:.2f} %")

                # Temperature and Humidity chart
                st.line_chart(pd.DataFrame({
                    'Suhu (°C)': temperature_data,
                    'Kelembaban (%)': humidity_data
                }, index=pd.to_datetime(time_data)))

                # Display temperature data in DataFrame
                st.header("Detail Data")
                df = pd.DataFrame({
                    'Ruangan': room_names,
                    'Suhu (°C)': temperature_data,
                    'Kelembaban (%)': humidity_data,
                    'Waktu': pd.to_datetime(time_data)
                })
                df.index = range(1, len(df) + 1)
                st.dataframe(df)
            else:
                st.write("Tidak ada data suhu yang ditemukan untuk ruangan/kelas ini.")

if __name__ == '__main__':
    streamlit_app()
