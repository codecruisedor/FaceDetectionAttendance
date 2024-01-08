import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://facerecognitionattendace-default-rtdb.firebaseio.com/",
    "storageBucket" : "facerecognitionattendace.appspot.com"
})

ref = db.reference('Students')