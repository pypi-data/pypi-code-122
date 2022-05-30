#!/usr/bin/env python3
from typing import Optional

from pygame import display

from tools_for_pygame.constants import ABSOLUTE
from tools_for_pygame.element import Element, AniElement
from tools_for_pygame.mathf import Pos, Size
from tools_for_pygame.type_hints import _size


class GUIElement(Element):
    """
    GUIElement(Element)

    Type: class

    Description: this class adds some functionality to the element that
        is related to GUI

    Args:
        'layout' (GUILayout?): the layout the element resembles to, see
            help(pgt.gui.GUILayout) for more info
        'position_mode' (int): this can be either pgt.ABSOLUTE (default)
            or pgt.AUTOMATIC; the latter positions the elements
            automatically only if the layout is set and the pos_point is
            pgt.UL
        'rel_size' (Size): percentage of the element's size relative to
            the layout or to the window if the layout is not set
            can be anything from 0 to 1 and None, if deactivated. The
            minimum size is set with the 'size' argument
        'margin_top' (int): the space from the top that the element
            should keep when position_mode is automatic
        'margin_bottom' (int): space from the bottom
        'margin_left' (int): space from the left
        'margin_right' (int): space from the right
        'app' (Any): an attribute that should be used to link the
            element with the application you're creating

    Attrs:
        'rel_size' (Size): see 'rel_size' in args
        'base_size' (Size): the minimum size of the element
        'layout' (GUILayout?): the layout the element resembles to
        'position_mode' (int): see 'position_mode' in args
        'margin_ul' (Pos): margin_top and margin_left
        'margin_dr' (Pos): margin_bottom and margin_right
        'true_size' (Size): the size without the padding
        'size' (Size): instead of returning only the size of the element,
            size here adds the padding, the setter sets the size not
            considering the padding

    Methods:
        set_layout(new_layout)
        _update_size()
    """
    def __init__(self,
                 layout: Optional["GUILayout"] = None,
                 position_mode: int = ABSOLUTE,
                 rel_size: _size = Size(None),
                 margin_top: int = 0,
                 margin_bottom: int = 0,
                 margin_left: int = 0,
                 margin_right: int = 0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rel_size = Size(rel_size)
        self.base_size = self._size
        self.layout = layout
        self.position_mode = position_mode
        self.margin_ul = round(Pos(margin_left,  margin_top))
        self.margin_dr = round(Pos(margin_right, margin_bottom))

    @property
    def margin_size(self):
        return Size(self.rect.size) + self.margin_ul + self.margin_dr

    def set_layout(self, new_layout: "GUILayout") -> None:
        """
        set_layout(self, new_layout)

        Type: method

        Description: changes the layout of the element and anchors the
            GUIElement to it if the element is not already anchored to
            something

        Args:
            'new_layout' (GUILayout): the new element's layout

        Return type: None
        """
        self.layout = new_layout
        if not self.is_anchored:
            self.anchor(new_layout, self._a_point)

    def _update_size(self):
        """Changes the size when 'rel_size' is not None"""
        if self.layout:
            max_size = self.layout.size
        else:
            max_size = Size(display.get_window_size())

        new_size = self.size

        if self.rel_size.w is not None:
            if 0 <= self.rel_size.w <= 1:
                new_size.w = max_size.w * self.rel_size.w
            else:
                new_size.w = max_size.w + self.rel_size.w
            if new_size.w < self._size.w:
                new_size.w = self._size.w

        if self.rel_size.h is not None:
            if 0 <= self.rel_size.h <= 1:
                new_size.h = max_size.h * self.rel_size.h
            else:
                new_size.h = max_size.h + self.rel_size.h
            if new_size.h < self._size.h:
                new_size.h = self._size.h

        self.size = new_size

    def draw(self, *args, **kwargs) -> None:
        self._update_size()
        super().draw(*args, **kwargs)


class GUIAniElement(GUIElement, AniElement):
    pass
