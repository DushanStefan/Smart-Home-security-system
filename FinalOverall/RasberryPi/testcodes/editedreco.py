#! /usr/bin/python

# Import the necessary packages
import face_recognition
import imutils
import pickle
import cv2
from imutils.video import FPS

import RPi.GPIO as GPIO
from time import sleep

import firebase_admin
from firebase_admin import credentials, db
import threading



# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your actual file name
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://realtimeexpo-682c7-default-rtdb.asia-southeast1.firebasedatabase.app'
})

ref_light = db.reference('/light')  # Reference to the database signal path
ref_lock = db.reference('/lock')


Event = threading.Event()


GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)




def listen_for_signal():    
    while True:
        if ref_light.get() == 'off':
            #light off alarm-off     
            print("Wake up main thread")
            Event.set()

            Event.clear()  # Resetting the event for future signals
        else:
            print('gthy')


# Start a separate thread to listen for the database signal
signal_thread = threading.Thread(target=listen_for_signal)
signal_thread.start()



# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
encodingsP = "encodings.pickle"

print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# Load the video
input_video_path = '/home/pi/Desktop/wert/mandanaV.mp4'
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()

# Start the FPS counter
fps = FPS().start()

# Process each frame of the video
while cap.isOpened():
    ret, frame = cap.read()
    
    # Break if the video has ended
    if not ret:
        break

    frame = imutils.resize(frame, width=500)
    
    # Detect face boxes
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    # Loop over the facial embeddings
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        # Check to see if we have found a match
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            if currentname != name:
                currentname = name
                print(currentname)
                
            if name != "Unknown":
                GPIO.output(27,True)
            if name == "Unknown":
                print("green")
                GPIO.output(17,True)
                print("event waited 1")
                print(Event.is_set())
                Event.wait()
                
                

        names.append(name)
        if name == "Unknown":
            GPIO.output(17,True)
            print("event waited 2")
            print(Event.is_set())
            Event.wait()

    # Loop over the recognized faces and draw on the frame
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    # Quit when 'q' key is pressed
    if key == ord("q"):
        
        break

    fps.update()

# Display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Cleanup
cv2.destroyAllWindows()
cap.release()
GPIO.output(17,False)
GPIO.output(27,False)