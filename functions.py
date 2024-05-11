import datetime
import sqlite3
import settings
import random
import pygame


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
def next_idx(image_idx, max_idx):
    return 0 if image_idx == max_idx else image_idx + 1


def previous_idx(image_idx, max_idx):
    return max_idx if image_idx == 0 else image_idx - 1
