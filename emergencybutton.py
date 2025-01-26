#Import the necessary dependencies
import pygame          
import os
from twilio.rest import Client

#Initialize the Joystick
pygame.joystick.init()
pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
#Twilio account id and authentication token, will not be published on Github for privacy reasons.
account_sid = ""
auth_token  = ""
client = Client(account_sid, auth_token)
counter = 1
while(counter):
    #Checking for an event
    for event in pygame.event.get():
        #If the event is a button being pressed,
        if event.type == pygame.JOYBUTTONDOWN:
                #And if the button is button #5, print emergency button pressed
                if pygame.joystick.Joystick(0).get_button(5):
                    print("Emergency Button Pressed")
                    #Call to the emergency contact for AssistBot, and tell them that the emergency button has been pressed.
                    #For privacy reasons, the emergency contact's phone number and AssistBot's phone number will not be published.
                    call = client.calls.create(to="",
                                            from_="",
                                            twiml='<Response><Say>Hello there. The emergency button has been pressed. Please come immediately.</Say></Response>')
                    counter = 0
                    break
    
