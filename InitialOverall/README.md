# Smart Home Secuirity System
![smart Home secuirity System](k.jpg)

this system is implemented to increase security of a home and the cupboards those have valuable things.

## Features

when an unauthorised person is detetcted at outside of the maindoor,four main things happen,those are;
   1. alarm is rung
   2. the light at outsude of the maindoor is turned on
   3. a digital lock in the cupboards those have valuable things and a digital lock of main door ,are locked
   4. one picture of that unauthorised person is  send to app or website that is maked by us and send a notification to user whether unautherised person is detetcted.


## Project Components

1. data(face) collecting code
3. training model
4. face recognizing code
5. apk development

## Technologies and Hardware Utilized

1. rasberry pi 4B
2. pi camera 1 or web camera
3. buzzer
4. relay module 
5. digital locks(servo motors)
6. openCV--provides tools and functions essential for computer vision and machine learning tasks.
7. imutils-Python library containing a series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, and displaying Matplotlib images easier with OpenCV.It's a lightweight utility, not a full-fledged library like OpenCV
8. face_recognition library---built upon the dlib library's facial recognition technology
     1. face_locations---detect the bounding boxes of human faces in an image
     2. HOG-based model--feature descriptor that's particularly used in object detection(gradient(intensity change) based-Edges and textures in an image correspond to regions of high gradient magnitude,faster than CNN)
     3. face_encodings--computes a 128-dimension face embedding (or encoding) for each face.This embedding is a numerical representation of the facial features in a manner that allows the library to distinguish one face from another
     4. compare
  
9. react native,javascript lanuages
10. flask frameWork for backend

-------------------------------------------------------------------------------------------------------------------------------------------------------------

this system is implemented for local tasks at home(ringing alarm,light on and lock the doors) and remote tasks by user faraway from home.so it has to be a edge computing mechanism.(i.e when wifi is not in home ,local tasks happen.)
So;
for this system ,rasberrypi 4b board is used.(rasberrypi is poweruped by home current and when power cut occurs,ups powerup only rasberrypi and digital locks,alarm ) 

first rasberrypi board gets the images of the faces of each person in home by raspi 1 camera.to do this ,there should be a code for getting the face images.for code python,openCV are used.
then make a set of dataset with faces of persons of home.
then train a model of recognizing faces with above data set.

and make a website or app with buttons capable with on or off the maindoor light,alarm and unlock the maindoor.it is used for display the anuathorised faces those are detetcted at maindoor for user  far away from home.And he can see that face and identify whether that unauthorised person is a relative or cousin.if that person is relative or cousin ,user can unlock the door and off the alarm and the light at the maindoor from app by remotely accessing.




---------------------------------------

---data collecting for training----

This python code will let us take some photos of our faces using the Official Raspberry Pi Camera. See below the location of this file.(faceshots)

replace the name with family members

then it will be stored in dataset folder

This will then open up a little window and a terminal window which you can use to save images of your face. Press Spacebar Key to take a picture (take around 10) and then Q key to close the window. Provide the software different angles of your face so it can determine your dimensions better. 


----------------------------------
--training--

The pictures we took will be used by the Python code | train_model.py |. Any pictures in the dataset folder location will be analysed by this code when we run it. 


---------------------------------
--testing and recognition----
To run example code that will identify faces and if they find a face trained will write their name next to it. 


---gpio pins used to lock and and unlock doors and generate alarm and lights. 

# to do:
1. develop apk or web page l
2. backend for apk using frameworks like flask or fastApi 




