#Import the necessary dependencies
import serial
import time
import face_recognition
import cv2
import numpy as np
import speech_recognition as sr
import os
import gtts
from playsound import playsound
from twilio.rest import Client

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
ser1 = serial.Serial("/dev/ttyACM1", 115200, timeout=1)
temp1=1

ser.setDTR(False)
ser1.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
ser1.flushInput()
ser1.setDTR(True)
time.sleep(5)

ser.write(b'1')
ser1.write(b'1')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
hiba_image = face_recognition.load_image_file("hiba.jpg")
hiba_face_encoding = face_recognition.face_encodings(hiba_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    hiba_face_encoding
    ]
known_face_names = [
    "Hiba "
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
print("Test")
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
    if name != "Unknown":
        break
        
        
process_this_frame = not process_this_frame

# Release handle to the webcam
video_capture.release()

account_sid = "AccountSID"
auth_token  = "AccountTKN"
client = Client(account_sid, auth_token)
recognizer = sr.Recognizer()
try:
    # List available microphones
    print("Available microphones:")
    print(sr.Microphone.list_microphone_names())

    # Select a specific microphone (optional)
    # with sr.Microphone(device_index = 1) as source:

    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration = 1)
        tts = gtts.gTTS("Hello "+ name +" Are you ok?")
        tts.save("hello.mp3")
        #sleep(5)
        playsound("hello.mp3")
        print("Recording audio for 15 seconds...")
        time.sleep(5)
        recorded_audio = recognizer.listen(source, 14, 10)
        print("Done recording.")

except sr.UnknownValueError:
    print("Google Speech Recognition couldn't understand the audio.")
except sr.RequestError:
    print("Couldn't request results from Google Speech Recognition service.")
except Exception as ex:
    print("Error during recognition: ", ex)
    
try:
    print("Recognizing the text..")
    text = recognizer.recognize_google(recorded_audio, language = "en-US")
    print("Decoded Text: {}".format(text))
    if 'yes' in text:
        tts = gtts.gTTS("Thats great!")
        tts.save("check.mp3")
        playsound("check.mp3")

        #If response is no, reply, Ok, I will call someone to come and check on you.
    if 'no' in text:
        tts = gtts.gTTS("Ok, I will call someone to come and check on you.")
        tts.save("check.mp3")
        playsound("check.mp3")
        call = client.calls.create(to="ANumber",
                        from_="YourNumber",
                        twiml='<Response><Say>Hello there. '+name+'    says that they are not okay. Please check on them.</Say></Response>')
        print(call.sid)
except sr.UnknownValueError:
    print("Google Speech Recognition couldn't understand the audio.")
except sr.RequestError:
    print("Couldn't request results from Google Speech Recognition service.")
except Exception as ex:
    print("Error during recognition: ", ex)
    
cv2.destroyAllWindows()
