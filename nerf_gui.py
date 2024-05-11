import os
import time
import pygame

from functions import construct_folder_path, load_images, next_idx, previous_idx
import settings
from classes import (
    Button,
    ButtonLayout,
    CheckBoxLayout,
    Image,
    Orientation,
)

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Quick Maths")


def initialize_layouts():
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
    media_buttons_y = int(settings.SCREEN_SIZE.mid_y - 50 + 600 / 2 + settings.DISTANCE)
    arrows = ButtonLayout(
        ["<", ">"],
        active_ids=[0, 1],
        width=small_button_width,
        distance=settings.DISTANCE,
        orientation=Orientation.HORIZONTAL,
        x=int(settings.SCREEN_SIZE.x * 2 / 6),
        y=media_buttons_y,
    )
    play_button = Button(
        text="Play",
        y=media_buttons_y,
        x=settings.SCREEN_SIZE.left_third,
        width=200,
        active=True,
    )
    return n_samples, ablation, locks, arrows, play_button


def lego():
    samples_checkboxes, ablation_checkboxes, locks, arrows_buttons, play_button = (
        initialize_layouts()
    )
    folder_data = {
        "dataset_dir": "sampling_dataset",
        "pos_encoding": ablation_checkboxes["Pos encoding"].active,
        "view_dirs": ablation_checkboxes["View direction"].active,
        "n_samples": samples_checkboxes.get_active_checkboxes()[0].text,
    }
    folder_path = construct_folder_path(folder_data)
    images = load_images(folder_path)
    image_idx = 0
    max_idx = len(images) - 1
    run = True
    play = False
    while run:
        screen.fill(settings.Color.BACKGROUND.value)
        for event in pygame.event.get():
            if samples_checkboxes.update(event):
                active_samples_checkbox = samples_checkboxes.get_active_checkboxes()[0]
                if active_samples_checkbox.text == "128":
                    ablation_checkboxes.unlock()
                else:
                    ablation_checkboxes["Pos encoding"].active = True
                    ablation_checkboxes["View direction"].active = True
                    folder_data["pos_encoding"] = ablation_checkboxes[
                        "Pos encoding"
                    ].active
                    folder_data["view_dirs"] = ablation_checkboxes[
                        "View direction"
                    ].active
                    ablation_checkboxes.lock()

                folder_data["n_samples"] = active_samples_checkbox.text

                folder_path = construct_folder_path(folder_data)

                images = load_images(folder_path)

            if ablation_checkboxes.update(event):
                folder_data["pos_encoding"] = ablation_checkboxes["Pos encoding"].active
                folder_data["view_dirs"] = ablation_checkboxes["View direction"].active

                folder_path = construct_folder_path(folder_data)

                images = load_images(folder_path)

            if arrows_buttons.update(event):
                if arrows_buttons["<"].action:
                    image_idx = previous_idx(image_idx, max_idx)
                elif arrows_buttons[">"].action:
                    image_idx = next_idx(image_idx, max_idx)

            if play_button.set_action(event):
                play = not play
                if play:
                    play_button.text = "Stop"
                else:
                    play_button.text = "Play"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RIGHT:
                    image_idx = next_idx(image_idx, max_idx)
                if event.key == pygame.K_LEFT:
                    image_idx = previous_idx(image_idx, max_idx)
            if event.type == pygame.QUIT:
                run = False
        images[image_idx].draw(screen)
        play_button.draw(screen)
        arrows_buttons.display(screen)
        samples_checkboxes.display(screen)
        ablation_checkboxes.display(screen)
        if ablation_checkboxes.is_lock:
            for lock in locks:
                lock.draw(screen)
        if play:
            time.sleep(0.07)
            image_idx = next_idx(image_idx, max_idx)
        pygame.display.update()


if __name__ == "__main__":
    lego()
