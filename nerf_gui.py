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
    checkboxes_y = 600
    n_samples = CheckBoxLayout(
        ["8", "16", "32", "64", "128"],
        active={0},
        width=60,
        distance=settings.DISTANCE,
        x=checkboxes_x,
        y=checkboxes_y,
        orientation=Orientation.HORIZONTAL,
    )
    while run:
        screen.fill(settings.Color.BACKGROUND.value)
        for event in pygame.event.get():
            n_samples.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
        n_samples.display(screen)
        pygame.display.update()


if __name__ == "__main__":
    lego()
