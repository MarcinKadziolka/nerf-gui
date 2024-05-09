import pygame
import settings
import functions
from classes import (
    Button,
    TextField,
    CheckBoxLayout,
    Navigation,
    ButtonLayout,
    Orientation,
)
import random
import time
from collections import defaultdict
import os
from copy import copy

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Quick Maths")


def lego():
    run = True
    checkboxes_x = settings.SCREEN_SIZE.right_third
    checkboxes_y = 200
    while run:
        screen.fill(settings.Color.BACKGROUND.value)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


if __name__ == "__main__":
    lego()
