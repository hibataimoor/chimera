#Import the necessary dependencies
import pygame
import serial
import time

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
ser1 = serial.Serial("/dev/ttyACM1", 115200, timeout=1)
temp1=1

#Initialize the Joystick
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

ser.setDTR(False)
ser1.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
ser1.flushInput()
ser1.setDTR(True)
time.sleep(5)

print("Press: Asterisk/A for Forwards, Moon/B for Backwards, Triangular Arrow/Y for Stop, and Hourglass/X for Right.")
print("\n") 

counter = 1
while(counter):
    #Checking for an event
    for event in pygame.event.get():
        #If the event is a button being pressed,
        if event.type == pygame.JOYBUTTONDOWN:
                print("Button Pressed")
                if pygame.joystick.Joystick(0).get_button(0):
                     print("Button A")
                     ser.write(b'1')
                     ser1.write(b'1')

                if pygame.joystick.Joystick(0).get_button(1):
                     print("Button B")
                     ser.write(b'2')
                     ser1.write(b'2')
                if pygame.joystick.Joystick(0).get_button(2):
                     print("Button X")
                     ser.write(b'5')
                     ser1.write(b'5')
                if pygame.joystick.Joystick(0).get_button(3):
                     print("Button Y")
                     ser.write(b'3')
                     ser1.write(b'3')

if KeyboardInterrupt:
	print("Keyboard interrupt received.")
	ser.close()
	ser1.close()
