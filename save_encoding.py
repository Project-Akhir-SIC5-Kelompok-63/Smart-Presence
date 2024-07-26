import os
import face_recognition
import pickle
import uuid
import mysql.connector
from datetime import datetime

# initialize database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="smart_presence"
)
cursor = conn.cursor()

# Initialize variables
known_faces = []

# Load known faces and encode them
folder_path = "datasets"
print("Loading images from folder:", folder_path)
for filename in os.listdir(folder_path):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(folder_path, filename)
        face = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(face)
        if face_encodings:
            face_encoding = face_encodings[0]
            face_name = os.path.splitext(filename)[0]
            face_id = str(uuid.uuid4())  # Generate a unique identifier
            known_faces.append((face_encoding, face_name, face_id))

# Save the encodings and names to a file
with open('face_encodings.pkl', 'wb') as f:
    pickle.dump(known_faces, f)

print("Encodings and names saved to face_encodings.pkl")

created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for face_encoding, face_name, face_id in known_faces:
    cursor.execute("INSERT INTO users VALUES (null, %s, %s, %s, %s)", (face_name, face_id, created_at, created_at))

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Names and UUIDs have been saved to the database.")