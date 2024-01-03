#!/usr/bin/env python

import pygame, sys
from pygame.locals import *  

#For Flask
import threading
from flask import Flask, render_template, Response
import cv2
import numpy as np 

app = Flask(__name__)

backgroundColor = (105,255,255) 
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
botColor = (100,0,0) 

botX = 200
botY = 200

# To set the speed of the bot.
speed = 0.2

# DIMENTIONS
originalDimention = [40, 40, 305, 305, 20, 50, 80, 15]
scale = 2
D = [element * scale for element in originalDimention]

# Bot Dimensions
botWidth = D[0]
botHeight = D[1] 

# ARENA SHAPES
arenaX = D[2]
arenaY = D[3]
arenaPad = D[4]

# WASTE AREA SHAPES
wasteAreaX = D[5]
wasteAreaY = D[6]

# MARKER SIZE
markerSize = D[7]

arenaInternal = pygame.Rect(arenaPad, arenaPad, arenaX, arenaY)
arenaInner = pygame.Rect(arenaPad+markerSize, arenaPad+markerSize, arenaX-2*markerSize, arenaY-2*markerSize)
wasteOrganic = pygame.Rect(arenaPad, arenaPad+arenaY/2-wasteAreaY/2, wasteAreaX, wasteAreaY)
wasteInorganic = pygame.Rect(arenaPad+arenaX/2-wasteAreaY/2, arenaPad, wasteAreaY, wasteAreaX)

canvasWidth = arenaPad+arenaX+arenaPad
canvasHeight = arenaPad+arenaY+arenaPad

# CREATING CANVAS 
canvas = pygame.display.set_mode((canvasWidth,canvasHeight)) 

# MARKERS
corner1 = pygame.image.load('markers/C1.svg').convert()
corner2 = pygame.image.load('markers/C2.svg').convert()
corner3 = pygame.image.load('markers/C3.svg').convert()
corner4 = pygame.image.load('markers/C4.svg').convert()

# MARKER FOR BOT
bot1 = pygame.image.load('markers/B69.svg').convert()

# MARKERS FOR WASTE AREAS
wasteOrganicMarker = pygame.image.load('markers/W1.svg').convert()
wasteInorganicMarker = pygame.image.load('markers/W2.svg').convert()

# RESIZING MARKERS
corner1 = pygame.transform.scale(corner1, (markerSize, markerSize))
corner2 = pygame.transform.scale(corner2, (markerSize, markerSize))
corner3 = pygame.transform.scale(corner3, (markerSize, markerSize))
corner4 = pygame.transform.scale(corner4, (markerSize, markerSize))

bot1 = pygame.transform.scale(bot1, (markerSize, markerSize))

wasteOrganicMarker = pygame.transform.scale(wasteOrganicMarker, (markerSize, markerSize))
wasteInorganicMarker = pygame.transform.scale(wasteInorganicMarker, (markerSize, markerSize))

# Position of Markers
rectCorner1 = pygame.Rect(arenaPad, arenaPad, markerSize, markerSize)
rectCorner2 = pygame.Rect(arenaPad+arenaX-markerSize, arenaPad, markerSize, markerSize)
rectCorner3 = pygame.Rect(arenaPad+arenaX-markerSize, arenaPad+arenaY-markerSize, markerSize, markerSize)
rectCorner4 = pygame.Rect(arenaPad, arenaPad+arenaY-markerSize, markerSize, markerSize)

rectWasteOrganicMarker = pygame.Rect(arenaPad-markerSize/2+wasteAreaX/2, arenaPad+arenaX/2-markerSize/2, markerSize, markerSize)
rectWasteInorganicMarker = pygame.Rect(arenaPad+arenaY/2-markerSize/2, arenaPad-markerSize/2+wasteAreaX/2, markerSize, markerSize)

# TITLE OF CANVAS 
pygame.display.set_caption("Swarmanoid Simulation") 

# Creating a lock to handle multithreading
lock = threading.Lock()


def pygame_loop():
    global botX, botY  # Declare botX and botY as global variables
    while True:

        with lock:

            # Get inputs
            for event in pygame.event.get() :
              if event.type == QUIT :
                pygame.quit()
                sys.exit()    
    
            # BACKGROUND COLOR
            canvas.fill(backgroundColor) 

            pygame.draw.rect(canvas, BLUE, arenaInternal, 1)
            pygame.draw.rect(canvas, BLUE, arenaInner, 1)
            pygame.draw.rect(canvas, GREEN, wasteOrganic)
            pygame.draw.rect(canvas, RED, wasteInorganic)

            pygame.draw.rect(canvas, RED, rectCorner1, 1)
            pygame.draw.rect(canvas, RED, rectCorner2, 1)
            pygame.draw.rect(canvas, RED, rectCorner3, 1)
            pygame.draw.rect(canvas, RED, rectCorner4, 1)

            # Draw the image inside the rectangle
            canvas.blit(corner1, rectCorner1)
            canvas.blit(corner2, rectCorner2)
            canvas.blit(corner3, rectCorner3)
            canvas.blit(corner4, rectCorner4)

            canvas.blit(wasteOrganicMarker, rectWasteOrganicMarker)
            canvas.blit(wasteInorganicMarker, rectWasteInorganicMarker)

            bot = pygame.Rect(botX, botY, botWidth, botHeight)
            pygame.draw.rect(canvas, botColor, bot)

            #Marker For Bot
            rectBot1 = pygame.Rect(botX+botWidth/1.45-markerSize, botY+botHeight/1.45-markerSize, markerSize, markerSize)
            pygame.draw.rect(canvas, RED, rectBot1, 1)
            canvas.blit(bot1, rectBot1)

            # stores keys pressed  
            keys = pygame.key.get_pressed() 
      
            # if left arrow key is pressed 
            if keys[pygame.K_LEFT] and botX>0: 
          
                # decrement in x co-ordinate 
                botX -= speed
          
            # if left arrow key is pressed 
            if keys[pygame.K_RIGHT] and botX<canvasWidth-botWidth: 
          
                # increment in x co-ordinate 
                botX += speed 
         
            # if left arrow key is pressed    
            if keys[pygame.K_UP] and botY>0: 
          
                # decrement in y co-ordinate 
                botY -= speed 
          
            # if left arrow key is pressed    
            if keys[pygame.K_DOWN] and botY<canvasHeight-botHeight: 
                # increment in y co-ordinate 
                botY += speed        

            pygame.display.update()

 
@app.route('/')
def index():
    return render_template('index.html')

def generate():
    while True:
        with lock:
            # Capture the Pygame screen
            img_str = pygame.image.tostring(canvas, 'RGB')
            img_np = np.frombuffer(img_str, dtype=np.uint8)
            img = cv2.cvtColor(np.reshape(img_np, (canvasHeight, canvasWidth, 3)), cv2.COLOR_RGB2BGR)

            # Encode the frame to JPEG
            _, frame = cv2.imencode('.JPEG', img)
            frame_bytes = frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    pygame_thread = threading.Thread(target=pygame_loop)
    pygame_thread.daemon = True
    pygame_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=False)
