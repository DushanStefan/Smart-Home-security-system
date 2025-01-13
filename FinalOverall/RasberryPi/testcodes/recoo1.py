#! /usr/bin/python

# Import the necessary packages
import face_recognition
import imutils
import pickle
import cv2
from imutils.video import FPS

import RPi.GPIO as GPIO
# from time import sleep



import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import credentials, storage
# import msvcrt  # Windows-specific library for keyboard input
import threading
import time



# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your actual file name
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://realtimeexpo-682c7-default-rtdb.asia-southeast1.firebasedatabase.app',
    'storageBucket': 'realtimeexpo-682c7.appspot.com'
})

ref = db.reference('/light')  # Reference to the database signal path
ref1 = db.reference('/lock') 
ref2 = db.reference('/photolink') 

bucket = storage.bucket()
fb_folder_timestamp = time.strftime("%Y-%m-%d@%H-%M-%S", time.localtime(time.time()))
fb_folder_name =f"images_{fb_folder_timestamp}"
fb_folder_path = f"images_{fb_folder_timestamp}/raw_images/"


GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(19,GPIO.OUT) #check 19?



# Function to capture an image from the webcam
def capture_image(frame):
    current_time = time.strftime("%H_%M_%S", time.localtime(time.time()))
    image_name = f"image_{current_time}.jpg"
    # Use OpenCV to capture an image from the webcam
    # camera = cv2.VideoCapture(0)  # Use 0 for the default webcam
    # ret, frame = camera.read()
    
    cv2.imwrite(image_name, frame)
    print("Image captured:", image_name)
    upload_image(image_name)
    print("Image uploaded:", image_name)
    
    

photo_upload_link=None
# Function to upload an image to Firebase Storage
def upload_image(file_name):
    global photo_upload_link

    blob = bucket.blob(f"{fb_folder_path}{file_name}")
    try:
        blob.upload_from_filename(file_name)
        print("Image uploaded to Firebase:", blob.public_url)
        photo_upload_link = blob.public_url
    except Exception as e:
        print("Error uploading image:", e)



Event = threading.Event()  # Event to signal when 'go' is received from the database

def listen_for_signal():    
    while True:
        if ref.get() == 'off':
            #light off alarm-off
            ref2.set(None)
            time.sleep(1) 
            if ref1.get() == 'unlock':
                # unlock
                GPIO.output(19,False)
                ref1.set('lock')
            ref.set('on')        
            print("Wake up main thread")
            Event.set()
            time.sleep(1)  # To ensure main_thread.set() is not executed repeatedly
            Event.clear()  # Resetting the event for future signals

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
# fps = FPS().start()

# Process each frame of the video
while cap.isOpened():
    if not Event.is_set():
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
                    GPIO.output(27,True)#green light
                if name == "Unknown":
                    print("Paused... Waiting for database signal.")
                    #light alrm photo_upload
                    GPIO.output(17,True)
                    capture_image(frame)
                    ref2.get() == photo_upload_link            
                    Event.wait()  #Wait for the signal from the database
                    print("Database signaled 'go'.Resuming...")
                    print('green light on')
                    GPIO.output(27,True)#green lights
                    time.sleep(100)
                    #grenn light off
                    print('green light off')
                    GPIO.output(27,False)#green lights
                    
                    
                    
                    

            names.append(name)
            if name == "Unknown":
                    print("Paused... Waiting for database signal.")
                    #light alrm photo_upload
                    GPIO.output(17,True)
                    capture_image(frame)
                    ref2.get() == photo_upload_link            
                    Event.wait()  #Wait for the signal from the database
                    print("Database signaled 'go'.Resuming...")
                    print('green light on')
                    GPIO.output(27,True)#green lights
                    time.sleep(100)
                    #grenn light off
                    print('green light off')
                    GPIO.output(27,False)#green lights

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

    # fps.update()

# Display FPS information
# fps.stop()
# print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Cleanup
cv2.destroyAllWindows()
cap.release()
GPIO.output(17,False)
GPIO.output(27,False)
