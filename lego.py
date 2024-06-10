import settings
import time
import pygame
import mednerf
from helpers import (
    Button,
    ButtonLayout,
    CheckBoxLayout,
    Image,
    Orientation,
    Indexing,
    draw_text,
    load_all_folders,
    construct_folder_name,
    set_idx,
    handle_arrows,
    handle_play_flag,
)


def initialize_layouts():
    checkboxes_x = settings.SCREEN_SIZE.right_third
    checkboxes_y = 600
    small_button_width = 70
    coarse_n_samples = CheckBoxLayout(
        ["0", "64"],
        active_ids=[1],
        width=small_button_width,
        distance=settings.HORIZONTAL_DISTANCE + 10,
        x=checkboxes_x,
        y=checkboxes_y - 70,
        orientation=Orientation.HORIZONTAL,
    )
    n_samples = CheckBoxLayout(
        ["16", "32", "64", "128"],
        active_ids=[3],
        width=small_button_width,
        distance=settings.HORIZONTAL_DISTANCE + 10,
        x=checkboxes_x,
        y=checkboxes_y,
        orientation=Orientation.HORIZONTAL,
    )
    ablation = CheckBoxLayout(
        ["Pos encoding", "View direction"],
        active_ids=[0, 1],
        width=350,
        distance=settings.VERTICAL_DISTANCE,
        x=checkboxes_x,
        y=400,
        orientation=Orientation.VERTICAL,
        multiple_choice=True,
    )
    locks_x = int(ablation.x - ablation.width / 2 + 20)
    lock1 = Image(
        "lock.png",
        x=locks_x,
        border_size=0,
        y=ablation.y - 3,
    )
    lock2 = Image(
        "lock.png",
        x=locks_x,
        border_size=0,
        y=ablation.y + ablation.distance - 3,
    )
    locks = [lock1, lock2]
    media_buttons_y = int(
        settings.SCREEN_SIZE.mid_y - 50 + 600 / 2 + settings.HORIZONTAL_DISTANCE
    )
    arrows = ButtonLayout(
        ["<", ">"],
        active_ids=[0, 1],
        width=small_button_width,
        distance=settings.HORIZONTAL_DISTANCE,
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
    return coarse_n_samples, n_samples, ablation, locks, arrows, play_button


# initialize lego
(
    coarse_samples_checkboxes,
    samples_checkboxes,
    ablation_checkboxes,
    locks,
    arrows_buttons,
    play_button,
) = initialize_layouts()
folder_data = {
    "dataset_dir": "sampling_dataset",
    "pos_encoding": ablation_checkboxes["Pos encoding"].active,
    "view_dirs": ablation_checkboxes["View direction"].active,
    "n_samples": samples_checkboxes.get_active_checkboxes()[0].text,
    "coarse_n_samples": coarse_samples_checkboxes.get_active_checkboxes()[0].text,
}

folders = load_all_folders("sampling_dataset")
folder_name = construct_folder_name(folder_data)
images = folders[folder_name]
image_idx = 0
max_idx = len(images) - 1
play = False
play_speed = 0.07


def lego_run(project_checkboxes, screen):
    global play
    global image_idx
    global images
    run = True
    active_samples_checkbox = samples_checkboxes.get_active_checkboxes()[0]
    active_coarse_samples_checkbox = coarse_samples_checkboxes.get_active_checkboxes()[
        0
    ]
    total_num_of_samples = int(active_coarse_samples_checkbox.text) + int(
        active_samples_checkbox.text
    )
    while run:
        update_folder = False
        for event in pygame.event.get():
            folder_name = None
            index_direction = None

            if (
                samples_checkboxes.update(event)
                or ablation_checkboxes.update(event)
                or coarse_samples_checkboxes.update(event)
            ):
                update_folder = True
            if project_checkboxes.update(event):
                if project_checkboxes["Mednerf"].active:
                    mednerf.mednerf_run(project_checkboxes, screen)

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
            active_coarse_samples_checkbox = (
                coarse_samples_checkboxes.get_active_checkboxes()[0]
            )
            if (
                active_samples_checkbox.text == "128"
                and active_coarse_samples_checkbox.text == "64"
            ):
                ablation_checkboxes.unlock()
            else:
                ablation_checkboxes["Pos encoding"].active = True
                ablation_checkboxes["View direction"].active = True
                ablation_checkboxes.lock()

            folder_data["coarse_n_samples"] = active_coarse_samples_checkbox.text
            folder_data["n_samples"] = active_samples_checkbox.text
            folder_data["pos_encoding"] = ablation_checkboxes["Pos encoding"].active
            folder_data["view_dirs"] = ablation_checkboxes["View direction"].active
            folder_name = construct_folder_name(folder_data)
            images = folders[folder_name]
            total_num_of_samples = int(active_coarse_samples_checkbox.text) + int(
                active_samples_checkbox.text
            )

        screen.fill(settings.Color.BACKGROUND.value)
        images[image_idx].draw(screen)
        play_button.draw(screen)
        arrows_buttons.display(screen)

        draw_text(
            "Coarse: ",
            screen,
            coarse_samples_checkboxes.x - 230,
            coarse_samples_checkboxes.y,
        )
        draw_text(
            "Fine: ",
            screen,
            coarse_samples_checkboxes.x - 230,
            samples_checkboxes.y,
        )
        draw_text(
            f"Total number of samples: {total_num_of_samples}",
            screen,
            coarse_samples_checkboxes.x - 50,
            samples_checkboxes.y + 100,
        )

        coarse_samples_checkboxes.display(screen)
        samples_checkboxes.display(screen)
        project_checkboxes.display(screen)
        ablation_checkboxes.display(screen)
        if ablation_checkboxes.is_lock:
            for lock in locks:
                lock.draw(screen)
        if play:
            time.sleep(play_speed)
            image_idx = set_idx(image_idx, max_idx, Indexing.NEXT)
        pygame.display.update()
