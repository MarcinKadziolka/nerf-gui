import pygame
import functions
import settings
from enum import Enum
from collections import defaultdict


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Image:
    def __init__(
        self,
        image_path: str,
        x: int = 0,
        y: int = 0,
        scale: float = 1,
        border_size: int = 2,
    ) -> None:
        self.x = x
        self.y = y
        self.border_size = border_size
        self.image = pygame.transform.scale_by(pygame.image.load(image_path), scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self, screen: pygame.SurfaceType):
        screen.blit(self.image, self.rect)
        if self.border_size > 0:
            pygame.draw.rect(
                self.image,
                (0, 0, 0),
                [
                    0,
                    0,
                    self.width,
                    self.height,
                ],
                self.border_size,
            )


class Button:
    def __init__(
        self,
        text: str = "Button",
        y: int = settings.SCREEN_SIZE.mid_y,
        x: int = settings.SCREEN_SIZE.mid_x,
        width: int = 400,
        height: int = 50,
        font: pygame.font.FontType = settings.main_font_small,
        text_color: tuple = settings.Color.BLACK.value,
        color: tuple[int, int, int] = settings.Color.WHITE.value,
        shadow_color: tuple[int, int, int] = settings.Color.BLACK.value,
        inactive_color: tuple[int, int, int] = settings.Color.GRAY.value,
        current_color: tuple[int, int, int] = settings.Color.GREEN.value,
        active_and_current_color: tuple[
            int, int, int
        ] = settings.Color.LIGHT_GREEN.value,
        active: bool = False,
        on_hover: bool = True,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = pygame.Rect(0, 0, width, height)
        self.shadow = pygame.Rect(0, 0, width, height)
        self.hitbox = pygame.Rect(0, 0, width, height)
        self.hitbox.center = x, y
        self.button.center = x, y
        self.shadow.center = x, y + 5
        self.border_radius = 5

        self.active_color = color
        self.shadow_color = shadow_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.current_color = current_color
        self.active_and_current_color = active_and_current_color

        self.text = text
        self.font = font

        self.clicked = False
        self.pressed = False
        self.current = False
        self.active = active

        if on_hover:
            self.hover_size = 2
            self.hover_pop = 2
        else:
            self.hover_size = 0
            self.hover_pop = 0

    def get_color(self):
        if self.active and self.current:
            return self.active_and_current_color
        elif self.current:
            return self.current_color
        elif self.active:
            return self.active_color
        else:
            return self.inactive_color

    def check_clicked(self):
        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.button.collidepoint(pos) and left_click and not self.clicked:
            self.clicked = True
        if left_click == 0 and self.clicked:
            self.clicked = False
            return True
        return False

    def check_pressed(self, event: pygame.event.EventType):
        if not self.current:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not self.pressed:
                self.pressed = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            if self.pressed:
                self.pressed = False
                return True
        return False

    def check_action(self, event: pygame.event.EventType):
        return self.check_pressed(event) or self.check_clicked()

    def check_down(self):
        return self.clicked or self.pressed

    def is_popup(self):
        pos = pygame.mouse.get_pos()
        if self.button.collidepoint(pos) or self.current:
            return True
        return False

    def set_size(self):
        self.button = pygame.Rect(0, 0, self.width, self.height)
        self.button.center = self.x, self.y
        if self.check_down():
            self.button.center = self.x, self.y + 5 - self.hover_pop
        elif self.is_popup():
            self.button = pygame.Rect(
                0, 0, self.width + self.hover_size, self.height + self.hover_size
            )
            self.button.center = (self.x, self.y - self.hover_pop)

    def draw(self, screen: pygame.SurfaceType):
        pygame.draw.rect(
            screen,
            self.shadow_color,
            self.shadow,
            border_radius=self.border_radius,
        )
        self.set_size()
        pygame.draw.rect(
            screen,
            self.get_color(),
            self.button,
            border_radius=self.border_radius,
        )
        functions.draw_text(
            text=self.text,
            text_color=self.text_color,
            font=self.font,
            x=self.button.center[0],
            y=self.button.center[1],
            screen=screen,
        )


class ButtonLayout:
    def __init__(
        self,
        texts: list[str],
        active: set[int],
        distance: int,
        x: int = settings.SCREEN_SIZE.mid_x,
        y: int = settings.SCREEN_SIZE.mid_y,
        height: int = 50,
        width: int = 400,
        center: bool = True,
        orientation: Orientation = Orientation.VERTICAL,
        inactive_color: tuple[int, int, int] = settings.Color.GRAY.value,
    ):
        self.num_buttons = len(texts)
        self.buttons = []
        self.active_ids = active
        self.start_x = x
        self.start_y = y

        if center:
            half_length = int(((self.num_buttons - 1) * distance) / 2)
            if orientation == Orientation.HORIZONTAL:
                self.start_x = x - half_length
            elif orientation == Orientation.VERTICAL:
                self.start_y = y - half_length
            else:
                raise Exception("Invalid orientation")

        for i, text in enumerate(texts):
            self.buttons.append(
                Button(
                    text=str(text),
                    width=width,
                    y=self.start_y,
                    x=self.start_x,
                    height=height,
                    active=(i in self.active_ids),
                    inactive_color=inactive_color,
                )
            )
            if orientation == Orientation.HORIZONTAL:
                self.start_x += distance
            elif orientation == Orientation.VERTICAL:
                self.start_y += distance

    def display(self, screen: pygame.SurfaceType):
        for button in self.buttons:
            button.draw(screen)

    def update(self, event: pygame.event.EventType):
        for button in self.buttons:
            if button.check_action(event):
                return button

    def __len__(self):
        return len(self.buttons)


class Navigation:
    def __init__(self, layouts: list, navigation: defaultdict = defaultdict(tuple, {})):
        self.layout_id = 0
        self.button_id = 0
        self.layouts = layouts
        self.layouts[self.layout_id].buttons[self.button_id].current = True
        self.navigation = navigation

    def get_next_id(self, event: pygame.event.EventType):
        curr_layout = self.layouts[self.layout_id]
        n_buttons = len(curr_layout)
        if event.type != pygame.KEYDOWN:
            return
        if target := self.navigation[(self.layout_id, self.button_id, event.key)]:
            self.layout_id, self.button_id = target[0], target[1]
            return
        if event.key in (pygame.K_DOWN, pygame.K_RIGHT):
            if self.button_id + 1 < n_buttons:
                self.button_id += 1
        elif event.key in (pygame.K_UP, pygame.K_LEFT):
            if self.button_id - 1 >= 0:
                self.button_id -= 1

    def update(self, event: pygame.event.EventType):
        self.layouts[self.layout_id].buttons[self.button_id].current = False
        self.get_next_id(event)
        self.layouts[self.layout_id].buttons[self.button_id].current = True


class CheckBoxLayout:
    def __init__(
        self,
        texts: list[str],
        active: set[int],
        distance: int,
        x: int = settings.SCREEN_SIZE.mid_x,
        y: int = settings.SCREEN_SIZE.mid_y,
        height: int = 50,
        width: int = 400,
        center: bool = True,
        orientation: Orientation = Orientation.VERTICAL,
        inactive_color: tuple[int, int, int] = settings.Color.GRAY.value,
        multiple_choice: bool = False,
    ) -> None:
        self.distance = distance
        self.height = height
        self.width = width
        self.num_checkboxes = len(texts)
        self.checkboxes = []
        self.active_ids = active
        self.multiple_choice = multiple_choice
        self.x = x
        self.y = y

        if center:
            half_length = int(((self.num_checkboxes - 1) * distance) / 2)
            if orientation == Orientation.HORIZONTAL:
                self.x = x - half_length
            elif orientation == Orientation.VERTICAL:
                self.y = y - half_length
            else:
                raise Exception("Invalid orientation")
        next_x = self.x
        next_y = self.y

        for i, text in enumerate(texts):
            self.checkboxes.append(
                Button(
                    text=str(text),
                    width=width,
                    x=next_x,
                    y=next_y,
                    height=height,
                    active=(i in self.active_ids),
                    inactive_color=inactive_color,
                )
            )
            if orientation == Orientation.HORIZONTAL:
                next_x += distance
            elif orientation == Orientation.VERTICAL:
                next_y += distance

    def display(self, screen: pygame.SurfaceType):
        for button in self.checkboxes:
            button.draw(screen)

    def update(self, event: pygame.event.EventType):
        for i, button in enumerate(self.checkboxes):
            if button.check_action(event):
                if self.multiple_choice:
                    button.active = not button.active
                    if button.active:
                        self.active_ids.add(i)
                    else:
                        self.active_ids.discard(i)
                else:
                    self.active_ids.clear()
                    button.active = True
                    self.active_ids.add(i)
                    for other_button in self.checkboxes:
                        if other_button != button:
                            other_button.active = False
                break

    def __len__(self):
        return len(self.checkboxes)


class TextField:
    def __init__(
        self,
        font: pygame.font.FontType,
        text_color: tuple[int, int, int],
        active_color: tuple[int, int, int],
        inactive_color: tuple[int, int, int],
        prompt_text: str,
        x: int = settings.SCREEN_SIZE.mid_x,
        y: int = settings.SCREEN_SIZE.mid_y,
        width: int = 500,
        height: int = 50,
        numeric_only: bool = False,
    ):
        self.active = True
        self.user_input = prompt_text
        self.input_field = pygame.Rect(x, y, width, height)
        self.input_field.center = x, y
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.font = font

        self.fast_delete_activation = 500
        self.delete_speed = 50
        self.delete_wait = self.fast_delete_activation

        self.dont_register = [pygame.K_RETURN, pygame.K_BACKSPACE, pygame.K_ESCAPE]
        self.numeric_only = numeric_only

    def get_event(self, event: pygame.event.EventType):
        if not self.active or event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
            self.backspace_timer = pygame.time.get_ticks()

        if event.key in self.dont_register:
            return

        if self.numeric_only and event.unicode.isnumeric():
            self.user_input += event.unicode
        else:
            self.user_input += event.unicode

    def update(self, screen: pygame.SurfaceType):
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, color, self.input_field, border_radius=50)

        functions.draw_text(
            text=self.user_input,
            font=self.font,
            text_color=self.text_color,
            x=self.input_field.center[0],
            y=self.input_field.center[1],
            screen=screen,
        )

        self.handle_backspace()

    def handle_backspace(self):
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            if pygame.time.get_ticks() - self.backspace_timer > self.delete_wait:
                self.delete_wait = self.delete_speed
                self.backspace_timer = pygame.time.get_ticks()
                self.user_input = self.user_input[:-1]
        else:
            self.delete_wait = self.fast_delete_activation
