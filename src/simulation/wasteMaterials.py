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

speed = 0.2

botWidth = 80
botHeight = 80


markerSize = 30

botColor = (255, 255, 255)
RED = (255, 0, 0)


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

# Rectangles for waste positions
waste01X, waste01Y = 170, 470
waste02X, waste02Y = 270, 370
waste03X, waste03Y = 470, 170
waste04X, waste04Y = 370, 270
waste05X, waste05Y = 470, 325
waste06X, waste06Y = 170, 170
waste07X, waste07Y = 270, 270
waste08X, waste08Y = 370, 370
waste09X, waste09Y = 470, 470
waste10X, waste10Y = 170, 325

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


# Main game loop
picking_up_waste = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    canvas.fill((105, 255, 255))

    # Draw the wastes
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

    waveBot, rectBot1 = drawBots()

    particleBotX = 0
    particleBotY = 0

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

    # Update the display
    pygame.display.update()
