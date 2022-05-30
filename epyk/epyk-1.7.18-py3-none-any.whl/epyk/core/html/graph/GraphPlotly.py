#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.html import Html
from epyk.core.css import Colors
from epyk.core.html.options import OptPlotly

from epyk.core.js import JsUtils
from epyk.core.js.primitives import JsObject

from epyk.core.data.DataClass import DataClass

from epyk.core.js.packages import JsPlotly
from epyk.core.js.packages import JsD3


class Chart(Html.Html):
  name = 'Plotly'
  requirements = ('plotly.js', )
  _option_cls = OptPlotly.OptionConfig

  def __init__(self,  page, width, height, options, html_code, profile):
    self.seriesProperties, self.__chartJsEvents, self.height = {'static': {}, 'dynamic': {}}, {}, height[0]
    super(Chart, self).__init__(page, [], html_code=html_code, profile=profile, options=options,
                                css_attrs={"width": width, "height": height})
    self._d3, self._attrs, self._traces, self._layout, self._options = None, None, [], None, None
    self.layout.autosize, self._labels = True, None
    if not height[0] is None:
      self.layout.height = height[0]

  @property
  def shared(self) -> OptPlotly.OptionsChartSharedPlotly:
    """
    Description:
    -----------
    All the common properties shared between all the charts.
    This will ensure a compatibility with the plot method.

    Usage::

      line = page.ui.charts.bb.bar()
      line.shared.x_label("x axis")
    """
    return OptPlotly.OptionsChartSharedPlotly(self)

  @property
  def chartId(self):
    """
    Description:
    ------------
    Return the Javascript variable of the chart.
    """
    return "%s_obj" % self.htmlCode

  def click_legend(self, js_funcs, profile=False):
    """
    Description:
    ------------

    Related Pages:

      https://plotly.com/javascript/plotlyjs-events/

    Attributes:
    ----------
    :param js_funcs: List | String. Javascript functions.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    self.onReady("%s.on('plotly_legendclick', function(data) {%s})" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))
    return self

  def click(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------
    The onclick event occurs when the user clicks on an element.

    Related Pages:

      https://plotly.com/javascript/click-events/

    Attributes:
    ----------
    :param js_funcs: List | String. A Javascript Python function.
    :param profile: Boolean. Optional. Set to true to get the profile for the function on the Javascript console.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.on('plotly_click', function(data) {%s})" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))
    return self

  def dblclick(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------
    The onDblclick event occurs when the user double clicks on an element.

    Related Pages:

      https://plotly.com/javascript/click-events/

    Attributes:
    ----------
    :param js_funcs: List | String. A Javascript Python function.
    :param profile: Boolean. Optional. Set to true to get the profile for the function on the Javascript console.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.on('plotly_doubleclick', function(data) {%s})" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))
    return self

  def hover(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------

    Related Pages:

      https://plotly.com/javascript/hover-events/

    Attributes:
    ----------
    :param js_funcs: List | String. A Javascript Python function.
    :param profile: Boolean. Optional. Set to true to get the profile for the function on the Javascript console.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.on('plotly_hover', function(data) {%s})" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))
    return self

  def unhover(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------

    Related Pages:

      https://plotly.com/javascript/hover-events/

    Attributes:
    ----------
    :param js_funcs: List | String. A Javascript Python function.
    :param profile: Boolean. Optional. Set to true to get the profile for the function on the Javascript console.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.on('plotly_unhover', function(data) {%s})" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))
    return self

  @property
  def data(self):
    """
    Description:
    ------------

    :rtype: DataChart
    """
    if not self._traces:
      self.add_trace([])
    return self._traces[-1]

  @property
  def options(self) -> OptPlotly.OptionConfig:
    """
    Description:
    ------------
    Property to the component options.
    Options can either impact the Python side or the Javascript builder.

    Python can pass some options to the JavaScript layer.

    :rtype: OptPlotly.OptionConfig
    """
    return super().options

  def traces(self, i: int = None):
    """
    Description:
    ------------

    :rtype: JsChartJs.DataSetPie
    """
    if i is None:
      return self._traces[-1]

    return self._traces[i]

  def labels(self, values):
    self._labels = values

  def add_dataset(self, data, label, colors=None, opacity=None, kind=None):
    series = {"x": [], "y": []}
    for i, x in enumerate(self._labels):
      series["x"].append(x)
      series["y"].append(data[i])
    trace = self.add_trace(series, type=kind)
    current_trace = trace.traces()
    current_trace.name = label
    return current_trace

  _js__builder__ = '''
      if(data.python){
        result = [];
        data.datasets.forEach(function(values, i){
          dataSet = {x: [], y: [], name: data.series[i], type: options.type, mode: options.mode, marker: {}};
          if(typeof options.attrs !== undefined){ for(var attr in options.attrs){dataSet[attr] = options.attrs[attr]} };
          if(typeof options.marker !== undefined){
            for(var attr in options.marker){dataSet.marker[attr] = options.marker[attr]} };
          result.push(Object.assign(dataSet, values))
        }); 
      } else {
        var temp = {}; var labels = []; var uniqLabels = {}; var result = [] ;
        options.y_columns.forEach(function(series){temp[series] = {}});
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(rec[name] !== undefined){
              if(!(rec[options.x_column] in uniqLabels)){
                labels.push(rec[options.x_column]); uniqLabels[rec[options.x_column]] = true};
              temp[name][rec[options.x_column]] = rec[name]}})});
        options.y_columns.forEach(function(series){
          dataSet = {x: [], y: [], name: series, type: options.type, mode: options.mode, marker: {}};
          if(typeof options.attrs !== undefined){ 
            for(var attr in options.attrs){dataSet[attr] = options.attrs[attr]} };
          if(typeof options.marker !== undefined){
            for(var attr in options.marker){dataSet.marker[attr] = options.marker[attr]} };
          labels.forEach(function(x, i){
            dataSet.x.push(x);
            if(temp[series][x] == undefined){dataSet.y.push(null)} else{dataSet.y.push(temp[series][x])}
          }); result.push(dataSet)})
      }; return result'''

  def colors(self, hex_values):
    """
    Description:
    -----------
    Set the colors of the chart.

    hex_values can be a list of string with the colors or a list of tuple to also set the bg colors.
    If the background colors are not specified they will be deduced from the colors list changing the opacity.

    Usage::

    Attributes:
    ----------
    :param hex_values: List. An array of hexadecimal color codes.
    """
    line_colors, bg_colors = [], []
    for h in hex_values:
      if h.upper() in Colors.defined:
        h = Colors.defined[h.upper()]['hex']
      if not isinstance(h, tuple):
        line_colors.append(h)
        bg_colors.append("rgba(%s, %s, %s, %s" % (
          Colors.getHexToRgb(h)[0], Colors.getHexToRgb(h)[1],
          Colors.getHexToRgb(h)[2], self.options.opacity))
      else:
        line_colors.append(h[0])
        bg_colors.append(h[0])
    self.options.colors = line_colors
    self.options.background_colors = bg_colors
    for i, rec in enumerate(self._traces):
      rec.fillcolor = self.options.background_colors[i]
      rec.line.color = self.options.colors[i]
      rec.marker.line.color = self.options.colors[i]
      rec.marker.color = self.options.colors[i]

  @property
  def js(self) -> JsPlotly.JsPlotly:
    """
    Description:
    -----------
    Javascript base function.

    Return all the Javascript functions defined in the framework.
    This is an entry point to the full Javascript ecosystem.

    :return: A Javascript object

    :rtype: JsPlotly.JsPlotly
    """
    if self._js is None:
      self._js = JsPlotly.JsPlotly(selector="window['%s']" % self.chartId, component=self, page=self.page)
    return self._js

  @property
  def layout(self):
    """
    Description:
    -----------

    :rtype: Layout
    """
    if self._layout is None:
      self._layout = Layout(page=self.page, component=self)
    return self._layout

  @property
  def d3(self):
    """
    Description:
    -----------

    :rtype: JsD3.D3Select
    """
    if self._d3 is None:
      self._d3 = JsD3.D3Select(self.page, selector="d3.select('#%s')" % self.htmlCode, setVar=False)
    return self._d3

  def add_trace(self, data, type=None, mode=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param data:
    :param type:
    :param mode:
    """
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataChart(component=self, page=self.page, attrs=c_data))
    return self

  def build(self, data=None, options=None, profile=None, component_id=None):
    if data is not None:
      js_convertor = "%s%s" % (self.name, self.__class__.name)
      self.page.properties.js.add_constructor(
        js_convertor, "function %s(data, options){%s}" % (js_convertor, self._js__builder__))
      profile = self.with_profile(profile, event="Builder", element_id=self.chartId)
      if profile:
        js_func_builder = JsUtils.jsConvertFncs(
          ["var result = %s(data, options)" % js_convertor], toStr=True, profile=profile)
        js_convertor = "(function(data, options){%s; return result})" % js_func_builder
      return JsUtils.jsConvertFncs([
        self.js.react(JsUtils.jsWrap("%(chartFnc)s(%(data)s, %(options)s)" % {
          'chartFnc': js_convertor, "data": JsUtils.jsConvertData(data, None),
          "options":  self.options.config_js(options)}), self.layout, self.options.config_js(options))], toStr=True)

    str_traces = []
    for t in self._traces:
      str_traces.append("{%s}" % ", ".join(["%s: %s" % (k, JsUtils.jsConvertData(v, None)) for k, v in t.attrs()]))
    obj_datasets = JsObject.JsObject.get("[%s]" % ", ".join(str_traces))
    return "%s = %s" % (self.chartId, JsUtils.jsConvertFncs([
      self.js.newPlot(obj_datasets, self.layout, self.options)], toStr=True))

  def __str__(self):
    self.page.properties.js.add_builders(self.build())
    return '<div %s></div>' % self.get_attrs(css_class_names=self.style.get_classes())


class Line(Chart):

  @property
  def dom(self):
    """
    :rtype: JsPlotly.Line
    """
    if self._dom is None:
      self._dom = JsPlotly.Line(component=self, js_code=self.chartId, page=self.page)
    return self._dom

  def trace(self, data, type=None, mode='lines+markers'):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = self.options.type
    if mode is not None:
      c_data['mode'] = self.options.mode or mode
    return DataXY(page=self.page, attrs=c_data, component=self)

  def add_trace(self, data, type=None, mode='lines+markers'):
    """

    :param data:
    :param type:
    :param mode:
    """
    self._traces.append(self.trace(data, type, mode))
    self.data.line.color = self.options.colors[len(self._traces)-1]
    self.data.marker.color = self.options.colors[len(self._traces)-1]
    return self


class Bar(Chart):

  @property
  def chart(self) -> JsPlotly.Bar:
    """
    :rtype: JsPlotly.Bar
    """
    if self._chart is None:
      self._chart = JsPlotly.Bar(page=self.page, js_code=self.chartId, component=self)
    return self._chart

  @property
  def layout(self):
    if self._layout is None:
      self._layout = LayoutBar(page=self.page, component=self)
    return self._layout

  def trace(self, data, type='bar', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = self.options.type
    if mode is not None:
      c_data['mode'] = self.options.mode or mode
    return DataXY(component=self, page=self.page, attrs=c_data)

  def add_trace(self, data, type='bar', mode=None):
    self._traces.append(self.trace(data, type, mode))
    self.data.line.color = self.options.colors[len(self._traces)-1]
    self.data.marker.color = self.options.colors[len(self._traces)-1]
    return self

  def add_dataset(self, data, label, colors=None, opacity=None, kind='bar'):
    return super().add_dataset(data, label, colors, opacity, kind)


class DataFill(DataClass):

  @property
  def color(self):
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val


class LayoutAnnotation(DataClass):

  @property
  def xanchor(self):
    return self._attrs["xanchor"]

  @xanchor.setter
  def xanchor(self, val):
    self._attrs["xanchor"] = val

  @property
  def ax(self):
    return self._attrs["ax"]

  @ax.setter
  def ax(self, val):
    self._attrs["ax"] = val

  @property
  def ay(self):
    return self._attrs["ay"]

  @ay.setter
  def ay(self, val):
    self._attrs["ay"] = val

  @property
  def text(self):
    return self._attrs["text"]

  @text.setter
  def text(self, val):
    self._attrs["text"] = val

  @property
  def showarrow(self):
    return self._attrs["showarrow"]

  @showarrow.setter
  def showarrow(self, val):
    self._attrs["showarrow"] = val

  @property
  def x(self):
    return self._attrs["x"]

  @x.setter
  def x(self, val):
    self._attrs["x"] = val

  @property
  def y(self):
    return self._attrs["y"]

  @y.setter
  def y(self, val):
    self._attrs["y"] = val

  @property
  def xref(self):
    return self._attrs["xref"]

  @xref.setter
  def xref(self, val):
    self._attrs["xref"] = val

  @property
  def yref(self):
    return self._attrs["yref"]

  @yref.setter
  def yref(self, val):
    self._attrs["yref"] = val

  @property
  def font(self):
    return self.sub_data("font", DataFont)


class LayoutShape(DataClass):

  def add_path(self, points, color: str = None):
    """

    https://plot.ly/javascript/shapes/

    :param points:
    :param color:
    """
    self._attrs.update({'type': 'path', 'path': points})
    self.fillcolor = color or self.page.theme.warning.light
    return self

  def add_line(self, x, y, x1, y1, opacity=0.2, color=None):
    """

    .layout.shapes.add_line(-100, 10, -50, -10, color="red")

    :param x:
    :param y:
    :param x1:
    :param y1:
    :param opacity:
    :param color:
    """
    self._attrs.update({'type': 'line', 'xref': 'x', 'yref': 'y', 'x0': x, 'y0': y, 'x1': x1, 'y1': y1})
    self.line.color = color or self.page.theme.warning.light
    self.line.dash = 'dot'
    self.opacity = opacity
    return self

  def add_circle(self, x, y, x1, y1, opacity=0.2, color=None):
    """

    :param x:
    :param y:
    :param x1:
    :param y1:
    :param opacity:
    :param color:
    """
    self._attrs.update({'type': 'circle', 'xref': 'x', 'yref': 'y', 'x0': x, 'y0': y, 'x1': x1, 'y1': y1})
    self.fillcolor = color or self.page.theme.warning.light
    self.line.width = 0
    self.opacity = opacity
    return self

  def add_rect(self, x, y, x1, y1, opacity=0.2, color=None):
    """

    :param x:
    :param y:
    :param x1:
    :param y1:
    :param opacity:
    :param color:
    """
    self._attrs.update({'type': 'rect', 'xref': 'x', 'yref': 'paper', 'x0': x, 'y0': y, 'x1': x1, 'y1': y1})
    self.fillcolor = color or self.page.theme.warning.light
    self.line.width = 0
    self.opacity = opacity
    return self

  @property
  def type(self):
    return self._attrs["type"]

  @type.setter
  def type(self, val):
    self._attrs["type"] = val

  @property
  def xref(self):
    return self._attrs["xref"]

  @xref.setter
  def xref(self, val):
    self._attrs["xref"] = val

  @property
  def yref(self):
    return self._attrs["yref"]

  @yref.setter
  def yref(self, val):
    self._attrs["yref"] = val

  @property
  def x0(self):
    return self._attrs["x0"]

  @x0.setter
  def x0(self, val):
    self._attrs["x0"] = val

  @property
  def y0(self):
    return self._attrs["y0"]

  @y0.setter
  def y0(self, val):
    self._attrs["y0"] = val

  @property
  def x1(self):
    return self._attrs["x1"]

  @x1.setter
  def x1(self, val):
    self._attrs["x1"] = val

  @property
  def y1(self):
    return self._attrs["y1"]

  @y1.setter
  def y1(self, val):
    self._attrs["y1"] = val

  @property
  def fillcolor(self):
    return self._attrs["fillcolor"]

  @fillcolor.setter
  def fillcolor(self, val):
    self._attrs["fillcolor"] = val

  @property
  def opacity(self):
    return self._attrs["opacity"]

  @opacity.setter
  def opacity(self, val):
    self._attrs["opacity"] = val

  @property
  def line(self):
    """

    :rtype: DataMarkersLine
    """
    return self.sub_data("line", DataMarkersLine)


class LayoutFont(DataClass):

  @property
  def color(self):
    """

    :prop color: color or array of colors
    """
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val

  @property
  def family(self):
    """
    HTML font family - the typeface that will be applied by the web browser.

    https://plot.ly/javascript/reference/#pie-outsidetextfont-family

    :prop font-family:  string or array of strings
    """
    return self._attrs["family"]

  @family.setter
  def family(self, val):
    self._attrs["family"] = val

  @property
  def size(self):
    """

    https://plot.ly/javascript/reference/#pie-outsidetextfont-family

    :return: number or array of numbers greater than or equal to 1
    """
    return self._attrs["size"]

  @size.setter
  def size(self, val):
    self._attrs["size"] = val


class LayoutGrid(DataClass):

  @property
  def rows(self):
    return self._attrs["rows"]

  @rows.setter
  def rows(self, val):
    self._attrs["rows"] = val

  @property
  def columns(self):
    return self._attrs["columns"]

  @columns.setter
  def columns(self, val):
    self._attrs["columns"] = val

  @property
  def pattern(self):
    return self._attrs["pattern"]

  @pattern.setter
  def pattern(self, val):
    self._attrs["pattern"] = val


class LayoutButtons(DataClass):

  @property
  def count(self):
    return self._attrs["count"]

  @count.setter
  def count(self, val):
    self._attrs["count"] = val

  @property
  def label(self):
    return self._attrs["label"]

  @label.setter
  def label(self, val):
    self._attrs["label"] = val

  @property
  def step(self):
    return self._attrs["step"]

  @step.setter
  def step(self, val):
    self._attrs["step"] = val

  @property
  def stepmode(self):
    return self._attrs["stepmode"]

  @stepmode.setter
  def stepmode(self, val):
    self._attrs["stepmode"] = val


class LayoutRangeSelector(DataClass):

  @property
  def buttons(self) -> LayoutButtons:
    """

    https://plot.ly/javascript/time-series/
    https://plot.ly/javascript/range-slider/

    :rtype: LayoutButtons
    """
    return self.sub_data_enum("buttons", LayoutButtons)

  def month(self, n):
    but = self.buttons
    but.step = 'month'
    but.stepmode = 'backward'
    but.count = n
    but.label = "%sm" % n
    return self

  def year(self, n=0):
    but = self.buttons
    but.step = 'year'
    but.count = n
    but.stepmode = 'todate' if n == 0 else 'backward'
    but.label = 'YTD' if n == 0 else "%sy" % n
    return self

  def all(self):
    but = self.buttons
    but.step = 'all'
    return self


class LayoutRangeSlider(DataClass):

  @property
  def range(self):
    return self._attrs["range"]

  @range.setter
  def range(self, val):
    self._attrs["range"] = val


class LayoutAxis(DataClass):

  @property
  def title(self):
    return self._attrs["title"]

  @title.setter
  def title(self, val):
    self._attrs["title"] = val

  @property
  def showbackground(self):
    return self._attrs["showbackground"]

  @showbackground.setter
  def showbackground(self, val):
    self._attrs["showbackground"] = val

  @property
  def backgroundcolor(self):
    return self._attrs["backgroundcolor"]

  @backgroundcolor.setter
  def backgroundcolor(self, val):
    self._attrs["backgroundcolor"] = val

  @property
  def tickangle(self):
    return self._attrs["tickangle"]

  @tickangle.setter
  def tickangle(self, val):
    self._attrs["tickangle"] = val

  @property
  def titlefont(self) -> LayoutFont:
    """

    :rtype: LayoutFont

    :return:
    """
    return self.sub_data("titlefont", LayoutFont)

  @property
  def tickfont(self) -> LayoutFont:
    """

    :rtype: LayoutFont

    :return:
    """
    return self.sub_data("tickfont", LayoutFont)

  def set_color(self, color):
    """

    :param color:
    """
    self.titlefont.color = color
    self.tickfont.color = color
    return self

  @property
  def overlaying(self):
    return self._attrs["overlaying"]

  @overlaying.setter
  def overlaying(self, val):
    self._attrs["overlaying"] = val

  @property
  def side(self):
    return self._attrs["side"]

  @side.setter
  def side(self, val):
    self._attrs["side"] = val

  @property
  def anchor(self):
    return self._attrs["anchor"]

  @anchor.setter
  def anchor(self, val):
    self._attrs["anchor"] = val

  @property
  def domain(self):
    return self._attrs["domain"]

  @domain.setter
  def domain(self, val):
    self._attrs["domain"] = val

  @property
  def dtick(self):
    return self._attrs["dtick"]

  @dtick.setter
  def dtick(self, val):
    self._attrs["dtick"] = val

  @property
  def autorange(self):
    return self._attrs["autorange"]

  @autorange.setter
  def autorange(self, val):
    self._attrs["autorange"] = val

  @property
  def position(self):
    return self._attrs["position"]

  @position.setter
  def position(self, val):
    self._attrs["position"] = val

  @property
  def paper_bgcolor(self):
    return self._attrs["paper_bgcolor"]

  @paper_bgcolor.setter
  def paper_bgcolor(self, val):
    self._attrs["paper_bgcolor"] = val

  @property
  def plot_bgcolor(self):
    return self._attrs["plot_bgcolor"]

  @plot_bgcolor.setter
  def plot_bgcolor(self, val):
    self._attrs["plot_bgcolor"] = val

  @property
  def range(self):
    return self._attrs["range"]

  @range.setter
  def range(self, val):
    self._attrs["range"] = val

  @property
  def gridcolor(self):
    return self._attrs["gridcolor"]

  @gridcolor.setter
  def gridcolor(self, val):
    self._attrs["gridcolor"] = val

  @property
  def gridwidth(self):
    return self._attrs["gridwidth"]

  @gridwidth.setter
  def gridwidth(self, val):
    self._attrs["gridwidth"] = val

  @property
  def type(self):
    return self._attrs["type"]

  @type.setter
  def type(self, val):
    self._attrs["type"] = val

  @property
  def zeroline(self):
    return self._attrs["zeroline"]

  @zeroline.setter
  def zeroline(self, val):
    self._attrs["zeroline"] = val

  @property
  def showline(self):
    return self._attrs["showline"]

  @showline.setter
  def showline(self, val):
    self._attrs["showline"] = val

  @property
  def showgrid(self):
    return self._attrs["showgrid"]

  @showgrid.setter
  def showgrid(self, val):
    self._attrs["showgrid"] = val

  @property
  def showticklabels(self):
    return self._attrs["showticklabels"]

  @showticklabels.setter
  def showticklabels(self, val):
    self._attrs["showticklabels"] = val

  @property
  def rangeselector(self) -> LayoutRangeSelector:
    """

    https://plot.ly/javascript/time-series/

    :rtype: LayoutRangeSelector
    """
    return self.sub_data("rangeselector", LayoutRangeSelector)

  @property
  def rangeslider(self) -> LayoutRangeSlider:
    """

    https://plot.ly/javascript/time-series/

    :rtype: LayoutRangeSlider
    """
    return self.sub_data("rangeslider", LayoutRangeSlider)


class LayoutMargin(DataClass):

  @property
  def l(self):
    return self._attrs["l"]

  @l.setter
  def l(self, val):
    self._attrs["l"] = val

  @property
  def r(self):
    return self._attrs["r"]

  @r.setter
  def r(self, val):
    self._attrs["r"] = val

  @property
  def b(self):
    return self._attrs["b"]

  @b.setter
  def b(self, val):
    self._attrs["b"] = val

  @property
  def t(self):
    return self._attrs["t"]

  @t.setter
  def t(self, val):
    self._attrs["t"] = val

  def clear(self, l=0, r=0, b=0, t=0):
    self.l = l
    self.r = r
    self.b = b
    self.t = t


class LayoutEye(DataClass):

  @property
  def x(self):
    return self._attrs["x"]

  @x.setter
  def x(self, val):
    self._attrs["x"] = val

  @property
  def y(self):
    return self._attrs["y"]

  @y.setter
  def y(self, val):
    self._attrs["y"] = val

  @property
  def z(self):
    return self._attrs["z"]

  @z.setter
  def z(self, val):
    self._attrs["z"] = val


class LayoutCamera(DataClass):

  @property
  def eye(self) -> LayoutEye:
    """

    :rtype: LayoutEye

    :return:
    """
    return self.sub_data("eye", LayoutEye)


class LayoutScene(DataClass):

  @property
  def camera(self) -> LayoutCamera:
    """

    :rtype: LayoutCamera

    :return:
    """
    return self.sub_data("scene", LayoutCamera)

  @property
  def xaxis(self) -> LayoutAxis:
    """

    :rtype: LayoutAxis

    :return:
    """
    return self.sub_data("xaxis", LayoutAxis)

  @property
  def yaxis(self) -> LayoutAxis:
    """

    :rtype: LayoutAxis

    :return:
    """
    return self.sub_data("yaxis", LayoutAxis)

  @property
  def zaxis(self) -> LayoutAxis:
    """

    :rtype: LayoutAxis

    :return:
    """
    return self.sub_data("zaxis", LayoutAxis)


class LayoutLegend(DataClass):

  @property
  def x(self):
    return self._attrs["x"]

  @x.setter
  def x(self, val):
    self._attrs["x"] = val

  @property
  def bgcolor(self):
    return self._attrs["bgcolor"]

  @bgcolor.setter
  def bgcolor(self, val):
    self._attrs["bgcolor"] = val

  @property
  def bordercolor(self):
    return self._attrs["bordercolor"]

  @bordercolor.setter
  def bordercolor(self, val):
    self._attrs["bordercolor"] = val

  @property
  def borderwidth(self):
    return self._attrs["borderwidth"]

  @borderwidth.setter
  def borderwidth(self, val):
    self._attrs["borderwidth"] = val

  @property
  def traceorder(self):
    return self._attrs["traceorder"]

  @traceorder.setter
  def traceorder(self, val):
    self._attrs["traceorder"] = val

  @property
  def orientation(self):
    return self._attrs["orientation"]

  @orientation.setter
  def orientation(self, val):
    self._attrs["orientation"] = val

  @property
  def y(self):
    return self._attrs["y"]

  @y.setter
  def y(self, val):
    self._attrs["y"] = val

  @property
  def xanchor(self):
    return self._attrs["xanchor"]

  @xanchor.setter
  def xanchor(self, val):
    self._attrs["xanchor"] = val

  @property
  def font(self) -> LayoutFont:
    """

    :rtype: LayoutFont
    """
    return self.sub_data("font", LayoutFont)


class LayoutTitle(DataClass):

  @property
  def text(self):
    return self._attrs["text"]

  @text.setter
  def text(self, val):
    self._attrs["text"] = val


class Layout(DataClass):


  @property
  def title(self):
    """


    :rtype: LayoutTitle
    """
    return self.sub_data("title", LayoutTitle)

  @property
  def paper_bgcolor(self):
    return self._attrs["paper_bgcolor"]

  @paper_bgcolor.setter
  def paper_bgcolor(self, val):
    self._attrs["paper_bgcolor"] = val

  @property
  def plot_bgcolor(self):
    return self._attrs["plot_bgcolor"]

  @plot_bgcolor.setter
  def plot_bgcolor(self, val):
    self._attrs["plot_bgcolor"] = val

  @property
  def showlegend(self):
    return self._attrs["showlegend"]

  @showlegend.setter
  def showlegend(self, val):
    self._attrs["showlegend"] = val

  @property
  def height(self):
    return self._attrs["height"]

  @height.setter
  def height(self, val):
    self._attrs["height"] = val

  @property
  def width(self):
    return self._attrs["width"]

  @width.setter
  def width(self, val):
    self._attrs["width"] = val

  @property
  def scene(self):
    """

    :rtype: LayoutScene
    """
    return self.sub_data("scene", LayoutScene)

  @property
  def legend(self):
    """

    https://plot.ly/javascript/legend/

    :rtype: LayoutLegend
    """
    return self.sub_data("legend", LayoutLegend)

  @property
  def xaxis(self):
    """

    https://plot.ly/javascript/time-series/

    :rtype: LayoutAxis
    """
    return self.sub_data("xaxis", LayoutAxis)

  @property
  def xaxis2(self):
    """

    https://plot.ly/javascript/time-series/

    :rtype: LayoutAxis
    """
    return self.sub_data("xaxis2", LayoutAxis)

  @property
  def grid(self):
    """

    https://plot.ly/javascript/subplots/

    :rtype: LayoutGrid
    """
    return self.sub_data("grid", LayoutGrid)

  @property
  def yaxis(self):
    """

    https://plot.ly/javascript/time-series/

    :rtype: LayoutAxis
    """
    return self.sub_data("yaxis", LayoutAxis)

  @property
  def yaxis2(self):
    """

    https://plot.ly/javascript/time-series/

    :rtype: LayoutAxis
    """
    return self.sub_data("yaxis2", LayoutAxis)

  @property
  def margin(self):
    """

    https://plot.ly/javascript/3d-surface-plots/

    :rtype: LayoutMargin
    """
    return self.sub_data("margin", LayoutMargin)

  def sub_plot(self, columns, rows=1, pattern='independent'):
    self.grid.rows = rows
    self.grid.columns = columns
    self.grid.pattern = pattern
    return self

  def inset_trace(self, x_domain, x, y=None, y_domain=None):
    """

    https://plot.ly/javascript/insets/

    :param x_domain:
    :param x:
    :param y:
    :param y_domain:
    """
    y = y or x
    y_domain = y_domain or x_domain
    x_axis = self.sub_data('xaxis%s' % x, LayoutAxis)
    x_axis.domain = x_domain
    x_axis.anchor = "y%s" % y
    y_axis = self.sub_data('yaxis%s' % y, LayoutAxis)
    y_axis.domain = y_domain
    y_axis.anchor = "x%s" % x
    return self

  def no_background(self):
    """

    https://community.plot.ly/t/you-can-remove-the-white-background-of-the-graphics-background/933

    :return:
    """
    self.paper_bgcolor = 'rgba(0,0,0,0)'
    self.plot_bgcolor = 'rgba(0,0,0,0)'
    return self

  def no_grid(self):
    """
    Remove the vertical and horizontal sub axis from the chart display.
    Keep the zeroline axis

    :return: The attribute object to allow the chaining
    """
    self.xaxis.showgrid = False
    self.xaxis.showline = False
    self.xaxis.showticklabels = False
    self.yaxis.showgrid = False
    self.yaxis.showline = False
    self.yaxis.showticklabels = False
    return self

  def grid_colors(self, x_color, y_color=None):
    """

    :param x_color:
    :param y_color:

    :return:
    """
    self.xaxis.gridcolor = x_color
    self.yaxis.gridcolor = y_color or x_color
    return self

  def axis_colors(self, x_color, y_color=None):
    """

    :param x_color:
    :param y_color:

    :return:
    """
    self.xaxis.set_color(x_color)
    self.yaxis.set_color(y_color or x_color)
    return self

  @property
  def shapes(self):
    """

    https://plot.ly/javascript/shapes/

    :rtype: LayoutShape
    """
    return self.sub_data_enum("shapes", LayoutShape)

  @property
  def annotations(self):
    """

    https://plot.ly/javascript/shapes/

    :rtype: LayoutAnnotation
    """
    return self.sub_data_enum("annotations", LayoutAnnotation)


class Layout3D(Layout):

  @property
  def scene(self):
    """

    :rtype: LayoutScene
    """
    return self.sub_data("scene", LayoutScene)

  def grid_colors(self, x_color, y_color=None, z_color=None):
    """

    :param x_color:
    :param y_color:
    :param z_color:
    """
    self.scene.xaxis.gridcolor = x_color
    self.scene.xaxis.zerolinecolor = x_color
    self.scene.yaxis.gridcolor = y_color
    self.scene.yaxis.zerolinecolor = y_color
    self.scene.zaxis.gridcolor = z_color
    self.scene.zaxis.zerolinecolor = z_color
    return self

  def axis_colors(self, x_color, y_color=None, z_color=None):
    """

    :param x_color:
    :param y_color:
    :param z_color:

    :return:
    """
    self.scene.xaxis.set_color(x_color)
    self.scene.yaxis.set_color(y_color or x_color)
    self.scene.zaxis.set_color(z_color or x_color)
    return self


class LayoutBar(Layout):

  @property
  def barmode(self):
    return self._attrs["barmode"]

  @barmode.setter
  def barmode(self, val):
    self._attrs["barmode"] = val


class LayoutBox(Layout):
  @property
  def boxmode(self):
    return self._attrs["boxmode"]

  @boxmode.setter
  def boxmode(self, val):
    self._attrs["boxmode"] = val


class DataFont(DataClass):

  @property
  def family(self):
    return self._attrs["family"]

  @family.setter
  def family(self, val):
    self._attrs["family"] = val

  @property
  def size(self):
    return self._attrs["size"]

  @size.setter
  def size(self, val):
    self._attrs["size"] = val

  @property
  def color(self):
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val


class DataMarkersLine(DataClass):

  @property
  def width(self):
    return self._attrs["width"]

  @width.setter
  def width(self, val):
    self._attrs["width"] = val

  @property
  def color(self):
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val

  @property
  def dash(self):
    return self._attrs["dash"]

  @dash.setter
  def dash(self, val):
    self._attrs["dash"] = val

  @property
  def outliercolor(self):
    return self._attrs["outliercolor"]

  @outliercolor.setter
  def outliercolor(self, val):
    self._attrs["outliercolor"] = val

  @property
  def outlierwidth(self):
    return self._attrs["outlierwidth"]

  @outlierwidth.setter
  def outlierwidth(self, val):
    self._attrs["outlierwidth"] = val


class DataMarkers(DataClass):

  @property
  def size(self):
    return self._attrs["size"]

  @size.setter
  def size(self, val):
    self._attrs["size"] = val

  @property
  def symbol(self):
    return self._attrs["symbol"]

  @symbol.setter
  def symbol(self, val):
    self._attrs["symbol"] = val

  @property
  def sizemode(self):
    return self._attrs["sizemode"]

  @sizemode.setter
  def sizemode(self, val):
    self._attrs["sizemode"] = val

  @property
  def color(self):
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val

  @property
  def colors(self):
    return self._attrs["colors"]

  @colors.setter
  def colors(self, val):
    self._attrs["colors"] = val

  @property
  def opacity(self):
    return self._attrs["opacity"]

  @opacity.setter
  def opacity(self, val):
    self._attrs["opacity"] = val

  @property
  def width(self):
    return self._attrs["width"]

  @width.setter
  def width(self, val):
    self._attrs["width"] = val

  @property
  def outliercolor(self):
    """

    https://plot.ly/javascript/box-plots/
    """
    return self._attrs["outliercolor"]

  @outliercolor.setter
  def outliercolor(self, val):
    self._attrs["outliercolor"] = val

  @property
  def line(self):
    """

    https://plot.ly/javascript/webgl-vs-svg/

    :rtype: DataMarkersLine
    """
    return self.sub_data("line", DataMarkersLine)


class DataChart(DataClass):

  @property
  def automargin(self):
    return self._attrs["automargin"]

  @automargin.setter
  def automargin(self, val):
    self._attrs["automargin"] = val

  @property
  def hole(self):
    return self._attrs["hole"]

  @hole.setter
  def hole(self, val):
    self._attrs["hole"] = val

  @property
  def opacity(self):
    return self._attrs["opacity"]

  @opacity.setter
  def opacity(self, val):
    self._attrs["opacity"] = val

  @property
  def name(self):
    return self._attrs["name"]

  @name.setter
  def name(self, val):
    self._attrs["name"] = val

  @property
  def mode(self):
    return self._attrs["mode"]

  @mode.setter
  def mode(self, val):
    self._attrs["mode"] = val

  @property
  def fill(self):
    return self._attrs["fill"]

  @fill.setter
  def fill(self, val):
    self._attrs["fill"] = val

  @property
  def fillcolor(self):
    return self._attrs["fillcolor"]

  @fillcolor.setter
  def fillcolor(self, val):
    self._attrs["fillcolor"] = val

  @property
  def orientation(self):
    return self._attrs["orientation"]

  @orientation.setter
  def orientation(self, val):
    self._attrs["orientation"] = val

  @property
  def type(self):
    return self._attrs["type"]

  @type.setter
  def type(self, val):
    self._attrs["type"] = val

  @property
  def showlegend(self):
    return self._attrs["showlegend"]

  @showlegend.setter
  def showlegend(self, val):
    self._attrs["showlegend"] = val

  @property
  def legendgroup(self):
    return self._attrs["legendgroup"]

  @legendgroup.setter
  def legendgroup(self, val):
    self._attrs["legendgroup"] = val

  @property
  def mode(self):
    return self._attrs["mode"]

  @mode.setter
  def mode(self, val):
    self._attrs["mode"] = val

  @property
  def xaxis(self):
    return self._attrs["xaxis"]

  @xaxis.setter
  def xaxis(self, val):
    self._attrs["xaxis"] = val

  @property
  def yaxis(self):
    return self._attrs["yaxis"]

  @yaxis.setter
  def yaxis(self, val):
    self._attrs["yaxis"] = val

  def axis_index(self, x, y=None):
    """

    :param x:
    :param y:
    """
    self.xaxis = "x%s" % x
    self.yaxis = "y%s" % (y or x)
    return self

  @property
  def marker(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/bubble-charts/

    :rtype: DataMarkers
    """
    return self.sub_data("marker", DataMarkers)


class DataXY(DataChart):

  @property
  def x(self):
    return self._attrs["x"]

  @x.setter
  def x(self, val):
    self._attrs["x"] = val

  @property
  def y(self):
    return self._attrs["y"]

  @y.setter
  def y(self, val):
    self._attrs["y"] = val

  @property
  def text(self):
    return self._attrs["text"]

  @text.setter
  def text(self, val):
    self._attrs["text"] = val

  @property
  def line(self):
    return self.sub_data("line", DataLine)


class DataPie(DataChart):

  @property
  def hole(self):
    return self._attrs["hole"]

  @hole.setter
  def hole(self, val):
    self._attrs["hole"] = val

  @property
  def values(self):
    return self._attrs["values"]

  @values.setter
  def values(self, val):
    self._attrs["values"] = val

  @property
  def labels(self):
    return self._attrs["labels"]

  @labels.setter
  def labels(self, val):
    self._attrs["labels"] = val

  @property
  def textinfo(self):
    return self._attrs["textinfo"]

  @textinfo.setter
  def textinfo(self, val):
    self._attrs["textinfo"] = val

  @property
  def outsidetextfont(self):
    """
    Sets the font used for `textinfo` lying outside the sector.

    https://plot.ly/javascript/reference/#pie-outsidetextfont-family

    :rtype: DataFont
    """
    return self.sub_data("outsidetextfont", DataFont)

  @property
  def hoverinfo(self):
    return self._attrs["hoverinfo"]

  @hoverinfo.setter
  def hoverinfo(self, val):
    self._attrs["hoverinfo"] = val

  @property
  def text(self):
    return self._attrs["text"]

  @text.setter
  def text(self, val):
    self._attrs["text"] = val

  @property
  def textposition(self):
    return self._attrs["textposition"]

  @textposition.setter
  def textposition(self, val):
    self._attrs["textposition"] = val


class DataProject(DataChart):

  @property
  def z(self):
    return self._attrs["z"]

  @z.setter
  def z(self, val):
    self._attrs["z"] = val


class DataZ(DataChart):

  @property
  def show(self):
    return self._attrs["show"]

  @show.setter
  def show(self, val):
    self._attrs["show"] = val

  @property
  def usecolormap(self):
    return self._attrs["usecolormap"]

  @usecolormap.setter
  def usecolormap(self, val):
    self._attrs["usecolormap"] = val

  @property
  def highlightcolor(self):
    return self._attrs["highlightcolor"]

  @highlightcolor.setter
  def highlightcolor(self, val):
    self._attrs["highlightcolor"] = val

  @property
  def project(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/3d-surface-plots/

    :rtype: DataProject
    """
    return self.sub_data("project", DataProject)


class DataContours(DataChart):

  @property
  def z(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/3d-surface-plots/

    :rtype: DataZ
    """
    return self.sub_data("z", DataZ)


class DataLine(DataChart):

  @property
  def color(self):
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val

  @property
  def width(self):
    return self._attrs["width"]

  @width.setter
  def width(self, val):
    self._attrs["width"] = val


class DataMove(DataChart):

  @property
  def line(self):
    """
    Description:
    ------------

    :rtype: DataLine

    :return:
    """
    return self.sub_data("line", DataLine)


class DataSurface(DataChart):

  @property
  def showscale(self):
    return self._attrs["showscale"]

  @showscale.setter
  def showscale(self, val):
    self._attrs["showscale"] = val

  @property
  def contours(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/3d-surface-plots/

    :rtype: DataContours
    """
    return self.sub_data("contours", DataContours)

  @property
  def line(self):
    """
    Description:
    ------------

    :rtype: DataLine

    :return:
    """
    return self.sub_data("line", DataLine)


class DataDelta(DataClass):

  @property
  def reference(self):
    return self._attrs["reference"]

  @reference.setter
  def reference(self, val):
    self._attrs["reference"] = val

  @property
  def relative(self):
    return self._attrs["relative"]

  @relative.setter
  def relative(self, val):
    self._attrs["relative"] = val

  @property
  def position(self):
    return self._attrs["position"]

  @position.setter
  def position(self, val):
    self._attrs["position"] = val

  @property
  def valueformat(self):
    return self._attrs["valueformat"]

  @valueformat.setter
  def valueformat(self, val):
    self._attrs["valueformat"] = val


class DataTitle(DataChart):

  @property
  def text(self):
    return self._attrs["text"]

  @text.setter
  def text(self, val):
    self._attrs["text"] = val


class DataNumber(DataChart):

  @property
  def prefix(self):
    return self._attrs["prefix"]

  @prefix.setter
  def prefix(self, val):
    self._attrs["prefix"] = val


class DataGauge(DataChart):

  @property
  def shape(self):
    return self._attrs["shape"]

  @shape.setter
  def shape(self, val):
    self._attrs["shape"] = val

  @property
  def axis(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/indicator/

    :rtype: LayoutAxis
    """
    return self.sub_data("axis", LayoutAxis)


class DataIndicator(DataChart):

  @property
  def vmax(self):
    return self._attrs["vmax"]

  @vmax.setter
  def vmax(self, val):
    self._attrs["vmax"] = val

  def domain(self, x, y):
    """
    Description:
    ------------

    https://plot.ly/javascript/indicator/

    :param x:
    :param y:
    """
    self._attrs['domain'] = {"x": x, 'y': y}

  @property
  def title(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/indicator/

    :rtype: DataTitle
    """
    return self.sub_data("title", DataTitle)

  @property
  def number(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/indicator/

    :rtype: DataNumber
    """
    return self.sub_data("number", DataNumber)

  @property
  def gauge(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/indicator/

    :rtype: DataGauge
    """
    if 'gauge' not in self.mode:
      self.mode = "%s+gauge" % self.mode
    return self.sub_data("gauge", DataGauge)

  def add_prefix(self, text):
    self.number.prefix = text
    return self

  def add_title(self, text):
    """

    delta.data.add_title("<b style='color:red'>test</b>")

    https://plot.ly/javascript/indicator/

    :param text:

    :return:
    """
    self.title.text = text
    return self

  @property
  def delta(self):
    """
    Description:
    ------------

    https://plot.ly/javascript/3d-surface-plots/

    :rtype: DataDelta
    """
    return self.sub_data("delta", DataDelta)


class DataBox(DataChart):

  @property
  def boxpoints(self):
    return self._attrs["boxpoints"]

  @boxpoints.setter
  def boxpoints(self, val):
    self._attrs["boxpoints"] = val

  @property
  def boxmean(self):
    return self._attrs["boxmean"]

  @boxmean.setter
  def boxmean(self, val):
    self._attrs["boxmean"] = val

  @property
  def jitter(self):
    return self._attrs["jitter"]

  @jitter.setter
  def jitter(self, val):
    self._attrs["jitter"] = val

  @property
  def whiskerwidth(self):
    return self._attrs["whiskerwidth"]

  @whiskerwidth.setter
  def whiskerwidth(self, val):
    self._attrs["whiskerwidth"] = val

  @property
  def pointpos(self):
    return self._attrs["pointpos"]

  @pointpos.setter
  def pointpos(self, val):
    self._attrs["pointpos"] = val


class DataCandle(DataChart):

  @property
  def close(self):
    return self._attrs["close"]

  @close.setter
  def close(self, val):
    self._attrs["close"] = val

  @property
  def high(self):
    return self._attrs["high"]

  @high.setter
  def high(self, val):
    self._attrs["high"] = val

  @property
  def low(self):
    return self._attrs["low"]

  @low.setter
  def low(self, val):
    self._attrs["low"] = val

  @property
  def open(self):
    return self._attrs["open"]

  @open.setter
  def open(self, val):
    self._attrs["open"] = val

  @property
  def increasing(self):
    """
    Description:
    ------------

    :rtype: DataMove

    :return:
    """
    return self.sub_data("increasing", DataMove)

  @property
  def decreasing(self):
    """
    Description:
    ------------

    :rtype: DataMove

    :return:
    """
    return self.sub_data("decreasing", DataMove)


class Pie(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(component=self, page=self.page, js_code=self.chartId)
    return self._chart

  @property
  def data(self) -> DataPie:
    """
    Description:
    ------------

    :rtype: DataPie

    :return:
    """
    if not self._traces:
      self._traces.append(DataPie(page=self.page, component=self))
    return self._traces[-1]

  def add_trace(self, data, type='pie', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = self.options.type
    if mode is not None:
      c_data['mode'] = self.options.mode or mode
    self._traces.append(DataPie(component=self, page=self.page, attrs=c_data))
    return self

  def add_dataset(self, data, label, colors=None, opacity=None, kind="pie"):
    series = {"label": [], "values": []}
    for i, x in enumerate(self._labels):
      series["label"].append(x)
      series["values"].append(data[i])
    trace = self.add_trace(series, type=kind)
    current_trace = trace.traces()
    current_trace.name = label
    return current_trace

  _js__builder__ = '''
      if(data.python){
        result = []; 
        dataSet = {label: [], values: [], name: data.series, type: options.type, mode: options.mode, marker: {}};
        if(typeof options.attrs !== undefined){ for(var attr in options.attrs){dataSet[attr] = options.attrs[attr]} };
        if(typeof options.marker !== undefined){
          for(var attr in options.marker){dataSet.marker[attr] = options.marker[attr]}};
        data.datasets.forEach(function(rec, i){
          dataSet.label = rec.x; dataSet.values = rec.y}); result.push(dataSet)
      } else {
        var temp = {}; var labels = []; var uniqLabels = {}; var result = [] ;
        options.y_columns.forEach(function(series){temp[series] = {}});
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(rec[name] !== undefined){
              if(!(rec[options.x_column] in uniqLabels)){
                labels.push(rec[options.x_column]); uniqLabels[rec[options.x_column]] = true};
              temp[name][rec[options.x_column]] = rec[name]}})});
        options.y_columns.forEach(function(series){
          dataSet = {label: [], values: [], name: series, type: options.type, mode: options.mode, marker: {}};
          if(typeof options.attrs !== undefined){
            for(var attr in options.attrs){dataSet[attr] = options.attrs[attr]}};
          if(typeof options.marker !== undefined){ 
            for(var attr in options.marker){dataSet.marker[attr] = options.marker[attr]} };
          labels.forEach(function(x, i){
            dataSet.label.push(x);
            if(temp[series][x] == undefined){dataSet.values.push(null)} else{dataSet.values.push(temp[series][x])}
          }); result.push(dataSet)})
      }; return result'''


class Surface(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(page=self.page, js_code=self.chartId, component=self)
    return self._chart

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='surface', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataSurface(page=self.page, component=self, attrs=c_data))
    return self

  _js__builder__ = '''
      if(data.python){
        result = []; 
        data.datasets.forEach(function(dataset, i){
          result.push( {z: dataset, type: options.type} ) 
        }); console.log(result);
      } else {
        var labels = []; var result = [] ;
        data.series.forEach(function(name, i){
          result.push( {z: data.datasets[i], type: options.type} );
        })
      }; return result'''


class Scatter3D(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(page=self.page, component=self, js_code=self.chartId)
    return self._chart

  @property
  def layout(self) -> Layout3D:
    if self._layout is None:
      self._layout = Layout3D(page=self.page, component=self)
    return self._layout

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='scatter3d', mode="lines"):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = self.options.type
    if mode is not None:
      c_data['mode'] = self.options.mode or mode
    self._traces.append(DataSurface(component=self, page=self.page, attrs=c_data))
    return self

  _js__builder__ = '''
      var temp = {}; var tempZ = {}; var labels = []; var uniqLabels = {}; var result = [] ;
      options.y_columns.forEach(function(series){temp[series] = {}});
      options.y_columns.forEach(function(series){tempZ[series] = {}});
      data.forEach(function(rec){ 
        options.y_columns.forEach(function(name){
          if(rec[name] !== undefined){
            if(!(rec[options.x_column] in uniqLabels)){
              labels.push(rec[options.x_column]); uniqLabels[rec[options.x_column]] = true};
            temp[name][rec[options.x_column]] = rec[name];
            tempZ[name][rec[options.x_column]] = rec[options.z_axis];
          }})});
      options.y_columns.forEach(function(series){
        dataSet = {x: [], y: [], z: [], name: series, type: options.type, mode: options.mode, marker: {}};
        if(typeof options.attrs !== undefined){ for(var attr in options.attrs){dataSet[attr] = options.attrs[attr]} };
        if(typeof options.marker !== undefined){ 
          for(var attr in options.marker){dataSet.marker[attr] = options.marker[attr]} };
        labels.forEach(function(x, i){
          dataSet.x.push(x);
          if(temp[series][x] == undefined){dataSet.y.push(null)} else{dataSet.y.push(temp[series][x])};
          if(tempZ[series][x] == undefined){dataSet.y.push(null)} else{dataSet.z.push(tempZ[series][x])};
        }); result.push(dataSet)});
      return result'''


class Mesh3d(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(page=self.page, component=self, js_code=self.chartId)
    return self._chart

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='mesh3d', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataSurface(component=self, page=self.page, attrs=c_data))
    return self


class Indicator(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(page=self.page, component=self, js_code=self.chartId)
    return self._chart

  def add_trace(self, data, type='indicator', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataIndicator(page=self.page, component=self, attrs=c_data))
    return self

  _js__builder__ = '''
      var dataset = {value: data, type: options.type, mode: options.mode, delta: {}};
      if(typeof options.delta !== undefined){
        for(var attr in options.delta){dataset.delta[attr] = options.delta[attr]}};
      return [dataset]'''


class ScatterPolar(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(page=self.page, component=self, js_code=self.chartId)
    return self._chart

  def add_trace(self, data, type='scatterpolar', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataChart(page=self.page, component=self, attrs=c_data))
    self.data.fill = 'toself'
    return self


class Box(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(page=self.page, component=self, js_code=self.chartId)
    return self._chart

  @property
  def layout(self) -> LayoutBox:
    """
    Description:
    ------------

    :rtype: LayoutBox
    """
    if self._layout is None:
      self._layout = LayoutBox(page=self.page, component=self)
    return self._layout

  def add_trace(self, data, type='box', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataBox(page=self.page, component=self, attrs=c_data))
    return self

  def add_dataset(self, data, label, colors=None, opacity=None, kind="pie"):
    self.add_trace({"x": data})


class CandleStick(Chart):

  @property
  def chart(self) -> JsPlotly.Pie:
    """
    Description:
    ------------

    :rtype: JsPlotly.Pie
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(component=self, page=self.page, js_code=self.chartId)
    return self._chart

  @property
  def layout(self) -> LayoutBox:
    """
    Description:
    ------------

    :rtype: LayoutBox
    """
    if self._layout is None:
      self._layout = LayoutBox(component=self, page=self.page)
    return self._layout

  def add_trace(self, data, type='candlestick', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataCandle(page=self.page, component=self, attrs=c_data))
    return self
