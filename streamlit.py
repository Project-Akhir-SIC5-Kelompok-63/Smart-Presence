import streamlit as st
import cv2
import face_recognition
import pickle
import numpy as np

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
            print(name)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    FRAME_WINDOW.image(frame)

video_capture.release()
cv2.destroyAllWindows()