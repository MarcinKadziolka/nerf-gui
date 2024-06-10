import settings
import time
import pygame
from helpers import (
    Button,
    ButtonLayout,
    CheckBoxLayout,
    Image,
    Orientation,
    Indexing,
    load_all_folders_mednerf,
    construct_folder_name_mednerf,
    set_idx,
    handle_arrows,
    handle_play_flag,
)

model_dict = {
    "Mednerf": "mednerf",
    "HyperNeRFGAN": "nerfgan",
    "HNGAN + aug": "nerfgan_aug",
    "HNGAN + aug + disc": "nerfgan_aug_gen",
}


def initialize_layouts_mednerf():
    checkboxes_x = settings.SCREEN_SIZE.right_third
    checkboxes_y = 800
    small_button_width = 70
    n_samples = CheckBoxLayout(
        ["Mednerf", "HyperNeRFGAN", "HNGAN + aug", "HNGAN + aug + disc"],
        active_ids=[0],
        width=350,
        distance=settings.HORIZONTAL_DISTANCE + 10,
        x=checkboxes_x,
        y=checkboxes_y,
        orientation=Orientation.VERTICAL,
    )
    ablation = CheckBoxLayout(
        ["Chest", "Knee"],
        active_ids=[0],
        width=350,
        distance=settings.HORIZONTAL_DISTANCE + 10,
        x=checkboxes_x,
        y=400,
        orientation=Orientation.VERTICAL,
        multiple_choice=False,
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
        settings.SCREEN_SIZE.mid_y - 50 + 800 / 2 + settings.HORIZONTAL_DISTANCE
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
    return n_samples, ablation, locks, arrows, play_button


samples_checkboxes, ablation_checkboxes, locks, arrows_buttons, play_button = (
    initialize_layouts_mednerf()
)
folder_data = {
    "dataset_dir": "mednerf_dataset",
    "dataset_name": "chest" if ablation_checkboxes["Chest"].active else "knee",
    "model": "mednerf",  ###samples_checkboxes.get_active_checkboxes()[0].text,
    "aug": True,
    "fmaps": True,
}

# load all images beforehand
# to allow for smooth changes during "rendering"

# warning: load_folder function calls load_images
# which scales images by 1.5 with hardcoded value
# also the position of the image is fixed
# pygame also has function scale() that scales
# to precise number (500, 500), instead of by the factor
# maybe it can be used to match lego and mednerf sizes
folders = load_all_folders_mednerf("mednerf_dataset")
folder_name = construct_folder_name_mednerf(folder_data)
images = folders[folder_name]
image_idx = 0
max_idx = len(images) - 1
run = True
play = False
play_speed = 0.07


def mednerf_run(project_checkboxes, screen):
    global play
    global images
    global image_idx
    run = True
    while run:
        update_folder = False
        # for loop iterating over every event that pygame catches
        # if user does not do any action (no mouse movement, no keyboard action) this is skipped
        for event in pygame.event.get():
            folder_name = None
            index_direction = None

            # .update() function in layouts returns True
            # only if any of the checkbox or button was activated
            # if that happened we know something changed, and can act on it later
            if samples_checkboxes.update(event) or ablation_checkboxes.update(event):
                update_folder = True

            if project_checkboxes.update(event):
                if project_checkboxes["Sampling"].active:
                    return
            # play and play_button is passed
            # because clicking any of the arrow
            # stops the animation
            play, index_direction = handle_arrows(
                arrows_buttons, play, play_button, event
            )

            play = handle_play_flag(play_button, play, event)

            # here every keyboard event is catched
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

        # act upon change registered earlier
        if update_folder:
            ### CUSTOM LOCKING
            # lock position encoding and viewing direction
            # for any other number of samples than 128
            # because it's the only n_samples that these ablations were done for
            active_samples_checkbox = samples_checkboxes.get_active_checkboxes()[0]
            # TODO LATER
            # if active_samples_checkbox.text == "128":
            #     ablation_checkboxes.unlock()
            # else:
            #     ablation_checkboxes["Pos encoding"].active = True
            #     ablation_checkboxes["View direction"].active = True
            #     ablation_checkboxes.lock()
            ### END OF CUSTOM LOCKING

            # update data that possibly changed
            folder_data["model"] = model_dict.get(active_samples_checkbox.text)

            # access individual checkboxes or buttons using bracket notation
            # either the checkbox text or its index in the list
            # can be used to retrieve it from the layout
            # TODO LATER
            folder_data["dataset_name"] = (
                "chest" if ablation_checkboxes["Chest"].active else "knee"
            )
            # folder_data["dataset_name"] = ablation_checkboxes["View direction"].active
            folder_name = construct_folder_name_mednerf(folder_data)
            images = folders[folder_name]

        screen.fill(settings.Color.BACKGROUND.value)
        images[image_idx].draw(screen)
        play_button.draw(screen)
        arrows_buttons.display(screen)
        samples_checkboxes.display(screen)
        ablation_checkboxes.display(screen)
        project_checkboxes.display(screen)

        # display locks to inform user that these options are locked
        if ablation_checkboxes.is_lock:
            for lock in locks:
                lock.draw(screen)
        if play:
            time.sleep(play_speed)
            image_idx = set_idx(image_idx, max_idx, Indexing.NEXT)
        pygame.display.update()
