import pygame
import settings
import os
from enum import Enum
from collections import defaultdict
from typing import Optional


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Image:
    """Stores image, its attributes and draws it."""

    def __init__(
        self,
        image_path: str,
        x: int = 0,
        y: int = 0,
        scale: float = 1,
        border_size: int = 0,
    ) -> None:
        """Load an image from given path.

        Args:
            image_path: path to an image.
            x: position the image center on the x coordinate.
            y: position the image center on the y coordinate.
            scale: reduce or enlarge image.
            border_size: display black border around the image when drawing.
        """
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
    """Creates all necessary button functionality."""

    def __init__(
        self,
        text: str = "Button",
        x: int = settings.SCREEN_SIZE.mid_x,
        y: int = settings.SCREEN_SIZE.mid_y,
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
        """Creates button with give properties.

        Args:
            text: Text that will be displayed at the center of the button.
            x: position the image center on the x coordinate.
            y: position the image center on the y coordinate.
            width: width of the button.
            height: height of the button.
            font: font of the displayed text.
            text_color: color of the displayed text.
            color: default color of the button.
            shadow_color: color of the buttons shadow.
            inactive_color: color of the button when button is in inactive state.
            current_color: color of the button if it's selected with arrow keys (when used in Navigation)
            active_and_current_color: color of the button if button is active and selected with the arrow keys.
            active: state of the button upon initialization.
            on_hover: whether to display pop effect upon mouse hover.
        """
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
        self.action = False
        self.is_lock = False
        self.active = active

        if on_hover:
            self.hover_size = 2
            self.hover_pop = 2
        else:
            self.hover_size = 0
            self.hover_pop = 0

    def get_color(self) -> tuple[int, int, int]:
        """Get color depending on the state of the button."""
        if self.active and self.current:
            return self.active_and_current_color
        elif self.current:
            return self.current_color
        elif self.active:
            return self.active_color
        else:
            return self.inactive_color

    def check_clicked(self) -> bool:
        """Check and set flags if button was pressed using mouse."""
        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.button.collidepoint(pos) and left_click and not self.clicked:
            self.clicked = True
        if left_click == 0 and self.clicked:
            self.clicked = False
            return True
        return False

    def check_pressed(self, event: pygame.event.EventType):
        """Check and set flags if button was pressed using keyboard."""
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

    def set_action(self, event: pygame.event.EventType) -> bool:
        """Checks whether button was pressed and if action is possible.

        Args:
            event: captured event in pygame event loop.

        Returns:
            self.action: if button was clicked/pressed.
        """

        if self.is_lock:
            return False
        if self.check_pressed(event) or self.check_clicked():
            self.action = True
        else:
            self.action = False
        return self.action

    def check_down(self) -> bool:
        """Check if either flag representing usage of the button is True."""
        return self.clicked or self.pressed

    def lock(self):
        """Set button to locked state."""
        self.is_lock = True

    def unlock(self):
        """Set button to unlocked state."""
        self.is_lock = False

    def is_popup(self) -> bool:
        """Check if button is suppossed to popup."""
        pos = pygame.mouse.get_pos()
        if self.button.collidepoint(pos) or self.current:
            return True
        return False

    def set_size(self):
        """Manage graphical effects of popup or button being pressed."""
        if self.is_lock:
            return
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
        """Display button layer by layer.

        1. Shadow
        2. Button
        3. Text
        """
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
        draw_text(
            text=self.text,
            text_color=self.text_color,
            font=self.font,
            x=self.button.center[0],
            y=self.button.center[1],
            screen=screen,
        )


class ButtonLayout:
    """Create multiple buttons and handle their interactions.

    Easily manage their position by providing the x,y of the layout
    and wanted distances between buttons.
    Manage interactions using only one call.
    """

    def __init__(
        self,
        texts: list[str],
        active_ids: list[int],
        distance: int,
        x: int = settings.SCREEN_SIZE.mid_x,
        y: int = settings.SCREEN_SIZE.mid_y,
        height: int = 50,
        width: int = 400,
        center: bool = True,
        orientation: Orientation = Orientation.VERTICAL,
        inactive_color: tuple[int, int, int] = settings.Color.GRAY.value,
    ):
        """
        Initalize buttons based on provided properties.

        Args:
            texts: Texts used to create buttons in provided order.
            active_ids: Which buttons should be active upon initialization.
            distance: distance between centers of the buttons.
            x: x coordinate of the (upperleft corner)/(center) of the layout.
            y: y coordinate of the (upperleft corner)/(center) of the layout.
            height: height of the single button.
            width: width of the single button.
            center: whether x,y coordinates will be upperleft corner or center of layout.
            orientation: whether to create layout vertically or horizontally.
            inactive_color: color of the buttons in inactive state.
        """
        self.num_buttons = len(texts)
        self.buttons = {}
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
            self.buttons[text] = Button(
                text=str(text),
                width=width,
                y=self.start_y,
                x=self.start_x,
                height=height,
                active=(i in active_ids),
                inactive_color=inactive_color,
            )
            if orientation == Orientation.HORIZONTAL:
                self.start_x += distance
            elif orientation == Orientation.VERTICAL:
                self.start_y += distance

    def __getitem__(self, button: Optional[str | int]) -> Button:
        """Access each button using bracket notation.

        Use either button index or the text that it stores.
        """
        if isinstance(button, str):
            return self.buttons[button]
        elif isinstance(button, int):
            return list(self.buttons.values())[button]
        else:
            raise TypeError(
                f"Expected value to be a str or int, got {type(button).__name__} instead."
            )

    def display(self, screen: pygame.SurfaceType):
        """Draw every button on screen."""
        for button in self.buttons.values():
            button.draw(screen)

    def get_active(self) -> Optional[Button]:
        """Return all buttons in active state."""
        for button in self.buttons.values():
            if button.active:
                return button

    def update(self, event: pygame.event.EventType) -> bool:
        """Check whether any button was pressed and set all buttons flags approprietly."""
        for button in self.buttons.values():
            if button.set_action(event):
                return True
        return False

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
    """Create layout of buttons that behaves like checkboxes."""

    def __init__(
        self,
        texts: list[str],
        active_ids: list[int],
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
        """
        Initalize checkboxes based on provided properties.

        Args:
            texts: Texts used to create checkboxes in provided order.
            active_ids: Which checkboxes should be active upon initialization.
            distance: distance between centers of the checkboxes.
            x: x coordinate of the (upperleft corner)/(center) of the layout.
            y: y coordinate of the (upperleft corner)/(center) of the layout.
            height: height of the single checkbox.
            width: width of the single checkbox.
            center: whether x,y coordinates will be upperleft corner or center of layout.
            orientation: whether to create layout vertically or horizontally.
            inactive_color: color of the checkbox in inactive state.
            multiple_choice: whether multiple checkboxes are allowed to be active at once.
        """
        self.distance = distance
        self.height = height
        self.width = width
        self.checkboxes = {}
        self.num_checkboxes = len(texts)
        self.multiple_choice = multiple_choice
        self.x = x
        self.y = y
        self.is_lock = False

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
            self.checkboxes[text] = Button(
                text=str(text),
                width=width,
                x=next_x,
                y=next_y,
                height=height,
                active=(i in active_ids),
                inactive_color=inactive_color,
            )
            if orientation == Orientation.HORIZONTAL:
                next_x += distance
            elif orientation == Orientation.VERTICAL:
                next_y += distance

    def __getitem__(self, checkbox: Optional[str | int]) -> Button:
        """Access each checkbox using bracket notation.

        Use either checkboxindex or the text that it stores.
        """
        if isinstance(checkbox, str):
            return self.checkboxes[checkbox]
        elif isinstance(checkbox, int):
            return list(self.checkboxes.values())[checkbox]
        else:
            raise TypeError(
                f"Expected value to be a str or int, got {type(checkbox).__name__} instead."
            )

    def get_active_checkboxes(self) -> list[Button]:
        """Return all checkboxes that are in active state."""
        active_checkboxes = []
        for checkbox in self.checkboxes.values():
            if checkbox.active:
                active_checkboxes.append(checkbox)
        return active_checkboxes

    def display(self, screen: pygame.SurfaceType):
        """Draw all the checkboxes on the screen."""
        for button in self.checkboxes.values():
            button.draw(screen)

    def deactivate_all_checkboxes(self):
        """Set all checkboxes to inactive state."""
        for checkbox in self.checkboxes.values():
            checkbox.active = False

    def update(self, event: pygame.event.EventType) -> bool:
        """Handle checkbox behavior, set checkboxes flags and return True if any checkbox was pressed.

        Default behavior sets only the clicked checkbox to be active, disabling others.
        If multiple option is set updates clicked checkbox independently of the others.
        """
        for _, checkbox in enumerate(self.checkboxes.values()):
            if checkbox.set_action(event):
                if self.multiple_choice:
                    checkbox.active = not checkbox.active
                else:
                    self.deactivate_all_checkboxes()
                    checkbox.active = True
                return True
        return False

    def lock(self):
        """Sets all checkboxes to locked state."""
        self.is_lock = True
        for checkbox in self.checkboxes.values():
            checkbox.lock()

    def unlock(self):
        """Sets all checkboxes to unlocked state."""
        self.is_lock = False
        for checkbox in self.checkboxes.values():
            checkbox.unlock()

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

        draw_text(
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


def draw_text(
    text,
    screen: pygame.Surface,
    x: int = settings.SCREEN_SIZE.mid_x,
    y: int = settings.SCREEN_SIZE.mid_y,
    center: bool = True,
    text_color: tuple[int, int, int] = settings.Color.BLACK.value,
    font: pygame.font.FontType = settings.main_font_small,
):
    """Draw text on the screen in wanted place.

    Args:
        text: Text to display.
        screen: surface that the text will be displayed on.
        x: x coordinate of the text on the surface.
        y: y coordinate of the text on the surface.
        center: whether to use x, y as the center coordinates (default: upperleft corner)
        text_color: color of the text.
        font: font used to display text.
    """
    text_obj = font.render(str(text), True, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)


def construct_folder_name(folder_data: dict[str, str]) -> str:
    """Construct folder name by extracting relevant data from provided dict."""
    pos_encoding = folder_data["pos_encoding"]
    view_dirs = folder_data["view_dirs"]
    n_samples = folder_data["n_samples"]
    folder_name = (
        f"lego_pos_encoding_{pos_encoding}_view_dirs_{view_dirs}_64_{n_samples}"
    )
    return folder_name


def construct_folder_name_mednerf(folder_data: dict[str, str]) -> str:
    """Construct folder name by extracting relevant data from provided dict."""
    dataset_name = folder_data["dataset_name"]
    model = folder_data["model"]
    aug = folder_data["aug"]
    fmaps = folder_data["fmaps"]
    folder_name = (
        f"{dataset_name}_{model}"
    )
    return folder_name


def load_images(folder_path: str) -> list[Image]:
    """Load all images from given folder into list."""
    images = []
    for image_name in sorted(os.listdir(folder_path)):
        image_path = os.path.join(folder_path, image_name)
        images.append(
            Image(
                image_path=image_path,
                scale=1.5,
                x=int(settings.SCREEN_SIZE.x * 2 / 6),
                y=settings.SCREEN_SIZE.mid_y - 50,
            )
        )
    return images


def load_all_folders(dataset_dir: str) -> dict[str, list[Image]]:
    """Create mapping dict {folder_path: images in that folder}."""
    folders = {}
    for folder_name in sorted(os.listdir(dataset_dir)):
        folder_path = os.path.join(dataset_dir, folder_name, "video_200000")
        images = load_images(folder_path=folder_path)
        folders[folder_name] = images
    return folders


def load_all_folders_mednerf(dataset_dir: str) -> dict[str, list[Image]]:
    """Create mapping dict {folder_path: images in that folder}."""
    folders = {}
    for folder_name in sorted(os.listdir(dataset_dir)):
        folder_path = os.path.join(dataset_dir, folder_name, "video_200000")
        images = load_images(folder_path=folder_path)
        folders[folder_name] = images
    return folders


class Indexing(Enum):
    PREVIOUS = 0
    NEXT = 1


def set_idx(image_idx: int, max_idx: int, direction: Indexing):
    """Set next index, loop in either side if size is exceeded."""
    if direction == Indexing.NEXT:
        return next_idx(image_idx, max_idx)
    elif direction == Indexing.PREVIOUS:
        return previous_idx(image_idx, max_idx)


def next_idx(image_idx: int, max_idx: int):
    return 0 if image_idx == max_idx else image_idx + 1


def previous_idx(image_idx: int, max_idx: int):
    return max_idx if image_idx == 0 else image_idx - 1


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
