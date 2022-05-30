#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core import html
from epyk.interfaces import Arguments
from epyk.core.css import Colors
from epyk.core.js import Imports
from epyk.core.css import Defaults as Defaults_css


class Rich:

  def __init__(self, ui):
    self.page = ui.page

  def delta(self, record=None, components=None, title=None, align="center", width=('auto', ''), height=('auto', ''),
            options=None, helper=None, profile=None):
    """
    Description:
    ------------

    Usage::

      page.ui.rich.delta({'number': 100, 'prevNumber': 60, 'thresold1': 100, 'thresold2': 50}, helper="test")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTextComp.Delta`

    :tags: Numbers |
    :categories: Container |

    Attributes:
    ----------
    :param record: Dictionary. Optional. The input data for this component.
    :param components: List. Optional. The HTML components to be added to this component.
    :param title: String | Component. Optional. A panel title. This will be attached to the title property.
    :param align: String. The text-align property within this component.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param helper: String. Optional. A tooltip helper.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="px")
    height = Arguments.size(height, unit="px")
    dfl_options = {"digits": 0, 'thousand_sep': ",", 'decimal_sep': ".",
                    'red': self.page.theme.danger.base, 'green': self.page.theme.success.base,
                    'orange': self.page.theme.warning.base}
    if options is not None:
      dfl_options.update(options)
    container = self.page.ui.div(align=align, height=height, width=width, profile=profile, options=options)

    if title is not None:
      if not hasattr(title, 'options'):
        title = self.page.ui.titles.title(title)
        title.style.css.display = "block"
        title.style.css.text_align = align
      container.add(title)
    main_component = html.HtmlTextComp.Delta(
      self.page, record or {}, components, width, ("auto", ''), dfl_options, helper, profile)
    container.add(main_component)
    container.build = main_component.build
    if title is not None:
      container.title = title
    html.Html.set_component_skin(container)
    return container

  def stars(self, val=None, label=None, color=None, align='left', best=5, html_code=None, helper=None, options=None,
            profile=None):
    """
    Description:
    ------------
    Entry point for the Stars component.

    :tags:
    :categories:

    Usage::

      page.ui.rich.stars(3, label="test", helper="This is a helper")
      stars = page.ui.rich.stars(3, label="test", helper="This is a helper")
      stars.click()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlOthers.Stars`

    Related Pages:

      https://www.w3schools.com/howto/howto_css_star_rating.asp

    Attributes:
    ----------
    :param val: Integer. Optional. Number of stars.
    :param label: String. Optional. The text of label to be added to the component.
    :param color: String. Optional. The font color in the component. Default inherit.
    :param align: String. Optional. A string with the horizontal position of the component.
    :param best: Integer. Optional. The max number of stars. Default 5.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param helper: String. Optional. The value to be displayed to the helper icon.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    html_star = html.HtmlOthers.Stars(self.page, val, label, color, align, best, html_code, helper, options, profile)
    html.Html.set_component_skin(html_star)
    return html_star

  def light(self, color=None, height=(None, 'px'), label=None, align="left", tooltip=None, helper=None, options=None,
            profile=None):
    """
    Description:
    ------------
    Add a traffic light component to give a visual status of a given process.

    :tags:
    :categories:

    Usage::

      page.ui.rich.light("red", label="label", tooltip="Tooltip", helper="Helper")
      page.ui.rich.light(True)

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTextComp.TrafficLight`

    Attributes:
    ----------
    :param color: String. Optional. A hexadecimal color code.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param label: String. Optional. The text of label to be added to the component.
    :param align: String. Optional. A string with the horizontal position of the component.
    :param tooltip: String. Optional. A string with the value of the tooltip.
    :param helper: String. Optional. The filtering properties for this component.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary.Optional. A flag to set the component performance storage.
    """
    height = Arguments.size(height, unit="px")
    if height is None or height[0] is None:
      height = (self.page.body.style.globals.font.size, "px")
    if isinstance(color, bool):
      color = self.page.theme.success.base if color else self.page.theme.danger.base
    html_traffic = html.HtmlTextComp.TrafficLight(self.page, color, label, height, tooltip, helper, options, profile)
    if align == "center":
      html_traffic.style.css.margin = "auto"
      html_traffic.style.css.display = "block"
    html.Html.set_component_skin(html_traffic)
    return html_traffic

  def info(self, text=None, options=None, profile=None):
    """
    Description:
    ------------
    Display an info icon with a tooltip.

    :tags:
    :categories:

    Usage::

      page.ui.info("Test")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlOthers.Help`

    Related Pages:

      https://fontawesome.com/icons/question-circle?style=solid
      https://api.jqueryui.com/tooltip/

    Attributes:
    ----------
    :param text: String. Optional. The content of the tooltip.
    :param profile: Boolean | Dictionary. Optional, A boolean to store the performances for each components.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    """
    html_help = html.HtmlOthers.Help(self.page, text, width=(10, "px"), profile=profile, options=options or {})
    html.Html.set_component_skin(html_help)
    return html_help

  def countdown(self, day, month, year, hour=0, minute=0, second=0, label=None, icon="fas fa-stopwatch",
                time_ms_factor=1000, width=(None, '%'), height=(None, 'px'), html_code=None, helper=None,
                options=None, profile=None):
    """
    Description:
    ------------
    Add a countdown to the page and remove the content if the page has expired.

    :tags:
    :categories:

    Usage::

      page.ui.rich.countdown(24, 9 2021)

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlDates.CountDownDate`

    Related Pages:

      https://www.w3schools.com/js/js_date_methods.asp
      https://www.w3schools.com/howto/howto_js_countdown.asp
      https://fontawesome.com/icons/stopwatch?style=solid

    Attributes:
    ----------
    :param day: Integer. . Day's number.
    :param month: Integer. . Month's number.
    :param year: Integer. Year's number.
    :param hour: Integer. Optional. Number of hours.
    :param minute: Integer. Optional. Number of minutes.
    :param second: Integer. Optional. Number of seconds.
    :param label: String. Optional. The component label content.
    :param icon: String. Optional. The component icon content from font-awesome references.
    :param time_ms_factor: Integer. Optional. The format from the format in milliseconds.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. The component identifier code (for both Python and Javascript).
    :param helper: String. Optional. A tooltip helper.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    html_cd = html.HtmlDates.CountDownDate(
      self.page, day, month, year, hour, minute, second, label, icon, time_ms_factor, width, height, html_code,
      helper, options or {}, profile)
    html.Html.set_component_skin(html_cd)
    return html_cd

  def update(self, label=None, color=None, align: str = None, width=("auto", ""), height=(None, "px"), html_code=None,
             options=None, profile=None):
    """
    Description:
    ------------
    Last Update time component.

    :tags:
    :categories:

    Usage::

      page.ui.rich.update("Last update: ")

      update = page.ui.rich.update()
      page.ui.button("Click").click([update.refresh()])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlDates.LastUpdated`

    Related Pages:

        https://github.com/epykure/epyk-templates/blob/master/locals/components/calendar.py

    Attributes:
    ----------
    :param label: String. Optional. The label to be displayed close to the date. Default Last Update.
    :param color: String. Optional. The color code for the font.
    :param align: String. Optional.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. The component identifier code (for both Python and Javascript).
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    component = html.HtmlDates.LastUpdated(self.page, label, color, width, height, html_code, options, profile)
    component.style.css.font_factor(-5)
    if align in ("center", "right"):
      component.style.css.margin = "auto"
      component.style.css.display = "block"
      component.style.css.text_align = align
    elif align == "left":
      component.style.css.display = "block"
    else:
      component.style.css.inline()
    html.Html.set_component_skin(component)
    return component

  def console(self, content="", width=(100, "%"), height=(200, "px"), html_code=None, options=None, profile=None):
    """
    Description:
    ------------
    Display an component to show logs.

    :tags:
    :categories:

    Usage::

      c = page.ui.rich.console(
        "* This is a log section for all the events in the different buttons *", options={"timestamp": True})

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTextEditor.Console`

    Templates:

        https://github.com/epykure/epyk-templates/blob/master/locals/components/checkbox.py

    Attributes:
    ----------
    :param content: String. Optional. The console content.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dflt_options = {"markdown": False, "timestamp": True}
    if options is not None:
      dflt_options.update(options)
    html_div = html.HtmlTextEditor.Console(self.page, content, width, height, html_code, None, dflt_options, profile)
    html_div.css({"border": "1px solid %s" % self.page.theme.greys[4], "background": self.page.theme.greys[2],
                  'padding': '5px'})
    html.Html.set_component_skin(html_div)
    return html_div

  def search_input(self, text='', placeholder='Search..', color=None, width=(100, '%'), height=(None, "px"),
                   html_code=None, tooltip=None, extensible=False, options=None, profile=None):
    """
    Description:
    ------------
    Search bar.

    :tags:
    :categories:

    Usage::

      page.ui.inputs.search()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlInput.Search`

    Related Pages:

      https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_anim_search

    Attributes:
    ----------
    :param text: String. Optional. The value to be displayed to the component.
    :param placeholder: String. Optional. The text display when empty.
    :param color: String. Optional. The font color in the component. Default inherit.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param tooltip: String. Optional. A string with the value of the tooltip.
    :param extensible: Boolean. Optional. Flag to specify the input style.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="px")
    height = Arguments.size(height, unit="px")
    icon_details = Defaults_css.get_icon("search")
    dflt_options = {"icon": icon_details["icon"], "icon_family": icon_details["icon_family"], 'position': 'left', 'select': True, "border": 1}
    if options is not None:
      dflt_options.update(options)
    html_s = html.HtmlInput.Search(
      self.page, text, placeholder, color, width, height, html_code, tooltip, extensible, dflt_options, profile)
    html.Html.set_component_skin(html_s)
    return html_s

  def search_results(self, records=None, results_per_page=20, width=(100, "%"), height=(None, "px"), options=None,
                     profile=None):
    """
    Description:
    ------------
    Display the search results. This will return the matches and the details.

    :tags:
    :categories:

    Usage::

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTextComp.SearchResult`

    Attributes:
    ----------
    :param records: List. Optional. The list of dictionaries with the input data.
    :param results_per_page: Integer. Optional. The page index.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    records = records or []
    dfl_options = {"pageNumber": results_per_page}
    if options is not None:
      dfl_options.update(options)
    html_help = html.HtmlTextComp.SearchResult(
      self.page, records, width=width, height=height, profile=profile,
      options=dfl_options)
    html.Html.set_component_skin(html_help)
    return html_help

  def composite(self, schema, width=(None, "%"), height=(None, "px"), html_code=None, helper=None, options=None,
                profile=None):
    """
    Description:
    ------------
    Composite bespoke object.

    This object will be built based on its schema. No specific CSS Style and class will be added to this object.
    The full definition will be done in the nested dictionary schema.

    :tags:
    :categories:

    Usage::

      schema = {'type': 'div', 'css': {}, 'class': , 'attrs': {} 'arias': {},  'children': [
          {'type': : {...}}
          ...
      ]}

    Attributes:
    ----------
    :param schema: Dictionary. The component nested structure.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param helper: String. Optional. The value to be displayed to the helper icon.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean or Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    html_help = html.HtmlTextComp.Composite(
      self.page, schema, width=width, height=height, html_code=html_code, profile=profile, options=options or {},
      helper=helper)
    html.Html.set_component_skin(html_help)
    return html_help

  def status(self, status, width=(None, "%"), height=(None, "px"), html_code=None, options=None, profile=None):
    """
    Description:
    ------------

    :tags:
    :categories:

    Usage::

    Attributes:
    ----------
    :param status:
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {'states': {
      "Done": 'green', "Success": 'green',
      'In Progress': 'orange', 'Blocked': 'brown', 'Failed': 'red'}}
    if options is not None:
      dfl_options.update(options)
    html_help = html.HtmlTextComp.Status(
      self.page, status, width=width, height=height, html_code=html_code, profile=profile, options=dfl_options)
    html.Html.set_component_skin(html_help)
    html_help.style.css.inline()
    return html_help

  def markdown(self, text="", width=("calc(100% - 10px)", ''), height=("auto", ''), html_code=None, options=None,
               profile=None):
    """
    Description:
    ------------

    :tags:
    :categories:

    Usage::

      page.ui.inputs.editor()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTextEditor.Editor`

    Templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/markdown.py

    Attributes:
    ----------
    :param text: String. Optional. The value to be displayed to the component.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dflt_options = {"markdown": True}
    if options is not None:
      dflt_options.update(options)
    md = html.HtmlTextEditor.MarkdownReader(self.page, text, width, height, html_code, dflt_options, profile)
    md.style.css.margin_left = 5
    md.style.css.margin_right = 5
    md.style.css.padding = 5
    html.Html.set_component_skin(md)
    return md

  def adv_text(self, section, title, content, background="", options=None, profile=None):
    """
    Description:
    ------------

    :tags:
    :categories:

    Usage::

    Attributes:
    ----------
    :param section:
    :param title: String | Component. Optional. A panel title. This will be attached to the title property.
    :param content:
    :param background:
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    container = self.page.ui.div(options=options, profile=profile)
    if section is not None:
      text = self.page.ui.text(section, width=(100, '%'), options=options, profile=profile)
      text.style.css.text_align = "center"
      text.style.css.font_size = self.page.body.style.globals.font.normal(-1)
      text.style.css.line_height = self.page.body.style.globals.font.normal(5)
      text.style.css.font_weight = 500
      text.style.css.letter_spacing = "0.15em"
      text.style.css.text_transform = "uppercase"
      container.add(text)

    if title is not None:
      title = self.page.ui.text(title, width=(100, '%'), options=options, profile=profile)
      title.style.css.text_align = "center"
      title.style.css.font_size = self.page.body.style.globals.font.normal(12)
      title.style.css.font_weight = 300
      title.css({'margin-block-end': '0.67em', 'margin-block-start': '0'})
      container.add(title)

    if content is not None:
      content = self.page.ui.text(content, width=(80, "%"), options=options, profile=profile)
      content.style.css.text_align = "center"
      content.style.css.font_size = self.page.body.style.globals.font.normal(2)
      content.style.css.margin = "auto"

    container.add(content)
    # container0.style.css.border = "10px solid white"
    container.style.css.text_align = "center"
    container.style.css.background = background
    container.style.css.padding = 10
    html.Html.set_component_skin(container)
    return container

  def color(self, code, content="data copied to clipboard", width=(20, 'px'), height=(20, 'px'), options=None,
            profile=None):
    """
    Description:
    ------------
    Color component.

    :tags:
    :categories:

    Usage::

    Attributes:
    ----------
    :param code: Tuple or String. The color code.
    :param content:
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    dflt_options = {"type": 'rgb', 'popup_timers': 1000}
    if options is not None:
      dflt_options.update(options)
    if dflt_options.get("type") == 'hex' or str(code).startswith("#"):
      code = Colors.getHexToRgb(code)
    d = self.page.ui.div(width=width, height=height, profile=profile)
    d.style.css.display = "inline-block"
    d.style.css.border = "1px solid %s" % self.page.theme.greys[0]
    d.tooltip("rgb: %s, hex: %s" % (code, Colors.getRgbToHex(code)))
    d.style.css.cursor = "pointer"
    d.click([
      self.page.js.clipboard(Colors.getRgbToHex(code)),
      self.page.js.print(content,  dflt_options.get('popup_timers'), dflt_options.get('popup_css'))])
    d.style.css.background = "rgb(%s, %s, %s)" % (code[0], code[1], code[2])
    html.Html.set_component_skin(d)
    return d

  def elapsed(self, day=None, month=None, year=None, label=None, icon=None, width=(None, "px"), height=(None, "px"),
              html_code=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    :tags:
    :categories:

    Usage::

    Attributes:
    ----------
    :param day:
    :param month:
    :param year:
    :param label:
    :param icon:
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    :param helper: String. Optional. The value to be displayed to the helper icon.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    options = options or {}
    md = html.HtmlDates.Elapsed(
      self.page, day, month, year, label, icon, width, height, html_code, helper, options, profile)
    html.Html.set_component_skin(md)
    return md

  def powered(self, by=None, width=(100, "%"), height=(None, "px"), options=None, profile=None):
    """
    Description:
    ------------
    Display badges for the specifies JavaScript modules.

    Tip: If by is None. This will display only the main JavaScript module with the current version.
    It will not display the underlying components.

    This component needs to be called at the end to ensure all the imported will be registered.

    :tags:
    :categories:

    Attributes:
    ----------
    :param by: List. Optional. Name of JavaScript library aliases.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit.
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    container = self.page.ui.div(width=width, options=options, profile=profile)
    container.style.css.font_factor(-4)
    if by is None:
      by = sorted(list(self.page.jsImports))
    elif by is True:
      by = []
      for alias, pkg in Imports.JS_IMPORTS.items():
        if "node_folder" not in pkg:
          by.append(alias)
    for i, b in enumerate(by):
      if b in self.page.imports.jsImports:
        if not self.page.imports.jsImports[b]["versions"]:
          continue

        badge = self.page.ui.div([
          self.page.ui.text(b.capitalize(), height=height, profile=profile),
          self.page.ui.text("v%s" % self.page.imports.jsImports[b]["versions"][0], height=height, profile=profile)],
          width="auto", profile=profile)
        badge[0].style.css.margin_right = 5
        badge[0].goto(self.page.imports.website(b), target="_blank")
        badge[0].style.css.background = Colors.randColor(self.page.py.hash(b))
        badge[0].style.css.color = "white"
        badge[0].style.css.text_shadow = "1px 1px black"
        badge[0].style.css.padding = "0 5px"
        badge[0].style.css.border_right = "1px solid black"
        badge[1].style.css.padding = "0 5px 0 0"
        badge.style.css.border = "1px solid %s" % self.page.theme.greys[5]
        badge.style.css.margin = 2
        badge.style.css.border_radius = "0 10px 10px 0"
        container.add(badge)
    html.Html.set_component_skin(container)
    return container
