#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Union, Optional, List
from epyk.core.py import primitives

from epyk.core.html.options import OptText

from epyk.core.html import Html
from epyk.core.js.html import JsHtml


class HtmlGeneric(Html.Html):
  name = 'tag'
  _option_cls = OptText.OptionsText

  def __init__(self, page: primitives.PageModel, tag: Union[str], text: Union[str, primitives.HtmlModel], width: tuple,
               height: tuple, html_code: Optional[str], tooltip: str, options: Optional[dict],
               profile: Optional[Union[bool, dict]]):
    self.tag = tag
    super(HtmlGeneric, self).__init__(page, [], html_code=html_code, css_attrs={"width": width, "height": height},
                                      options=options, profile=profile)
    self.add(text)
    if tooltip:
      self.tooltip(tooltip)
    if options is not None and not options.get('managed', True):
      self.options.managed = False

  @property
  def options(self) -> OptText.OptionsText:
    """
    Description:
    ------------
    Property to set all the possible object for a button.

    :rtype: OptText.OptionsText
    """
    return super().options

  def __getitem__(self, i: int) -> Html.Html:
    if not isinstance(self.val, list):
      return self.val

    return self.val[i]

  def __add__(self, components: Union[List[Html.Html], Html.Html]):
    """ Add items to a container """
    # Has to be defined here otherwise it is set to late
    if not isinstance(components, list):
      components = [components]
    for component in components:
      if component is None:
        continue

      if hasattr(component, "options"):
        component.options.managed = False
      self.val.append(component)
    return self

  @property
  def dom(self) -> JsHtml.JsHtmlRich:
    """
    Description:
    ------------
    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtml.JsHtmlRich
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtmlRich(self, page=self.page)
    return self._dom

  _js__builder__ = 'htmlObj.innerHTML = data'

  def __str__(self):
    if self.tag is None:
      if isinstance(self.val, list):
        str_val = "".join([v.html() if hasattr(v, 'html') else str(v) for v in self.val])
        return '%s%s' % (str_val, self.helper)

      return '%s%s' % (self.val, self.helper)

    if isinstance(self.val, list):
      str_val = "".join([v.html() if hasattr(v, 'html') else str(v) for v in self.val])
      return '<%s %s>%s</%s>%s' % (self.tag, self.get_attrs(css_class_names=self.style.get_classes()), str_val,
                                   self.tag, self.helper)

    return '<%s %s>%s</%s>%s' % (self.tag, self.get_attrs(css_class_names=self.style.get_classes()), self.val,
                                 self.tag, self.helper)


class HtmlGenericLInk(HtmlGeneric):
  name = 'tag'

  def preview(self, url: str, profile: Optional[Union[bool, dict]] = None):
    """
    Description:
    ------------


    Attributes:
    ----------
    :param str url: The url path.
    :param Optional[Union[bool, dict]] profile: Optional. A flag to set the component performance storage.
    """
    self.on('mouseenter', [
      self.page.js.request_http("test", 'GET', url).send().onSuccess([
        self.page.js.createElement("div", "popup").innerHTML(
          self.page.js.object("data")).attr('id', 'popup').css(
          {'color': 'red', 'display': 'block', 'background': 'white', 'width': '250px', 'padding': '10px'}).position(),
        self.page.body.dom.appendChild(self.page.js.object("popup"))]
      )
    ], profile=profile)

    self.on('mouseleave', [self.page.js.getElementById("popup").remove()], profile=profile)


class HtmlComment(Html.Html):
  name = 'comment'

  def __str__(self):
    return '<!--%s-->' % self.val
