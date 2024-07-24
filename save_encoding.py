import os
import face_recognition
import pickle

# Initialize variables
known_face_encodings = []
known_face_names = []

# Load known faces and encode them
folder_path = "datasets"
print("Loading images from folder:", folder_path)
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
        image_path = os.path.join(folder_path, filename)
        face = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(face)
        if face_encodings:
            face_encoding = face_encodings[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

# Save the encodings and names to a file
with open('face_encodings.pkl', 'wb') as f:
    pickle.dump((known_face_encodings, known_face_names), f)

print("Encodings and names saved to face_encodings.pkl")
