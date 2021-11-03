import cv2
import numpy as np
import face_recognition
import os
import datetime
import time

#import serial

# port = serial.Serial('COM4',9600)
import pyttsx3
engine = pyttsx3.init()
a=-1
matchIndex= -1
engine.setProperty("rate", 150)

path = 'Image Attendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for c1 in myList:
    curImg = cv2.imread(f'{path}/{c1}')
    images.append(curImg)
    classNames.append(os.path.splitext(c1)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
end_time = time.time() + 5
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS =cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    if (time.time() > end_time):
        matchIndex= -1

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):

        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)


        print(min(faceDis))

        if(min(faceDis)<0.55):
            matchIndex = np.argmin(faceDis)
           # print(matchIndex)
            end_time = time.time() + 5

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)


                currentTime = datetime.datetime.now()

                if currentTime.hour < 12:
                    greeting = 'good morning'
                elif 12 <= currentTime.hour < 18:
                    greeting = 'good afternoon'
                else:
                    greeting = 'good evening'

                if (a != matchIndex):
                    engine.say(greeting + name)
                    engine.runAndWait()

        else:
            name = ''
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    a = matchIndex


    cv2.imshow('Webcam',img)
    cv2.waitKey(1)

    data = matchIndex
    # bablu = matchIndex
    # rajiv = matchIndex

    # if (data == 0):
    #     port.write(str.encode('A'))
    # elif (data == 1):
    #     port.write(str.encode('B'))
    # elif(data==2):
    #     port.write(str.encode('C'))