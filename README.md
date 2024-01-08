## Overview
This is a face detection system that can be used to mark the attendance of candidates, whose images are pre-fed to the system. It works by detecting the current face from the webcam and matching it with the candidate's images.

## Algorithm
1. Store the candidate images in a storage bucket, and feed the candidate data to the realtime Firebase database.
2. Detect face/faces from the current image and try to match it with the storage images. (using OpenCV and cvzone)
3. On successful detection, update the attendance and attendance timestamp.
4. Get ready for detection again, after a cooldown period.

## Tools used
![python (1) (1)](https://github.com/codecruisedor/FaceDetectionAttendance/assets/25024714/5308cb35-382e-4941-986d-eb565083ccb0) ![189716855-2c69ca7a-5149-4647-936d-780610911353 (1)](https://github.com/codecruisedor/FaceDetectionAttendance/assets/25024714/af34b108-f19f-413d-977c-1421fc288e72)![192108372-f71d70ac-7ae6-4c0d-8395-51d8870c2ef0 (3)](https://github.com/codecruisedor/FaceDetectionAttendance/assets/25024714/e03467b1-56cc-47be-97a9-739953e7eb52)





