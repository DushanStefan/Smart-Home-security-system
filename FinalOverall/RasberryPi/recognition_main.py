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
from firebase_admin import credentials, storage
import threading
import time
import datetime




# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your actual file name
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://realtimeexpo-682c7-default-rtdb.asia-southeast1.firebasedatabase.app',
    'storageBucket': 'realtimeexpo-682c7.appspot.com'
    
})

ref_light = db.reference('/light')  # Reference to the database signal path
ref_lock = db.reference('/lock')
ref_authority = db.reference('/authorization/authority')
ref_imageLink = db.reference('/authorization/imageLink')
bucket = storage.bucket()

Event = threading.Event()


servo_pin=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(servo_pin,GPIO.OUT)

pwm=GPIO.PWM(servo_pin,50)#50 HZ

def set_angle(angle):
    duty_cycle=(angle/18)+2
    GPIO.output(servo_pin,True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo_pin,False)
    pwm.ChangeDutyCycle(0)

# kd=''

# Function to upload an image to Firebase Storage
def upload_image(file_name):
    
#     global kd
#     blob = bucket.blob(f"{fb_folder_path}{file_name}")
    blob = bucket.blob(f"{file_name}")
    try:
        blob.upload_from_filename(file_name)
        print("Image uploaded to Firebase:", blob.public_url)
#         kd=blob.public_url
    except Exception as e:
        print("Error uploading image:", e)





def listen_for_signal():    
    while True:
        time.sleep(1)
        if ref_light.get() == 'off' and ref_lock.get() != 'unlock':
            #light off alarm-off   
            ref_light.set('done')
            
            GPIO.output(17,False)
            print("Wake up main thread")
            GPIO.output(27,True)#green light on
            
            noIssue_output_path = f'good.png'
            
            ref_imageLink.set(noIssue_output_path)
            ref_authority.set('accepted2')
#             print("photo saved")
            #upload_image(noIssue_output_path)
#             print("photo uploaded")


            time.sleep(10)
            GPIO.output(27,False)#green off
            
            Event.set()
            Event.clear()  # Resetting the event for future signals
            ref_light.set('on')
        
        elif ref_light.get() == 'off' and ref_lock.get() == 'unlock':
            #light off alarm-off   
            ref_light.set('done')
            GPIO.output(17,False)  
            print("Wake up main thread")
            GPIO.output(27,True)#green light on
            
            noIssue_output_path = f'good.png'
            
            ref_imageLink.set(noIssue_output_path)
            ref_authority.set('accepted1')
#             print("photo saved")
            #upload_image(noIssue_output_path)
#             print("photo uploaded")
            
            #open the door-#implement lock details///////////////////////////////

            pwm.start(0)   
            set_angle(0)
            time.sleep(1)
            set_angle(180)
            time.sleep(1)
            pwm.stop()
            
            time.sleep(8)
            GPIO.output(27,False)#green off
            
            Event.set()
            Event.clear()  # Resetting the event for future signals
            ref_light.set('on')
            ref_lock.set('lock')
            
            
        else:
            print("light on else")
            
            
#         if key == ord("q"):
#             GPIO.output(17,False)
#             break


# Start a separate thread to listen for the database signal
signal_thread = threading.Thread(target=listen_for_signal)
signal_thread.start()



# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
encodingsP = "encodings.pickle"

print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# Load the video
input_video_path = '/home/pi/Desktop/gtyrty/trump.mp4'
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()

# Start the FPS counter
# fps = FPS().start()

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
                
                
                #open door
                set_angle(180)
                time.sleep(1)
                pwm.stop()
#                 print(green)
                GPIO.output(27,True)#green light on
                
                #open the door-#implement lock details///////////////////////////////
                pwm.start(0)   
                set_angle(0)
                time.sleep(1)
                set_angle(180)
                time.sleep(1)
                pwm.stop()
                
                k_output_path = name+'.png'
                #cv2.imwrite(k_output_path, frame)
                ref_imageLink.set(k_output_path)
                ref_authority.set(name)
                
                #upload_image(k_output_path)
                
                
                time.sleep(18)
                GPIO.output(27,False)#green off
                
            if name == "Unknown":
                print("ju")
                GPIO.output(17,True)
                print(Event.is_set())
                print("event waited 1")                
                Event.wait()
                
                

        names.append(name)
        if name == "Unknown":
            GPIO.output(17,True)

#             timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
#             output_path = f'unknownface_{timestamp}.jpg'
            output_path = f'ert.jpg'
            cv2.imwrite(output_path, frame)
            ref_imageLink.set(output_path)
            ref_authority.set("unknown")
            print("photo saved")
            upload_image(output_path)
            print("photo uploaded")

            
            print("light on")

            print(Event.is_set())
            print("event waited 2")
            
            Event.wait(15)

            print("back to main thread")
#             GPIO.output(27,True)#green light on
#             GPIO.output(17,False)
            #open the door(one nathi wei)
#             time.sleep(3)
#             GPIO.output(27,False)#green off

    # Loop over the recognized faces and draw on the frame
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF
    
    
    if len(boxes)==0:
        output_path = f'noIssue.png'
        #cv2.imwrite(output_path, frame)
        ref_imageLink.set(output_path)
        ref_authority.set('')
        
        
    
    

    # Quit when 'q' key is pressed
    if key == ord("q"):
        
        break


print("overall done")


# Cleanup
cv2.destroyAllWindows()
cap.release()
GPIO.output(17,False)
GPIO.output(27,False)

GPIO.cleanup()