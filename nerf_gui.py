import os

import pygame

from functions import construct_folder_path, load_images, next_idx, previous_idx
import settings
from classes import (
    ButtonLayout,
    CheckBoxLayout,
    Image,
    Orientation,
)

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Quick Maths")


def lego():
    run = True
    checkboxes_x = settings.SCREEN_SIZE.right_third
    checkboxes_y = 600
    small_button_width = 70
    n_samples = CheckBoxLayout(
        ["16", "32", "64", "128"],
        active_ids=[3],
        width=small_button_width,
        distance=settings.DISTANCE + 10,
        x=checkboxes_x,
        y=checkboxes_y,
        orientation=Orientation.HORIZONTAL,
    )
    ablation = CheckBoxLayout(
        ["Pos encoding", "View direction"],
        active_ids=[0, 1],
        width=350,
        distance=settings.DISTANCE,
        x=checkboxes_x,
        y=400,
        orientation=Orientation.VERTICAL,
        multiple_choice=True,
    )
    locks_x = int(ablation.x - ablation.width / 2 + 20)
    locks_scale = 1
    lock1 = Image(
        "lock.png",
        x=locks_x,
        border_size=0,
        y=ablation.y - 3,
        scale=locks_scale,
    )
    lock2 = Image(
        "lock.png",
        x=locks_x,
        border_size=0,
        y=ablation.y + ablation.distance - 3,
        scale=locks_scale,
    )
    locks = [lock1, lock2]
    image = Image(
        image_path="000.png",
        scale=1.5,
        x=int(settings.SCREEN_SIZE.x * 2 / 6),
        y=settings.SCREEN_SIZE.mid_y - 50,
    )
    arrows = ButtonLayout(
        ["<", ">"],
        active_ids=[0, 1],
        width=small_button_width,
        distance=settings.DISTANCE,
        orientation=Orientation.HORIZONTAL,
        x=image.x,
        y=int(image.y + image.height / 2 + settings.DISTANCE),
    )

    image_idx = 0
    folder_data = {
        "dataset_dir": "sampling_dataset",
        "pos_encoding": ablation["Pos encoding"].active,
        "view_dirs": ablation["View direction"].active,
        "n_samples": n_samples.get_active()[0].text,
    }
    folder_path = construct_folder_path(folder_data)
    images = load_images(folder_path)
    max_idx = len(images) - 1
    while run:
        screen.fill(settings.Color.BACKGROUND.value)
        for event in pygame.event.get():

            n_samples.update(event)
            if n_samples.checkboxes[-1].active:
                ablation.unlock()
            else:
                ablation.lock()

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
        if ablation.is_lock:
            for lock in locks:
                lock.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    lego()
