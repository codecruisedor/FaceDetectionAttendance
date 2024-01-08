import os
import pickle
from datetime import datetime

import numpy as np
import cvzone
import cv2
import face_recognition
from firebase_admin import db, storage

import firebaseCreds

bucket = storage.bucket()
modeType = 0
counter = 0
idOfMatchedStudent = -1

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

Folderpath = 'Resources/Modes'
modeList = os.listdir(Folderpath)
imageList = []
imgstudent = []
for img in modeList:
    imageList.append(cv2.imread(os.path.join(Folderpath,img)))

#print(len(imageList))


file = open('EncodeFile.p','rb')
encodeListwithIds = pickle.load(file)
file.close()
encodeList, studentIds = encodeListwithIds
print(studentIds)

imageBack = cv2.imread("Resources/background.png")
while True:
    success,img = cap.read()

    imgS = cv2.resize(img, (0,0),None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)


    imageBack[162:162+480,55:55+640] = img
    imageBack[44:44+633,808:808+414] = imageList[modeType]


    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeList, encodeFace)
        faceDistance = face_recognition.face_distance(encodeList, encodeFace)
        # print("matches",matches)
        # print("distance",faceDistance)
        matchIndex = np.argmin(faceDistance)
        if matches[matchIndex]:
            y1,x2,y2,x1 = faceLoc
            bbox = 55+x1*4, 162+y1*4, x2*4-x1*4, y2*4-y1*4
            imageBack = cvzone.cornerRect(imageBack,bbox,rt=0)
            idOfMatchedStudent = studentIds[matchIndex]

            if counter == 0:
                counter = 1
                modeType = 1

    if counter!=0 :
        if counter == 1:
            studentInfo = db.reference(f'Students/{idOfMatchedStudent}').get()
            print(studentInfo)
            #get the image from storage
            blob = bucket.get_blob(f'Images/{idOfMatchedStudent}.jpg')
            blob2 = bucket.get_blob(f'Images/{idOfMatchedStudent}.png')
            # if bucket is None:
            #     print("Its none")
            notnoneblob = blob if blob is not None else blob2
            array = np.frombuffer(notnoneblob.download_as_string(), np.uint8)
            imgstudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            ref = db.reference(f'Students/{idOfMatchedStudent}')
            date_time_obj = datetime.strptime(studentInfo['last_attended_time'],'%Y-%m-%d %H:%M:%S')
            secondsElapsed = (datetime.now() - date_time_obj).total_seconds()
            print(secondsElapsed)
            if secondsElapsed > 30:
                studentInfo['total_attendance']+=1
                studentInfo['last_attended_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attended_time').set(studentInfo['last_attended_time'])
            else:
                modeType = 3
                counter = 0
                imageBack[44:44 + 633, 808:808 + 414] = imageList[modeType]

        if modeType!=3:
            if 10<counter<20:
                modeType = 2

            imageBack[44:44 + 633, 808:808 + 414] = imageList[modeType]

            if counter <= 10:
                cv2.putText(imageBack,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                # cv2.putText(imageBack, str(studentInfo['name']), (808, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                #             (0,0,0), 1)
                cv2.putText(imageBack, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0,0,0), 1)
                cv2.putText(imageBack, str(idOfMatchedStudent), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0,0,0), 1)
                cv2.putText(imageBack, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0,0,0), 1)
                cv2.putText(imageBack, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0,0,0), 1)
                cv2.putText(imageBack, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0,0,0), 1)

                (w,h),_ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                offset = (414 - w)//2
                cv2.putText(imageBack, str(studentInfo['name']), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 0), 1)
                #print(imageBack.shape," ",imgstudent.shape)
                imageBack[175:175+216,909:909+216] = imgstudent
            counter+=1

            if counter > 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgstudent = []
                imageBack[44:44+633,808:808+414] = imageList[modeType]


    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance",imageBack)
    cv2.waitKey(1)



