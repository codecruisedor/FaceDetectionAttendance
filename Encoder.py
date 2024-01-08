import cv2
import face_recognition
import pickle
import os
import firebaseCreds
from firebase_admin import storage


Folderpath = 'Images'
pathList = os.listdir(Folderpath)
imageList = []
studentIds = []
for img in pathList:
    imageList.append(cv2.imread(os.path.join(Folderpath,img)))
    studentIds.append(img[0 : len(img) - 4])

    fileName = f'{Folderpath}/{img}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding started..")
encodeListAll = findEncodings(imageList)
print("Encoding completed..")
encodeListAllWithIds = [encodeListAll,studentIds]
file = open("EncodeFile.p","wb")
pickle.dump(encodeListAllWithIds, file)
print(encodeListAll)
