import cv2
import face_recognition
import pickle
import datetime
import os

print("Loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

print("Starting camera...")
video = cv2.VideoCapture(0)

marked_names = set()

def mark_attendance(name):
    if name not in marked_names:
        now = datetime.datetime.now()
        time_string = now.strftime("%Y-%m-%d %H:%M:%S")

        file_exists = os.path.isfile("attendance.csv")

        with open("attendance.csv", "a") as f:
            if not file_exists:
                f.write("Name,Time\n")
            f.write(f"{name},{time_string}\n")

        marked_names.add(name)
        print(f"Attendance marked for {name}")


while True:
    ret, frame = video.read()
    
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, box in zip(encodings, boxes):
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for i, b in enumerate(matches) if b]
            counts = {}

            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            mark_attendance(name)

        top, right, bottom, left = box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
