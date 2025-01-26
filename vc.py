import speech_recognition as sr
import os
import gtts
from playsound import playsound
import time
import serial

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
        tts = gtts.gTTS("Hi. I am Assist Bot. How can I help you?")
        tts.save("hello.mp3")
        playsound("hello.mp3")
        print("Recording audio for 15 seconds...")
        recorded_audio = recognizer.listen(source, timeout = 15)
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
    if 'forward' in text:
        print("User said forward.")
        ser.write(b'1')
        ser1.write(b'1')
    if 'backward' in text:
        print("User said backward.")
        ser.write(b'2')
        ser1.write(b'2')
    if 'right' in text:
        print("User said right.")
        ser.write(b'5')
        ser1.write(b'5')
    if 'stop' in text:
        print("User said stop.")
        ser.write(b'3')
        ser1.write(b'3')

except sr.UnknownValueError:
    print("Google Speech Recognition couldn't understand the audio.")
except sr.RequestError:
    print("Couldn't request results from Google Speech Recognition service.")
except Exception as ex:
    print("Error during recognition: ", ex)
