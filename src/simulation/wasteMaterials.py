#!/usr/bin/env python

import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the window
canvasWidth = 610
canvasHeight = 610
canvas = pygame.display.set_mode((canvasWidth, canvasHeight))
pygame.display.set_caption("Waste Grid")

# Marker Size
wasteMarkerSize = 20

# waste Size
wasteWidth = 10
wasteHeight = 30

waveBotX = 200
waveBotY = 200

speed = 1

botWidth = 80
botHeight = 80

markerSize = 30

botColor = (255, 255, 255)
RED = (255, 0, 0)

# Initialize active waste variables
active_waste = None

# Keyboard Movement Logic
from keyMovement import movement

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

# MARKER FOR BOT
bot1 = pygame.image.load("markers/B69.svg").convert()

bot1 = pygame.transform.scale(bot1, (markerSize, markerSize))


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

    return waveBot, rectBot1


def drawWasteBoxWithMarker(wasteImage, wastePosition):
    # Draw the waste box
    wasteX, wasteY = wastePosition["x"], wastePosition["y"]
    wasteBox = pygame.Rect(wasteX, wasteY, wasteWidth, wasteHeight)
    pygame.draw.rect(canvas, (0, 0, 0), wasteBox)

    # Calculate the position for the waste marker
    markerX = wasteX - wasteMarkerSize
    markerY = wasteY + wasteHeight / 2 - wasteMarkerSize / 2

    # Draw the waste marker
    markerRect = pygame.Rect(markerX, markerY, wasteMarkerSize, wasteMarkerSize)
    pygame.draw.rect(canvas, (0, 0, 0), markerRect, 1)
    canvas.blit(wasteImage, markerRect)


waste_positions = {
    "waste01": {"x": 170, "y": 470},
    "waste02": {"x": 270, "y": 370},
    "waste03": {"x": 470, "y": 170},
    "waste04": {"x": 370, "y": 270},
    "waste05": {"x": 470, "y": 325},
    "waste06": {"x": 170, "y": 170},
    "waste07": {"x": 270, "y": 270},
    "waste08": {"x": 370, "y": 370},
    "waste09": {"x": 470, "y": 470},
    "waste10": {"x": 170, "y": 325},
}

# Main game loop
clock = pygame.time.Clock()
active_waste = None
moving_with_bot = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    canvas.fill((105, 255, 255))

    # Draw the wastes
    for waste_key, waste_position in waste_positions.items():
        if moving_with_bot and active_waste == waste_key:
            # If the waste is active, move it with the bot
            waste_position["x"] = waveBotX + botWidth / 2 - wasteWidth / 2
            waste_position["y"] = waveBotY - botWidth / 2 + wasteHeight
        drawWasteBoxWithMarker(locals()[f"waste{waste_key[5:]}"], waste_position)

    waveBot, rectBot1 = drawBots()

    # Stores keys pressed
    keys = pygame.key.get_pressed()
    waveBotX, waveBotY, particleBotX, particleBotY = movement(
        keys,
        waveBotX,
        waveBotY,
        0,
        0,
        speed,
        canvasWidth,
        canvasHeight,
        botWidth,
        botHeight,
    )

    # Check for collisions with waveBot
    for waste_key, waste_position in waste_positions.items():
        waste_rect = pygame.Rect(
            waste_position["x"], waste_position["y"], wasteWidth, wasteHeight
        )
        if (
            keys[K_p]
            and waveBot.colliderect(waste_rect)
            and waveBot.top <= waste_rect.bottom
            and waveBot.bottom >= waste_rect.bottom
        ):
            # Store the active waste and start moving it with the bot
            active_waste = waste_key
            moving_with_bot = True

    if keys[K_d] and active_waste is not None:
        # If 'd' is pressed and there is an active waste, stop moving it with the bot
        moving_with_bot = False
        active_waste = None

    # Print the active waste (for demonstration purposes)
    print("Active Waste:", active_waste)

    # Update the display
    pygame.display.update()
    clock.tick(60)
