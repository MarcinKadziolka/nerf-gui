from dataclasses import dataclass
import pygame
from enum import Enum

pygame.init()


@dataclass
class ScreenSize:
    x: int
    y: int

    @property
    def mid_x(self) -> int:
        return int(self.x / 2)

    @property
    def mid_y(self) -> int:
        return int(self.y / 2)

    @property
    def left_third(self) -> int:
        return int(self.x / 6)

    @property
    def middle_third(self) -> int:
        return int(self.x / 2)

    @property
    def right_third(self) -> int:
        return int(self.x * 5 / 6)


infoObject = pygame.display.Info()
SCREEN_SIZE = ScreenSize(infoObject.current_w, infoObject.current_h)

DISTANCE = 80
SLEEP_DURATION = 0.1

main_font = pygame.font.SysFont("rasa", 80)
main_font_small = pygame.font.SysFont("rasa", 50)
equation_font_small = pygame.font.SysFont("rasa", 70)


class Color(Enum):
    BACKGROUND = [167, 199, 250]
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (127, 255, 212)
    LIGHT_GREEN = (179, 255, 230)
    LIGHT_RED = (180, 190, 250)
    GRAY = (220, 220, 220)
