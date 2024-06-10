import os

import pygame

import lego
import settings
from helpers import CheckBoxLayout, Orientation

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Nerf gui")


project_checkboxes = CheckBoxLayout(
    ["Sampling", "Mednerf"],
    active_ids=[0],
    width=350,
    distance=settings.VERTICAL_DISTANCE,
    x=settings.SCREEN_SIZE.right_third,
    y=100,
    orientation=Orientation.VERTICAL,
)


if __name__ == "__main__":
    lego.lego_run(project_checkboxes, screen)
