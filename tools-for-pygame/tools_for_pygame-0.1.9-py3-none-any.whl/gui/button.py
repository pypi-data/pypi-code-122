#!/usr/bin/env python3

import time
from typing import Optional, Callable, Iterable, Any

import pygame.mixer

from .label import Label
from .gui_element import GUIElement
from tools_for_pygame.ani import AniBase
from tools_for_pygame.constants import BUTTON_NORMAL, BUTTON_CLICK, BUTTON_HOVER
from tools_for_pygame.element import MouseInteractionAniElement, Element


class Button(MouseInteractionAniElement, GUIElement):
    """
    Button(MouseInteractionAniElement)

    Type: class

    Description: a customizable button that can run a function
        when clicked

    Args:
        'text_label' (Label?): a Label that gets drawn in front of
            the button
        'hint_bg' (Element?): background of the hint shown when the
            mouse is hovering the button
        'hint_label' (Label?): text of the hint
        'hint_delay' (float): time in seconds to wait before showing
            the hint
        'func' (Callable): function to run when the button is pressed
        'func_args' (Iterable?): *args of the function
        'func_kwargs' (dict?): **kwargs of the function
        'func_as_method' (bool): makes the 'func' argument a method by
            adding the button object as the first positional argument
            of the function
        'button' (int): which mouse button should activate the button
            1 - left, 2 - middle, 3 - right
        'sound' (pygame.mixer.Sound?): a sound to play when the
            button is clicked

    Attrs:
        'func' (Callable?): see 'func' in args
        'fargs' (Iterable?): see 'func_args' in args
        'fkwargs' (dict?): see 'func_kwargs' in args
        'func_as_method' (bool): see 'func_as_method' in args
        'button' (int): see 'button' in args
        'sound' (pygame.mixer.Sound?): see 'sound' in args
        'force_state' (int?): which state is shown of the button,
            if set to None the current one is shown.
            The module provides three constants BUTTON_NORMAL,
            BUTTON_HOVER and BUTTON_CLICK
        'label' (Label?): see 'label' in args
        'app' (Any): see 'app' in args

    Properties:
        'button_clicked' (bool, readonly): if the button is clicked
            with the assigned mouse button

    Methods:
        - run()
        - auto_run()

    Notes:
        - an animation called '_on_click' will start when a button is
          clicked
        - an animation called '_on_hover_from_click' will start when the
          button is unclicked but still hovered
        - an animation called '_on_hover' will start when the button is
          hovered and replaces '_on_hover_from_click' if not set
        - an animation called '_from_hover' will start when the button
          is no longer hovered and the cursor was not clicking when it
          left the button
        - an animation called '_from_click' will start start when the
          button is no longer hovered and the cursor was clicking when
          it left the button
        - an animation called '_normal' will start when the button is
          no longer hovered, replaces '_from_click' and or '_from_hover'
          if not set. If both '_from_hover' and '_from_click' are set,
          this animation never starts
    """
    def __init__(self,
                 text_label: Optional[Label] = None,
                 hint_bg: Optional[Element] = None,
                 hint_label: Optional[Label] = None,
                 hint_delay: float = 1,
                 func: Optional[Callable] = None,
                 func_args: Optional[Iterable] = None,
                 func_kwargs: Optional[dict] = None,
                 func_as_method: bool = False,
                 button: int = 0,
                 sound: Optional[pygame.mixer.Sound] = None,
                 app: Any = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__was_hovered = False
        self.__was_clicked = False
        self.__started_ani = ""

        self.func = func
        if func_args is None: func_args = []
        self.fargs = func_args
        if func_kwargs is None: func_kwargs = {}
        self.fkwargs = func_kwargs
        self.func_as_method = func_as_method

        self.button = button
        self.sound = sound

        self.__pressed = False
        self.force_state = None

        self.label = text_label
        if self.label: self.label.anchor(self)

        self.hint_bg = hint_bg
        self.hint_label = hint_label
        if self.hint_bg and self.hint_label:
            self.hint_label.anchor(self.hint_bg)
        self.start_hover = None
        self.hint_delay = hint_delay
        self.app = app

    @property
    def button_clicked(self):
        return self.clicked[self.button]

    def run(self) -> None:
        """Runs the button's function"""
        if not self.func:
            return
        if self.func_as_method:
            self.func(self, *self.fargs, **self.fkwargs)
        else:
            self.func(*self.fargs, **self.fkwargs)

    def auto_run(self) -> bool:
        """
        Calls 'run' automatically and plays the sound, should be called
        every frame
        """
        if self.button_clicked:
            if not self.__pressed and self.sound is not None:
                pygame.mixer.Sound.play(self.sound)
            self.__pressed = True
            return True
        elif self.hovered:
            if self.__pressed:
                self.run()
                self.__pressed = False
                return True
        else:
            self.__pressed = False

        return False

    def draw(self, *args, **kwargs) -> None:
        hovered = self.hovered
        clicked = self.button_clicked

        if self.force_state:
            if self.force_state == BUTTON_NORMAL:
                hovered = clicked = False
            elif self.force_state == BUTTON_HOVER:
                hovered = True
                clicked = False
            elif self.force_state == BUTTON_CLICK:
                clicked = True

        if clicked and hasattr(self, "_on_click"):
            if not self._on_click.running and self.__started_ani != "_on_click":
                self._on_click.start()
                self.__started_ani = "_on_click"

        elif hovered and self.__was_clicked and hasattr(self, "_on_hover_from_click"):
            if not self._on_hover_from_click.running \
               and self.__started_ani != "_on_hover_from_click":
                self._on_hover_from_click.start()
                self.__started_ani = "_on_hover_from_click"

        elif hovered and hasattr(self, "_on_hover"):
            if not self._on_hover.running \
               and self.__started_ani not in ("_on_hover", "_on_hover_from_click"):
                self._on_hover.start()
                self.__started_ani = "_on_hover"

        elif self.__was_hovered and hasattr(self, "_from_hover"):
            if not self._from_hover.running \
               and self.__started_ani != "_from_hover":
                self._from_hover.start()
                self.__started_ani = "_from_hover"

        elif self.__was_clicked and hasattr(self, "_from_click"):
            if not self._from_click.running \
               and self.__started_ani != "_from_click":
                self._from_click.start()
                self.__started_ani = "_from_click"

        elif not clicked \
             and not hovered \
             and not self.__was_hovered \
             and not self.__was_clicked \
             and hasattr(self, "_normal"):
            if not self._normal.running \
               and self.__started_ani not in ("_normal", "_from_hover", "_from_click"):
                self._normal.start()
                self.__started_ani = "_normal"

        self.__was_hovered = False if clicked else hovered
        self.__was_clicked = clicked

        if self.hidden:
            self.start_hover = None
            return

        if self.hovered and self.start_hover is None:
            self.start_hover = time.perf_counter()
        elif not self.hovered or self.button_clicked:
            self.start_hover = None

        super().draw(*args, **kwargs)
        if self.label:
            self.label.draw(*args, **kwargs)

        if self.layout is None: return

        if self.hint_bg \
           and self.hint_label \
           and self.start_hover is not None \
           and time.perf_counter() - self.start_hover > self.hint_delay:
            self.layout._curr_button_hint = (
                id(self),
                self.hint_bg,
                self.hint_label
            )

        # Uses id to hide only its own hint
        elif self.layout._curr_button_hint is not None \
             and self.layout._curr_button_hint[0] == id(self):
            self.layout._curr_button_hint = None
