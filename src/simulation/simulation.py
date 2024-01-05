#!/usr/bin/env python

import pygame, sys
from pygame.locals import *

# For Flask
import threading
from flask import Flask, render_template, Response
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# Keyboard Movement Logic
from keyMovement import movement

app = Flask(__name__)

# MQTT settings
broker_address = "192.168.1.80"
waveClient = mqtt.Client()
particleClient = mqtt.Client()


backgroundColor = (105, 255, 255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
botColor = (100, 0, 0)

waveBotX = 200
waveBotY = 200

#######################################################################################################################
particleBotX = 300
particleBotY = 200
#######################################################################################################################

# To set the speed of the bot.
speed = 0.2

# DIMENTIONS
originalDimention = [40, 40, 305, 305, 20, 50, 80, 15, 10, 5, 15]
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
wasteMarkerSize = D[8]

# WASTE SIZE
wasteWidth = D[9]
wasteHeight = D[10]

arenaInternal = pygame.Rect(arenaPad, arenaPad, arenaX, arenaY)

arenaInner = pygame.Rect(
    arenaPad + markerSize,
    arenaPad + markerSize,
    arenaX - 2 * markerSize,
    arenaY - 2 * markerSize,
)

wasteOrganic = pygame.Rect(
    arenaPad, arenaPad + arenaY / 2 - wasteAreaY / 2, wasteAreaX, wasteAreaY
)

wasteInorganic = pygame.Rect(
    arenaPad + arenaX / 2 - wasteAreaY / 2, arenaPad, wasteAreaY, wasteAreaX
)

canvasWidth = arenaPad + arenaX + arenaPad
canvasHeight = arenaPad + arenaY + arenaPad

# CREATING CANVAS
canvas = pygame.display.set_mode((canvasWidth, canvasHeight))


# WASTE
# Marker Size
markerSize = 20

# Importing Waste
waste01 = pygame.image.load("markers/M100.svg").convert()
waste02 = pygame.image.load("markers/M111.svg").convert()
waste03 = pygame.image.load("markers/M122.svg").convert()
waste04 = pygame.image.load("markers/M133.svg").convert()
waste05 = pygame.image.load("markers/M144.svg").convert()
waste06 = pygame.image.load("markers/M155.svg").convert()
waste07 = pygame.image.load("markers/M166.svg").convert()
waste08 = pygame.image.load("markers/M177.svg").convert()
waste09 = pygame.image.load("markers/M188.svg").convert()
waste10 = pygame.image.load("markers/M199.svg").convert()

# Resizing Waste
waste01 = pygame.transform.scale(waste01, (markerSize, markerSize))
waste02 = pygame.transform.scale(waste02, (markerSize, markerSize))
waste03 = pygame.transform.scale(waste03, (markerSize, markerSize))
waste04 = pygame.transform.scale(waste04, (markerSize, markerSize))
waste05 = pygame.transform.scale(waste05, (markerSize, markerSize))
waste06 = pygame.transform.scale(waste06, (markerSize, markerSize))
waste07 = pygame.transform.scale(waste07, (markerSize, markerSize))
waste08 = pygame.transform.scale(waste08, (markerSize, markerSize))
waste09 = pygame.transform.scale(waste09, (markerSize, markerSize))
waste10 = pygame.transform.scale(waste10, (markerSize, markerSize))

# Rectangles for waste positions
waste01X, waste01Y = 180, 480
waste02X, waste02Y = 280, 380
waste03X, waste03Y = 480, 180
waste04X, waste04Y = 380, 280
waste05X, waste05Y = 480, 335
waste06X, waste06Y = 180, 180
waste07X, waste07Y = 280, 280
waste08X, waste08Y = 380, 380
waste09X, waste09Y = 480, 480
waste10X, waste10Y = 180, 335


# MARKERS
corner1 = pygame.image.load("markers/C1.svg").convert()
corner2 = pygame.image.load("markers/C2.svg").convert()
corner3 = pygame.image.load("markers/C3.svg").convert()
corner4 = pygame.image.load("markers/C4.svg").convert()

# MARKER FOR BOT
bot1 = pygame.image.load("markers/B69.svg").convert()
bot2 = pygame.image.load("markers/B96.svg").convert()

# MARKERS FOR WASTE AREAS
wasteOrganicMarker = pygame.image.load("markers/W22.svg").convert()
wasteInorganicMarker = pygame.image.load("markers/W33.svg").convert()

# RESIZING MARKERS
corner1 = pygame.transform.scale(corner1, (markerSize, markerSize))
corner2 = pygame.transform.scale(corner2, (markerSize, markerSize))
corner3 = pygame.transform.scale(corner3, (markerSize, markerSize))
corner4 = pygame.transform.scale(corner4, (markerSize, markerSize))

bot1 = pygame.transform.scale(bot1, (markerSize, markerSize))
bot2 = pygame.transform.scale(bot2, (markerSize, markerSize))

wasteOrganicMarker = pygame.transform.scale(
    wasteOrganicMarker, (markerSize, markerSize)
)
wasteInorganicMarker = pygame.transform.scale(
    wasteInorganicMarker, (markerSize, markerSize)
)

# Position of Markers
rectCorner1 = pygame.Rect(arenaPad, arenaPad, markerSize, markerSize)

rectCorner2 = pygame.Rect(
    arenaPad + arenaX - markerSize, arenaPad, markerSize, markerSize
)

rectCorner3 = pygame.Rect(
    arenaPad + arenaX - markerSize,
    arenaPad + arenaY - markerSize,
    markerSize,
    markerSize,
)

rectCorner4 = pygame.Rect(
    arenaPad, arenaPad + arenaY - markerSize, markerSize, markerSize
)


# Waste  Spots
rectWasteOrganicMarker = pygame.Rect(
    arenaPad - markerSize / 2 + wasteAreaX / 2,
    arenaPad + arenaX / 2 - markerSize / 2,
    markerSize,
    markerSize,
)

rectWasteInorganicMarker = pygame.Rect(
    arenaPad + arenaY / 2 - markerSize / 2,
    arenaPad - markerSize / 2 + wasteAreaX / 2,
    markerSize,
    markerSize,
)


def drawWasteBoxWithMarker(wasteImage, wasteX, wasteY):
    # Draw the waste box
    wasteBox = pygame.Rect(wasteX, wasteY, wasteWidth, wasteHeight)
    pygame.draw.rect(canvas, (0, 0, 0), wasteBox)

    # Calculate the position for the waste marker
    markerX = wasteX - wasteMarkerSize
    markerY = wasteY + wasteHeight / 2 - wasteMarkerSize / 2

    # Draw the waste marker
    markerRect = pygame.Rect(markerX, markerY, wasteMarkerSize, wasteMarkerSize)
    pygame.draw.rect(canvas, (0, 0, 0), markerRect, 1)
    canvas.blit(wasteImage, markerRect)

def drawWaste():
    drawWasteBoxWithMarker(waste01, waste01X, waste01Y)
    drawWasteBoxWithMarker(waste02, waste02X, waste02Y)
    drawWasteBoxWithMarker(waste03, waste03X, waste03Y)
    drawWasteBoxWithMarker(waste04, waste04X, waste04Y)
    drawWasteBoxWithMarker(waste05, waste05X, waste05Y)
    drawWasteBoxWithMarker(waste06, waste06X, waste06Y)
    drawWasteBoxWithMarker(waste07, waste07X, waste07Y)
    drawWasteBoxWithMarker(waste08, waste08X, waste08Y)
    drawWasteBoxWithMarker(waste09, waste09X, waste09Y)
    drawWasteBoxWithMarker(waste10, waste10X, waste10Y)
    
def drawArena():
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

    # Draw Waste Spot Markers
    canvas.blit(wasteOrganicMarker, rectWasteOrganicMarker)
    canvas.blit(wasteInorganicMarker, rectWasteInorganicMarker)


def drawBots():
    waveBot = pygame.Rect(waveBotX, waveBotY, botWidth, botHeight)
    pygame.draw.rect(canvas, botColor, waveBot)

    # Marker For Bot
    rectBot1 = pygame.Rect(
        waveBotX + botWidth / 2 - markerSize / 2,
        waveBotY + botHeight / 2 - markerSize / 2,
        markerSize,
        markerSize,
    )
    pygame.draw.rect(canvas, RED, rectBot1, 1)
    canvas.blit(bot1, rectBot1)

    #######################################################################################################################

    particleBot = pygame.Rect(particleBotX, particleBotY, botWidth, botHeight)
    pygame.draw.rect(canvas, botColor, particleBot)

    # Marker For Bott
    rectBot2 = pygame.Rect(
        particleBotX + botWidth / 2 - markerSize / 2,
        particleBotY + botHeight / 2 - markerSize / 2,
        markerSize,
        markerSize,
    )

    pygame.draw.rect(canvas, RED, rectBot2, 1)
    canvas.blit(bot2, rectBot2)

    return waveBot, rectBot1, particleBot, rectBot2


# TITLE OF CANVAS
pygame.display.set_caption("Swarmanoid Simulation")


# Callback when a message is received
def on_wave_message(waveClient, userdata, msg):
    global waveBotX, waveBotY

    message = msg.payload.decode("utf-8")

    # Move the bot based on the received message
    if message == "left" and waveBotX > 0:
        waveBotX -= speed
    elif message == "right" and waveBotX < canvasWidth - botWidth:
        waveBotX += speed
    elif message == "up" and waveBotY > 0:
        waveBotY -= speed
    elif message == "down" and waveBotY < canvasHeight - botHeight:
        waveBotY += speed


# Connect to MQTT broker and subscribe to the wave movement topic
waveClient.connect(broker_address, 1883, 60)
waveClient.subscribe("wave")
waveClient.on_message = on_wave_message
waveClient.loop_start()


#######################################################################################################################
# Callback when a message is received
def on_particle_message(particleClient, userdata, msg):
    global particleBotX, particleBotY

    message = msg.payload.decode("utf-8")

    # Move the bot based on the received message
    if message == "left" and particleBotX > 0:
        particleBotX -= speed
    elif message == "right" and particleBotX < canvasWidth - botWidth:
        particleBotX += speed
    elif message == "up" and particleBotY > 0:
        particleBotY -= speed
    elif message == "down" and particleBotY < canvasHeight - botHeight:
        particleBotY += speed


# Connect to MQTT broker and subscribe to the particle movement topic
particleClient.connect(broker_address, 1883, 60)
particleClient.subscribe("particle")
particleClient.on_message = on_particle_message
particleClient.loop_start()
#######################################################################################################################

# Creating a lock to handle multithreading
lock = threading.Lock()


def pygame_loop():
    global waveBotX, waveBotY, particleBotX, particleBotY  # Declare botX and botY as global variables
    while True:
        with lock:
            # Get inputs
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # BACKGROUND COLOR
            canvas.fill(backgroundColor)

            drawArena()
            drawWaste()
            waveBot, rectBot1, particleBot, rectBot2 = drawBots()

            collisionTolerance = 10
            if waveBot.colliderect(particleBot):
                if abs(particleBot.top - waveBot.bottom) < collisionTolerance:
                    waveBotY -= speed
                if abs(particleBot.bottom - waveBot.top) < collisionTolerance:
                    waveBotY += speed
                if abs(particleBot.left - waveBot.right) < collisionTolerance:
                    waveBotX -= speed
                if abs(particleBot.right - waveBot.left) < collisionTolerance:
                    waveBotX += speed

            # stores keys pressed
            keys = pygame.key.get_pressed()
            waveBotX, waveBotY, particleBotX, particleBotY = movement(
                keys,
                waveBotX,
                waveBotY,
                particleBotX,
                particleBotY,
                speed,
                canvasWidth,
                canvasHeight,
                botWidth,
                botHeight,
            )

            pygame.display.update()


@app.route("/")
def index():
    return render_template("index.html")


def generate():
    while True:
        with lock:
            # Capture the Pygame screen
            img_str = pygame.image.tostring(canvas, "RGB")
            img_np = np.frombuffer(img_str, dtype=np.uint8)
            img = cv2.cvtColor(
                np.reshape(img_np, (canvasHeight, canvasWidth, 3)), cv2.COLOR_RGB2BGR
            )

            # Encode the frame to JPEG
            _, frame = cv2.imencode(".JPEG", img)
            frame_bytes = frame.tobytes()

        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    pygame_thread = threading.Thread(target=pygame_loop)
    pygame_thread.daemon = True
    pygame_thread.start()

    app.run(host="0.0.0.0", port=5000, debug=False)
