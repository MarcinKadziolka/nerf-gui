import settings
import pygame
import classes
import os
from os import listdir


def draw_text(
    text,
    screen: pygame.Surface,
    x: int = settings.SCREEN_SIZE.mid_x,
    y: int = settings.SCREEN_SIZE.mid_y,
    center: bool = True,
    text_color: tuple[int, int, int] = settings.Color.BLACK.value,
    font: pygame.font.FontType = settings.main_font_small,
):
    text_obj = font.render(str(text), True, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)


def construct_folder_path(folder_data: dict[str, str]):
    dataset_dir = folder_data["dataset_dir"]
    pos_encoding = folder_data["pos_encoding"]
    view_dirs = folder_data["view_dirs"]
    n_samples = folder_data["n_samples"]
    folder_name = (
        f"lego_pos_encoding_{pos_encoding}_view_dirs_{view_dirs}_64_{n_samples}"
    )
    folder_path = os.path.join(dataset_dir, folder_name, "video_200000")
    return folder_path


def load_images(folder_path: str) -> list[classes.Image]:
    images = []
    for image_name in sorted(os.listdir(folder_path)):
        image_path = os.path.join(folder_path, image_name)
        images.append(
            classes.Image(
                image_path=image_path,
                scale=1.5,
                x=int(settings.SCREEN_SIZE.x * 2 / 6),
                y=settings.SCREEN_SIZE.mid_y - 50,
            )
        )
    return images


def next_idx(image_idx, max_idx):
    return 0 if image_idx == max_idx else image_idx + 1


def previous_idx(image_idx, max_idx):
    return max_idx if image_idx == 0 else image_idx - 1
