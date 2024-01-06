import pygame


def movement(
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
):
    # Movement for waveBotX
    if (
        keys[pygame.K_LEFT]
        and waveBotX > 0
        and not pygame.key.get_mods() & pygame.KMOD_SHIFT
    ):
        waveBotX -= speed

    if (
        keys[pygame.K_RIGHT]
        and waveBotX < canvasWidth - botWidth
        and not pygame.key.get_mods() & pygame.KMOD_SHIFT
    ):
        waveBotX += speed

    if (
        keys[pygame.K_UP]
        and waveBotY > 0
        and not pygame.key.get_mods() & pygame.KMOD_SHIFT
    ):
        waveBotY -= speed

    if (
        keys[pygame.K_DOWN]
        and waveBotY < canvasHeight - botHeight
        and not pygame.key.get_mods() & pygame.KMOD_SHIFT
    ):
        waveBotY += speed

    # Movement for particleBotX with Shift key
    if (
        keys[pygame.K_LEFT]
        and pygame.key.get_mods() & pygame.KMOD_SHIFT
        and particleBotX > 0
    ):
        particleBotX -= speed

    if (
        keys[pygame.K_RIGHT]
        and pygame.key.get_mods() & pygame.KMOD_SHIFT
        and particleBotX < canvasWidth - botWidth
    ):
        particleBotX += speed

    if (
        keys[pygame.K_UP]
        and pygame.key.get_mods() & pygame.KMOD_SHIFT
        and particleBotY > 0
    ):
        particleBotY -= speed

    if (
        keys[pygame.K_DOWN]
        and pygame.key.get_mods() & pygame.KMOD_SHIFT
        and particleBotY < canvasHeight - botHeight
    ):
        particleBotY += speed

    return waveBotX, waveBotY, particleBotX, particleBotY
