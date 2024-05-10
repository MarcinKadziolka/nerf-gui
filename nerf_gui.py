import pygame
import settings
from classes import (
    ButtonLayout,
    CheckBoxLayout,
    Orientation,
    Image,
)
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Quick Maths")


def lego():
    run = True
    checkboxes_x = settings.SCREEN_SIZE.right_third
    checkboxes_y = 600
    small_button_width = 60
    n_samples = CheckBoxLayout(
        ["8", "16", "32", "64", "128"],
        active={0},
        width=small_button_width,
        distance=settings.DISTANCE,
        x=checkboxes_x,
        y=checkboxes_y,
        orientation=Orientation.HORIZONTAL,
    )
    ablation = CheckBoxLayout(
        ["Pos encoding", "View direction"],
        active={0, 1},
        width=300,
        distance=settings.DISTANCE,
        x=checkboxes_x,
        y=400,
        orientation=Orientation.VERTICAL,
        multiple_choice=True,
    )
    image = Image(
        image_path="000.png",
        scale_factor=1.5,
        x=int(settings.SCREEN_SIZE.x * 2 / 6),
        y=settings.SCREEN_SIZE.mid_y - 50,
    )
    arrows = ButtonLayout(
        ["<", ">"],
        active={0, 1},
        width=small_button_width,
        distance=settings.DISTANCE,
        orientation=Orientation.HORIZONTAL,
        x=image.x,
        y=int(image.y + image.height / 2 + settings.DISTANCE),
    )
    while run:
        screen.fill(settings.Color.BACKGROUND.value)
        for event in pygame.event.get():
            n_samples.update(event)
            ablation.update(event)

            if (activated_arrow := arrows.update(event)) is not None:
                if activated_arrow.text == "<":
                    pass
                elif activated_arrow.text == ">":
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        image.draw(screen)
        arrows.display(screen)
        n_samples.display(screen)
        ablation.display(screen)
        pygame.display.update()


if __name__ == "__main__":
    lego()
