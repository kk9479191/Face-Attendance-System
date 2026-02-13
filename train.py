import face_recognition
import os
import pickle

dataset_path = "dataset"
known_encodings = []
known_names = []

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]

        known_encodings.append(encoding)
        known_names.append(person_name)

data = {"encodings": known_encodings, "names": known_names}

with open("encodings.pickle", "wb") as f:
    pickle.dump(data, f)

print("Training Complete!")
