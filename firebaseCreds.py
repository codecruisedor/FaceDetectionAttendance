import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "FirebaseURL",
    "storageBucket" : "bucketURI"
})

ref = db.reference('Students')
