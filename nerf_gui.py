import os
import time

import pygame

import settings
from helpers import (
    Button,
    ButtonLayout,
    CheckBoxLayout,
    Image,
    Orientation,
    Indexing,
    load_all_folders,
    construct_folder_name,
    set_idx,
)

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Nerf gui")


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


def handle_play_flag(play_button, play, event):
    if play_button.set_action(event):
        play = not play
        play_button.text = "Stop" if play else "Play"
    return play


def handle_arrows(arrows_buttons, play, play_button, event):
    index_direction = None
    if arrows_buttons.update(event):
        play = False
        play_button.text = "Play"
        if arrows_buttons["<"].action:
            index_direction = Indexing.PREVIOUS
        elif arrows_buttons[">"].action:
            index_direction = Indexing.NEXT
    return play, index_direction


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

    folders = load_all_folders("sampling_dataset")
    folder_name = construct_folder_name(folder_data)
    images = folders[folder_name]
    image_idx = 0
    max_idx = len(images) - 1
    run = True
    play = False
    play_speed = 0.07
    while run:
        update_folder = False
        for event in pygame.event.get():
            folder_name = None
            index_direction = None

            if samples_checkboxes.update(event) or ablation_checkboxes.update(event):
                update_folder = True

            play, index_direction = handle_arrows(
                arrows_buttons, play, play_button, event
            )

            play = handle_play_flag(play_button, play, event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_LEFT:
                    index_direction = Indexing.PREVIOUS
                if event.key == pygame.K_RIGHT:
                    index_direction = Indexing.NEXT
            if event.type == pygame.QUIT:
                run = False

            if index_direction is not None:
                image_idx = set_idx(image_idx, max_idx, index_direction)

        if update_folder:
            active_samples_checkbox = samples_checkboxes.get_active_checkboxes()[0]
            if active_samples_checkbox.text == "128":
                ablation_checkboxes.unlock()
            else:
                ablation_checkboxes["Pos encoding"].active = True
                ablation_checkboxes["View direction"].active = True
                ablation_checkboxes.lock()

            folder_data["n_samples"] = active_samples_checkbox.text
            folder_data["pos_encoding"] = ablation_checkboxes["Pos encoding"].active
            folder_data["view_dirs"] = ablation_checkboxes["View direction"].active
            folder_name = construct_folder_name(folder_data)
            images = folders[folder_name]

        screen.fill(settings.Color.BACKGROUND.value)
        images[image_idx].draw(screen)
        play_button.draw(screen)
        arrows_buttons.display(screen)
        samples_checkboxes.display(screen)
        ablation_checkboxes.display(screen)
        if ablation_checkboxes.is_lock:
            for lock in locks:
                lock.draw(screen)
        if play:
            time.sleep(play_speed)
            image_idx = set_idx(image_idx, max_idx, Indexing.NEXT)
        pygame.display.update()


if __name__ == "__main__":
    lego()
