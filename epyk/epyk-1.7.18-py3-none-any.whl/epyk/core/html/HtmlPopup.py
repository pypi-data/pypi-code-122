#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Union
from epyk.core.py import primitives

from epyk.core.html import Html
from epyk.core.css import Colors
from epyk.core.html.options import OptPanel
from epyk.core.js.html import JsHtmlPopup


class Popup(Html.Html):
  name = 'Popup Container'

  def __init__(self, page: primitives.PageModel, components: List[Html.Html], width: tuple, height: tuple,
               options: Optional[dict], profile: Optional[Union[bool, dict]]):
    super(Popup, self).__init__(page, [], css_attrs={"width": width, "height": height}, profile=profile)
    self.__options = OptPanel.OptionPopup(self, options)
    if self.options.background:
      bg_color = Colors.rgba(*Colors.getHexToRgb(page.theme.greys[-1]), 0.4)
      self.css({'width': '100%', 'position': 'fixed', 'height': '100%', 'background-color': bg_color, 'left': 0,
                'top': 0})
      self.css({'display': 'none', 'z-index': self.options.z_index, 'text-align': 'center'})
    else:
      self.css({'position': 'absolute', 'margin': 0, 'padding': 0, 'display': 'none', 'z-index': self.options.z_index})
    self.set_attrs(name="name", value="report_popup")
    self.window = self.page.ui.div(width="auto")
    self.window.options.managed = False
    self.window.set_attrs(name="tabindex", value=0)
    self.window.style.css.padding = 10
    self.window.style.css.border = "3px solid %s" % page.theme.greys[3]
    self.window.style.css.top = "200px"
    self.window.style.css.min_width = "300px"
    self.window.style.css.left = "50%"
    self.window.style.css.transform = "translate(-50%, -50%)"
    self.window.style.css.position = "fixed"
    self.window.style.css.background = page.theme.greys[0]
    self.container = page.ui.div(components, width=(100, '%'), height=(100, '%'))
    self.container.options.managed = False
    self.container.style.css.position = 'relative'
    self.container.style.css.overflow = "auto"
    self.container.style.css.padding = "auto"
    self.container.style.css.vertical_align = "middle"
    self.window.add(self.container)
    if not self.options.background and self.options.draggable:
      page.body.onReady([self.window.dom.jquery_ui.draggable()])

  @property
  def js(self) -> JsHtmlPopup.JsHtmlPopup:
    """
    Description:
    -----------
    Specific JavaScript features for the popup component.

    :return: A Javascript object

    :rtype: JsHtmlPopup.JsHtmlPopup
    """
    if self._js is None:
      self._js = JsHtmlPopup.JsHtmlPopup(page=self.page, component=self)
    return self._js

  def add(self, component: Html.Html):
    """
    Description:
    ------------
    Add a component to the popup.
    If this is a list then they will be added in a row.

    Attributes:
    ----------
    :param Html.Html component: The component to be added to the underlying list.
    """
    return self.container.add(component)

  def extend(self, components: List[Html.Html]):
    """
    Description:
    ------------
    Append list of component to the popup.

    Attributes:
    ----------
    :param List[Html.Html] components: The component to be added to the underlying list.
    """
    return self.container.extend(components)

  def insert(self, n: int, component: Html.Html):
    """
    Description:
    ------------
    Insert a component to the popup at a specific place.

    Attributes:
    ----------
    :param int n: The position in the popup.
    :param Html.Html component: The component to be added to the underlying list.
    """
    return self.container.insert(n, component)

  @property
  def options(self) -> OptPanel.OptionPopup:
    """
    Description:
    ------------
    Property to set all the possible object for a button.

    :rtype: OptPanel.OptionPopup
    """
    return self.__options

  def add_title(self, text: str, align: str = 'center', level: Optional[int] = 5, css: Optional[dict] = None,
                position: str = "before", options: Optional[dict] = None):
    """
    Description:
    ------------
    Add a title to the popup.

    Attributes:
    ----------
    :param str text: The value to be displayed to the component.
    :param str align: Optional. The text-align property within this component.
    :param Optional[int] level: Optional.
    :param Optional[dict] css: Optional. The CSS attributes to be added to the HTML component
    :param str position: Optional. The position compared to the main component tag.
    :param Optional[dict] options: Specific Python options available for this component.
    """
    if not hasattr(text, 'options'):
      title = self.page.ui.title(text, align=align, level=level, options=options)
      title.style.css.margin_top = -3
    else:
      title = text
    self.container.insert(0, title)
    return self

  def __str__(self):
    if self.options.background:
      self.style.css.padding_top = self.options.top
    if self.options.closure:
      self.close.style.css.font_factor(3)
      self.close.style.css.background_color = self.page.theme.greys[0]
      self.close.style.css.border_radius = 20
      self.close.style.css.top = 5
      self.close.style.css.z_index = self.options.z_index + 10
      self.close.style.css.right = 5
      self.close.style.css.position = 'absolute'
      self.close.click([self.dom.hide()])
      self.window.add(self.close)
    return '''<div %s>%s</div>''' % (self.get_attrs(css_class_names=self.style.get_classes()), self.window.html())
