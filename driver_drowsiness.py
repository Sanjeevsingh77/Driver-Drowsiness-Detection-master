#Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np

#Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

#Initializing the face detector using OpenCV's Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

#status marking for current state
sleep = 0
drowsy = 0
active = 0
status=""
color=(0,0,0)

def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def detect_drowsiness(frame):
	"""Simplified drowsiness detection using eye detection"""
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	
	if len(faces) == 0:
		return "No Face Detected", (0, 0, 255)
	
	# Get the first (largest) face
	(x, y, w, h) = faces[0]
	roi_gray = gray[y:y+h, x:x+w]
	roi_color = frame[y:y+h, x:x+w]
	
	# Draw rectangle around face
	cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
	# Detect eyes
	eyes = eye_cascade.detectMultiScale(roi_gray)
	
	eye_closed = 0
	for (ex, ey, ew, eh) in eyes:
		# Calculate brightness in eye region to detect if eyes are closed
		eye_region = roi_gray[ey:ey+eh, ex:ex+ew]
		average_brightness = np.mean(eye_region)
		
		cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
		
		# If eyes are very dark, they might be closed
		if average_brightness < 50:
			eye_closed += 1
	
	# Simple drowsiness detection based on eyes
	if len(eyes) < 2:
		return "Drowsy !", (0, 0, 255)
	elif eye_closed >= 1:
		return "SLEEPING !!!", (255, 0, 0)
	else:
		return "Active :)", (0, 255, 0)

def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)

	#Checking if it is blinked
	if(ratio>0.25):
		return 2
	elif(ratio>0.21 and ratio<=0.25):
		return 1
	else:
		return 0


while True:
    _, frame = cap.read()
    
    if frame is None:
        print("Failed to read frame from camera")
        break
    
    status, color = detect_drowsiness(frame)
    cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    
    cv2.imshow("Driver Drowsiness Detection", frame)
    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()