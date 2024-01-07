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
from micropython.secrets import BROKER_ADDRESS

app = Flask(__name__)

# MQTT settings
broker_address = BROKER_ADDRESS
waveClient = mqtt.Client()
particleClient = mqtt.Client()


backgroundColor = (100, 255, 255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
botColor = (200, 200, 0)
wasteColor = (0, 200, 200)

waveBotX = 200
waveBotY = 200
#######################################################################################################################
particleBotX = 300
particleBotY = 200
#######################################################################################################################

# To set the speed of the bot.
speed = 1

# DIMENTIONS
originalDimention = [40, 40, 305, 305, 20, 50, 80, 15, 10, 5, 15]
scale = 2.2
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

# global variables for particle bot
waveBot = pygame.Rect(waveBotX, waveBotY, botWidth, botHeight)
particleBot = pygame.Rect(particleBotX, particleBotY, botWidth, botHeight)

# Active Wastes and Carrying Bots
activeWastes = {"waveBot": None, "particleBot": None}
carryingBots = {"waveBot": None, "particleBot": None}

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

# Importing Waste
waste01 = pygame.image.load("src/markers/M100.svg").convert()
waste02 = pygame.image.load("src/markers/M111.svg").convert()
waste03 = pygame.image.load("src/markers/M122.svg").convert()
waste04 = pygame.image.load("src/markers/M133.svg").convert()
waste05 = pygame.image.load("src/markers/M144.svg").convert()
waste06 = pygame.image.load("src/markers/M155.svg").convert()
waste07 = pygame.image.load("src/markers/M166.svg").convert()
waste08 = pygame.image.load("src/markers/M177.svg").convert()
waste09 = pygame.image.load("src/markers/M188.svg").convert()
waste10 = pygame.image.load("src/markers/M199.svg").convert()

# Resizing Waste
waste01 = pygame.transform.scale(waste01, (wasteMarkerSize, wasteMarkerSize))
waste02 = pygame.transform.scale(waste02, (wasteMarkerSize, wasteMarkerSize))
waste03 = pygame.transform.scale(waste03, (wasteMarkerSize, wasteMarkerSize))
waste04 = pygame.transform.scale(waste04, (wasteMarkerSize, wasteMarkerSize))
waste05 = pygame.transform.scale(waste05, (wasteMarkerSize, wasteMarkerSize))
waste06 = pygame.transform.scale(waste06, (wasteMarkerSize, wasteMarkerSize))
waste07 = pygame.transform.scale(waste07, (wasteMarkerSize, wasteMarkerSize))
waste08 = pygame.transform.scale(waste08, (wasteMarkerSize, wasteMarkerSize))
waste09 = pygame.transform.scale(waste09, (wasteMarkerSize, wasteMarkerSize))
waste10 = pygame.transform.scale(waste10, (wasteMarkerSize, wasteMarkerSize))

# Rectangles for waste positions
waste_positions = {
    "waste01": {"x": 90 * scale, "y": 240 * scale},
    "waste02": {"x": 140 * scale, "y": 190 * scale},
    "waste03": {"x": 240 * scale, "y": 90 * scale},
    "waste04": {"x": 190 * scale, "y": 140 * scale},
    "waste05": {"x": 240 * scale, "y": 167.5 * scale},
    "waste06": {"x": 90 * scale, "y": 90 * scale},
    "waste07": {"x": 140 * scale, "y": 140 * scale},
    "waste08": {"x": 190 * scale, "y": 190 * scale},
    "waste09": {"x": 240 * scale, "y": 240 * scale},
    "waste10": {"x": 90 * scale, "y": 167.5 * scale},
}

# MARKERS
corner1 = pygame.image.load("src/markers/C1.svg").convert()
corner2 = pygame.image.load("src/markers/C2.svg").convert()
corner3 = pygame.image.load("src/markers/C3.svg").convert()
corner4 = pygame.image.load("src/markers/C4.svg").convert()

# MARKER FOR BOT
bot1 = pygame.image.load("src/markers/B69.svg").convert()
bot2 = pygame.image.load("src/markers/B96.svg").convert()

# MARKERS FOR WASTE AREAS
wasteOrganicMarker = pygame.image.load("src/markers/W22.svg").convert()
wasteInorganicMarker = pygame.image.load("src/markers/W33.svg").convert()

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


def drawWasteBoxWithMarker(wasteImage, wastePosition):
    # Draw the waste box
    wasteX, wasteY = wastePosition["x"], wastePosition["y"]
    wasteBox = pygame.Rect(wasteX, wasteY, wasteWidth, wasteHeight)
    pygame.draw.rect(canvas, wasteColor, wasteBox)

    # Calculate the position for the waste marker
    markerX = wasteX - wasteMarkerSize
    markerY = wasteY + wasteHeight / 2 - wasteMarkerSize / 2

    # Draw the waste marker
    markerRect = pygame.Rect(markerX, markerY, wasteMarkerSize, wasteMarkerSize)
    pygame.draw.rect(canvas, (0, 0, 0), markerRect, 1)
    canvas.blit(wasteImage, markerRect)


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

# Define unique identifiers for each bot
WAVE_BOT_ID = "waveBot"
PARTICLE_BOT_ID = "particleBot"


# Callback when a message is received
def on_wave_message(waveClient, userdata, msg):
    global waveBotX, waveBotY, activeWastes, waveBot, carryingBots

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

    # Handle "pick" command
    if message == "pick":
        pick_waste(WAVE_BOT_ID)

    # Handle "drop" command
    if message == "drop":
        drop_waste(WAVE_BOT_ID)


#######################################################################################################################
# Callback when a message is received
def on_particle_message(particleClient, userdata, msg):
    global particleBotX, particleBotY, activeWastes, particleBot, carryingBots

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

    # Handle "pick" command
    if message == "pick":
        pick_waste(PARTICLE_BOT_ID)

    # Handle "drop" command
    if message == "drop":
        drop_waste(PARTICLE_BOT_ID)


# Function to handle picking up waste
def pick_waste(bot_id):
    global activeWastes, carryingBots, waste_positions

    # Check if the bot is already carrying waste
    if activeWastes[bot_id] is not None:
        return

    # Get the rectangle of the bot
    bot_rect = pygame.Rect(
        globals()[f"{bot_id}X"], globals()[f"{bot_id}Y"], botWidth, botHeight
    )

    # Iterate through waste positions to find a nearby waste
    for waste_key, waste_position in waste_positions.items():
        waste_rect = pygame.Rect(
            waste_position["x"], waste_position["y"], wasteWidth, wasteHeight
        )

        # Check if the bot and waste rectangles collide
        if bot_rect.colliderect(waste_rect):
            # Set the waste as active for the bot
            activeWastes[bot_id] = waste_key
            carryingBots[bot_id] = bot_id
            break  # Exit the loop after picking up one waste


# Function to handle dropping waste
def drop_waste(bot_id):
    global activeWastes, carryingBots

    if activeWastes[bot_id] is not None:
        activeWastes[bot_id] = None
        carryingBots[bot_id] = None


# Connect to MQTT broker and subscribe to the wave movement topic
waveClient.connect(broker_address, 1883, 60)
waveClient.subscribe("wave")
waveClient.on_message = on_wave_message
waveClient.loop_start()

#######################################################################################################################

# Connect to MQTT broker and subscribe to the particle movement topic
particleClient.connect(broker_address, 1883, 60)
particleClient.subscribe("particle")
particleClient.on_message = on_particle_message
particleClient.loop_start()

# Creating a lock to handle multithreading
lock = threading.Lock()


def pygame_loop():
    clock = pygame.time.Clock()
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

            # DRAW WASTE
            for waste_key, waste_position in waste_positions.items():
                drawWasteBoxWithMarker(
                    globals()[f"waste{waste_key[5:]}"], waste_position
                )

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

            if keys[K_q]:
                pygame.quit()
                sys.exit()

            # Check for collisions with bots and wastes
            for waste_key, waste_position in waste_positions.items():
                waste_rect = pygame.Rect(
                    waste_position["x"], waste_position["y"], wasteWidth, wasteHeight
                )

                if keys[K_p] and keys[K_LSHIFT]:
                    # Shift + P: ParticleBot picks up the waste
                    if (
                        particleBot.colliderect(waste_rect)
                        and particleBot.top <= waste_rect.bottom
                        and particleBot.bottom >= waste_rect.bottom
                    ):
                        activeWastes["particleBot"] = waste_key
                        carryingBots["particleBot"] = "particleBot"

                elif keys[K_p]:
                    # P: WaveBot picks up the waste
                    if (
                        waveBot.colliderect(waste_rect)
                        and waveBot.top <= waste_rect.bottom
                        and waveBot.bottom >= waste_rect.bottom
                    ):
                        activeWastes["waveBot"] = waste_key
                        carryingBots["waveBot"] = "waveBot"

                elif (
                    keys[K_d]
                    and keys[K_LSHIFT]
                    and activeWastes["particleBot"] is not None
                ):
                    # Shift + D: ParticleBot releases the waste
                    activeWastes["particleBot"] = None
                    carryingBots["particleBot"] = None

                elif keys[K_d] and activeWastes["waveBot"] is not None:
                    # D: WaveBot releases the waste
                    activeWastes["waveBot"] = None
                    carryingBots["waveBot"] = None

            # Move wastes with their respective bots
            for bot_key, waste_key in activeWastes.items():
                if waste_key is not None and carryingBots[bot_key] == bot_key:
                    waste_position = waste_positions[waste_key]
                    # Move the waste with the bot
                    if bot_key == "waveBot":
                        waste_position["x"] = waveBotX + botWidth / 2 - wasteWidth / 2
                        waste_position["y"] = waveBotY - botWidth / 2 + wasteHeight
                    elif bot_key == "particleBot":
                        waste_position["x"] = (
                            particleBotX + botWidth / 2 - wasteWidth / 2
                        )
                        waste_position["y"] = particleBotY - botWidth / 2 + wasteHeight

            # Print the active wastes (for demonstration purposes)
            # print("Active Wastes:", activeWastes)

            pygame.display.update()
            # clock.tick(130)
            clock.tick(65)


@app.route("/")
def index():
    return render_template("index.html")


def generate():
    while True:
        with lock:
            # Create local copies of canvasWidth and canvasHeight
            local_canvas_width = int(canvasWidth)
            local_canvas_height = int(canvasHeight)

            # Capture the Pygame screen
            img_str = pygame.image.tostring(canvas, "RGB")
            img_np = np.frombuffer(img_str, dtype=np.uint8)

            img = cv2.cvtColor(
                np.reshape(img_np, (local_canvas_height, local_canvas_width, 3)),
                cv2.COLOR_RGB2BGR,
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
