import streamlit as st
import cv2
import face_recognition
import pickle
import numpy as np
import pandas as pd
import mysql.connector
import requests
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Fungsi untuk menghubungkan ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_presence"
    )

# Fungsi untuk mendapatkan data presensi dari database
def fetch_presence(room_id):
    db = connect_db()
    cursor = db.cursor()
    query = """
    SELECT u.name, u.face_id, a.timestamp FROM users u 
    JOIN attendance a ON u.id = a.user_id 
    JOIN rooms r ON r.id = a.room_id WHERE a.room_id = %s
    """
    cursor.execute(query, (room_id,))
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
    SELECT rc.temperature, rc.setting_ac_temp, rc.recorded_at, r.name 
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
        st.header("Face Recognition App")
        
        # select room
        rooms = fetch_rooms()
        room_options = {room[1]: room[0] for room in rooms}
        selected_room = st.selectbox("Pilih Kelas", list(room_options.keys()), key= "room_tab1")
        
        # Load the encodings and names from the file
        with open('face_encodings.pkl', 'rb') as f:
            known_faces = pickle.load(f)
            known_face_encodings = [face[0] for face in known_faces]
            known_face_names = [face[1] for face in known_faces]
            known_face_ids = [face[2] for face in known_faces]

        # Set up face recognition
        run = st.checkbox('Run')

        FRAME_WINDOW = st.image([])
        video_capture = cv2.VideoCapture(0)

        while run:
            ret, frame = video_capture.read()
            
            if not ret:
                st.error("Failed to capture video")
                break
            
            # Convert the frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown Person"
                face_id = None
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    face_id = known_face_ids[first_match_index]
                    
                if face_id:
                    try:
                        response = requests.post(f'http://{local_ip}:5000/insert_attendance_by_face', json={'face_id': face_id, 'room_id': room_options[selected_room]})
                        if response.status_code == 200:
                            response_json = response.json()
                            if 'user_id' in response_json:
                                user_id = response_json['user_id']
                                st.success(f"Terimakasih {name}!, anda sudah presensi pada kelas {selected_room}.")
                            elif 'message' in response_json:
                                st.info(response_json['message'])
                        else:
                            st.error("Failed to log attendance.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Request failed: {e}")

                cv2.rectangle(rgb_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(rgb_frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
            # Display the frame with correct color
            FRAME_WINDOW.image(rgb_frame)

        video_capture.release()
        cv2.destroyAllWindows()
    
    with tab2:
        st.header("Data Presensi")
        
        # select room
        rooms = fetch_rooms()
        room_options = {room[1]: room[0] for room in rooms}
        selected_room = st.selectbox("Pilih Kelas", list(room_options.keys()), key= "room_tab2")
        
        # Display presence data
        presence_data = fetch_presence(room_options[selected_room])
        presence_df = pd.DataFrame(presence_data, columns=["Nama Mahasiswa", "Face ID", "Waktu Presensi"])
        presence_df.index = range(1, len(presence_df) + 1)  # Reset index starting from 1
        st.dataframe(presence_df)
    
    with tab3:
        # Fetch and display room options
        rooms = fetch_rooms()
        room_options = {room[1]: room[0] for room in rooms}
        selected_room = st.selectbox("Pilih Kelas", list(room_options.keys()))

        # Initialize empty lists to store data
        temperature_data = []
        setting_temp = []
        time_data = []

        if st.button('Lihat Data Suhu'):
            room_id = room_options[selected_room]
            room_conditions = fetch_room_conditions(room_id)
            if room_conditions:
                for condition in room_conditions:
                    temperature_data.append(condition[0])
                    setting_temp.append(condition[1])
                    time_data.append(condition[2])

                current_temp = temperature_data[-1]

                col1, col2 = st.columns(2)
                col1.metric("Suhu Saat Ini", f"{current_temp:.2f} °C")
                col2.metric("Suhu Yang Diatur", f"{setting_temp[-1]:.2f} °C")

                # Temperature chart
                col1.line_chart(pd.DataFrame({
                    'Suhu (°C)': temperature_data,
                }, index=pd.to_datetime(time_data)))
                col2.line_chart(pd.DataFrame({
                    'Suhu (°C)': setting_temp,
                }, index=pd.to_datetime(time_data)))

                # Display temperature data in DataFrame
                st.header("Detail Data")
                df = pd.DataFrame({
                    'Suhu Yang Diatur (°C)': setting_temp,
                    'Suhu Asli (°C)': temperature_data,
                    'Waktu': pd.to_datetime(time_data)
                })
                df.index = range(1, len(df) + 1)
                st.dataframe(df)
            else:
                st.write("Tidak ada data suhu yang ditemukan untuk ruangan/kelas ini.")

if __name__ == '__main__':
    streamlit_app()
