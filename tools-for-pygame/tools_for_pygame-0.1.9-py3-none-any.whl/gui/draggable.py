#!/usr/bin/env python3

from typing import Optional
import pygame.mouse
from .button import Button
from tools_for_pygame.element import MouseInteractionAniElement
from tools_for_pygame.mathf import Pos
from tools_for_pygame.type_hints import _pos


class Draggable(Button):
    """
    Draggable(Button)

    Type: class

    Description: an element that can be dragged around

    Args:
        'locked' (bool): if the element can be dragged or not
        'boundary_top' (int?): the top boundary that the element can
            never surpass
        'boundary_left' (int?): the left boundary
        'boundary_right' (int?): the right boundary
        'boundary_bottom' (int?): the bottom boundary
        'snap_pos' (Pos?): the position to set when the element is no
            longer dragged, if set to None the element is not moved

    Attrs:
        'dragging' (bool): whether the element is being dragged or not
        'drag_point' (Pos): the click point of the mouse relative to
            Draggable.pos
        'locked' (bool): see 'locked' in args
        'b_top' (int?): see 'boundary_top' in args
        'b_right' (int?): see 'boundary_right' in args
        'b_left' (int?): see 'boundary_left' in args
        'b_bottom' (int?): see 'boundary_bottom' in args
        'snap_pos' (Pos?): see 'snap_pos' in args

    Methods:
        - update()
        - _fix_pos()

    Nodes:
        - if the element has an animation called '_snap', it is started
          when the element needs to reach 'snap_pos' and stopped when
          the element is dragged again
    """
    def __init__(self,
                 locked: bool = False,
                 boundary_top: Optional[int] = None,
                 boundary_left: Optional[int] = None,
                 boundary_right: Optional[int] = None,
                 boundary_bottom: Optional[int] = None,
                 snap_pos: _pos = None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.dragging = False
        self.drag_point = Pos(0, 0)
        self.locked = locked
        self.b_top = boundary_top
        self.b_right = boundary_right
        self.b_left = boundary_left
        self.b_bottom = boundary_bottom
        self.snap_pos = Pos(snap_pos) if snap_pos is not None else None
        self._fix_pos()
        if self.snap_pos is not None:
            if hasattr(self, "_snap"):
                self._snap.start()
            else:
                self.pos = self.snap_pos

    def _fix_pos(self) -> None:
        """Repositions the draggable inside the boundaries"""
        if self.b_top is not None and self.u < self.b_top:
            self.u = self.b_top
        if self.b_bottom is not None and self.d > self.b_bottom:
            self.d = self.b_bottom
        if self.b_left is not None and self.l < self.b_left:
            self.l = self.b_left
        if self.b_right is not None and self.r > self.b_right:
            self.r = self.b_right

    def update(self) -> None:
        """Updates the draggable's position when it's dragged"""
        if not self.dragging and self.button_clicked and not self.locked:
            self.dragging = True
            self.drag_point = self.get_mouse_pos() - self.pos
            if hasattr(self, "_snap"):
                self._snap.force_stop()
        elif not pygame.mouse.get_pressed(3)[self.button] and self.dragging:
            self.dragging = False
            self._fix_pos()
            if self.snap_pos is None:
                return
            if hasattr(self, "_snap"):
                self._snap.start()
            else:
                self.pos = self.snap_pos

        if self.dragging:
            self.pos = self.get_mouse_pos() - self.drag_point
            self._fix_pos()

    def draw(self, *args, **kwargs) -> None:
        self.update()
        super().draw(*args, **kwargs)
