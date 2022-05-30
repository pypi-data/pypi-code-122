#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.py import primitives
from epyk.core.html import Html
from epyk.core.css import Colors
from epyk.core.js import JsUtils
from epyk.core.js.packages import JsNvd3
from epyk.core.js.packages import JsD3
from epyk.core.html.options import OptChart
from epyk.core.html.options import OptChartNvd3


class Chart(Html.Html):
  name = 'NVD3'
  requirements = ('nvd3', )
  _option_cls = OptChart.OptionsChart

  def __init__(self,  page: primitives.PageModel, width, height, options, html_code, profile):
    self.seriesProperties, self.__chartJsEvents, self.height = {'static': {}, 'dynamic': {}}, {}, height[0]
    super(Chart, self).__init__(page, [], html_code=html_code, profile=profile, options=options,
                                css_attrs={"width": width, "height": height})
    self._d3, self.html_items, self._datasets, self._labels = None, [], [], None
    self.style.css.margin_left = 10
    self.style.css.margin_right = 10

  @property
  def shared(self) -> OptChartNvd3.OptionsChartSharedNVD3:
    """
    Description:
    -----------
    All the common properties shared between all the charts.
    This will ensure a compatibility with the plot method.

    Usage::

      line = page.ui.charts.nvd3.bar()
      line.shared.x_label("x axis")
    """
    return OptChartNvd3.OptionsChartSharedNVD3(self)

  @property
  def options(self) -> OptChart.OptionsChart:
    """
    Description:
    -----------
    Property to the component options.
    Options can either impact the Python side or the Javascript builder.

    Python can pass some options to the JavaScript layer.

    :rtype: OptChart.OptionsChart
    """
    return super().options

  @property
  def chartId(self):
    """
    Description:
    ------------
    Return the Javascript variable of the chart.
    """
    return "%s_obj" % self.htmlCode

  @property
  def data(self):
    """
    Description:
    -----------
    Property to the last dataset added to the NVD3 chart.
    Use the function traces to get a specific series from the chart object.
    """
    return self._datasets[-1]

  def traces(self, i: int = None):
    """
    Description:
    ------------
    Get a specific series from the datasets attributes in the NVD3 chart.

    Usage::

    Attributes:
    ----------
    :param int i: Optional. An Index number.
    """
    if i is None:
      return self._datasets[-1]

    return self._datasets[i]

  def click(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------
    This function is not implemented.

    Usage::

    Attributes:
    ----------
    :param js_funcs: List | String. Required. Javascript functions.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    raise NotImplementedError()

  def add_trace(self, data, name=""):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param data:
    :param name:
    """
    dataset = {"values": data, 'key': name}
    next_index = len(self._datasets)
    if len(self.options.colors) > next_index:
      dataset['color'] = self.options.colors[next_index]
    self._datasets.append(dataset)
    return self

  def labels(self, values):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param values: List. The different values for the x axis.
    """
    self._labels = values

  def add_dataset(self, data, label, colors=None, opacity=None, kind=None):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param data: List. The list of points (float).
    :param label: String. Optional. The series label (visible in the legend).
    :param colors: List. Optional. The color for this series. Default the global definition.
    :param opacity: Number. Optional. The opacity factory from 0 to 1.
    :param kind: String. Optional. THe series type. Default to the chart type if not supplied.
    """
    return self.add_trace([{"x": l, "y": data[i]} for i, l in enumerate(self._labels)], name=label)

  @property
  def d3(self) -> JsD3.D3Select:
    """
    Description:
    ------------
    Property to the underlying D3 module.

    Usage::

    :rtype: JsD3.D3Select
    """
    if self._d3 is None:
      self._d3 = JsD3.D3Select(page=self.page, selector="d3.select('#%s')" % self.htmlCode, set_var=False,
                               component=self)
    return self._d3

  def colors(self, hex_values: list):
    """
    Description:
    -----------
    Set the colors of the chart.

    hex_values can be a list of string with the colors or a list of tuple to also set the bg colors.
    If the background colors are not specified they will be deduced from the colors list changing the opacity.

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
    self.dom.color(line_colors)
    for i, rec in enumerate(self._datasets):
      rec['color'] = self.options.colors[i]

  def build(self, data=None, options=None, profile=None, component_id=None):
    """
    Description:
    ------------
    Return the JavaScript fragment to refresh the component content.

    Usage::

    Attributes:
    ----------
    :param data:
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    :param component_id: String. Optional. Not used for this component.
    """
    if data is not None:
      js_convertor = "%s%s" % (self.name, self.__class__.name)
      self.page.properties.js.add_constructor(
        js_convertor, "function %s(data, options){%s}" % (js_convertor, self._js__builder__))
      profile = self.with_profile(profile, event="Builder", element_id=self.chartId)
      if profile:
        js_func_builder = JsUtils.jsConvertFncs(
          ["var result = %s(data, options)" % js_convertor], toStr=True, profile=profile)
        js_convertor = "(function(data, options){%s; return result})" % js_func_builder
      return '''
        d3.select('#%(htmlCode)s').datum(%(chartFnc)s(%(data)s, %(options)s)).transition().duration(500).call(%(chart)s); 
        nv.utils.windowResize(%(chart)s.update)''' % {
        'htmlCode': self.htmlCode, 'chartFnc': js_convertor, "data": JsUtils.jsConvertData(data, None),
        "options":  self.options.config_js(options), 'chart': self.dom.var}

    return JsUtils.jsConvertFncs([self.dom.set_var(True), self.dom.xAxis,  self.dom.yAxis,
                                  self.d3.datum(self._datasets).call(self.dom.var),
                                  "nv.utils.windowResize(function() { %s.update() })" % self.dom.var], toStr=True)[4:]

  def __str__(self):
    self.style.css.width = "calc(100%% - %spx)" % (
      int(self.style.css.margin_left[:-2]) + int(self.style.css.margin_right[:-2]))
    self.page.properties.js.add_builders(self.build())
    str_items = "".join([h.html() for h in self.html_items])
    return '%s<svg %s></svg>' % (str_items, self.get_attrs(css_class_names=self.style.get_classes()))


class ChartLine(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3Line:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3Line
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3Line(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  _js__builder__ = '''
      if(data.python){
        result = [];
        data.datasets.forEach(function(rec, i){
          result.push( {key: data.series[i], values: rec, labels: data.labels} )})
      } else {
        var temp = {}; var labels = []; var uniqLabels = {};
        options.y_columns.forEach(function(series){temp[series] = {}});
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(typeof rec[name] !== undefined){
              if (!(rec[options.x_axis] in uniqLabels)){
                labels.push(rec[options.x_axis]); uniqLabels[rec[options.x_axis]] = true};
              temp[name][rec[options.x_axis]] = rec[name]}})
        }); result = [];
        options.y_columns.forEach(function(series){
          dataSet = {key: series, values: [], labels: labels};
          labels.forEach(function(x, i){
            var value = temp[series][x]; 
            if (isNaN(value)) {value = null};
            if (value !== undefined) {dataSet.values.push({y: value, x: i, label: x})}
          }); result.push(dataSet)})
      }; return result'''


class ChartScatter(ChartLine):

  @property
  def dom(self) -> JsNvd3.JsNvd3Scatter:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3Scatter
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3Scatter(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def click(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param js_funcs: List | String. Required. Javascript functions.
    :param profile: Boolean | Dictionary. Required. A flag to set the component performance storage.
    :param source_event: String. Required. The source target for the event.
    :param on_ready: Boolean. Required. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.scatter.dispatch.on('elementClick', function(event){ %s })" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True)))
    return self


class ChartCumulativeLine(ChartLine):

  @property
  def dom(self) -> JsNvd3.JsNvd3CumulativeLine:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3CumulativeLine
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3CumulativeLine(page=self.page, js_code=self.chartId, component=self)
    return self._dom


class ChartFocusLine(ChartLine):

  @property
  def dom(self) -> JsNvd3.JsNvd3LineWithFocus:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3LineWithFocus
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3LineWithFocus(page=self.page, js_code=self.chartId, component=self)
    return self._dom


class ChartBar(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3Bar:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3Bar
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3Bar(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def colors(self, hex_values: list):
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
    self.dom.color(line_colors)
    for i, rec in enumerate(self._datasets):
      rec['color'] = self.options.colors[i]

  def click(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param js_funcs: List | String. Required. Javascript functions.
    :param profile: Boolean | Dictionary. Required. A flag to set the component performance storage.
    :param source_event: String. Required. The source target for the event.
    :param on_ready: Boolean. Required. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.selectAll('.nv-bar').on('click', function(event){%s})" % (
      self.d3.varId, JsUtils.jsConvertFncs(js_funcs, toStr=True)))
    return self

  def add_dataset(self, data, label, colors=None, opacity=None, kind=None):
    return self.add_trace([{"label": l, "y": data[i], "x": l} for i, l in enumerate(self._labels)], name=label)

  _js__builder__ = '''
      if(data.python){
        result = [];
        data.datasets.forEach(function(rec, i){
          result.push( {key: data.series[i], values: rec, labels: data.labels} )})
      } else {
        var temp = {}; var labels = []; var uniqLabels = {};
        options.y_columns.forEach(function(series){temp[series] = {}}) ;
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(rec[name] !== undefined){
              if (!(rec[options.x_axis] in uniqLabels)){
                labels.push(rec[options.x_axis]); uniqLabels[rec[options.x_axis]] = true};
              temp[name][rec[options.x_axis]] = rec[name]}})
        }); var result = [];
        options.y_columns.forEach(function(series){
          dataSet = {key: series, values: [], labels: labels};
          labels.forEach(function(x, i){
            var value = temp[series][x]; 
            if (isNaN(value)) { value = null};
            if (value !== undefined) {dataSet.values.push({y: value, x: i, label: x})}
          }); result.push(dataSet)})
      }; return result'''


class ChartHorizontalBar(ChartBar):

  @property
  def dom(self) -> JsNvd3.JsNvd3MultiBarHorizontal:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3MultiBarHorizontal
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3MultiBarHorizontal(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def add_dataset(self, data, label, colors=None, opacity=None, kind=None):
    return self.add_trace([{"label": l, "y": data[i]} for i, l in enumerate(self._labels)], name=label)


class ChartMultiBar(ChartBar):

  @property
  def dom(self) -> JsNvd3.JsNvd3MultiBar:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3MultiBar
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3MultiBar(page=self.page, js_code=self.chartId, component=self)
    return self._dom

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
    self.dom.barColor(line_colors)
    for i, rec in enumerate(self._datasets):
      rec['color'] = self.options.colors[i]

  def add_dataset(self, data, label, colors=None, opacity=None, kind=None):
    return self.add_trace([{"label": l, "y": data[i]} for i, l in enumerate(self._labels)], name=label)


class ChartPie(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3Pie:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3Pie
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3Pie(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  _js__builder__ = '''
      if(data.python){
        data.datasets.forEach(function(dataset, i){
          result = dataset;  
        });
      } else {
        var temp = {}; var labels = {};
        data.forEach(function(rec){ 
          if(!(rec[options.x_axis] in temp)){temp[rec[options.x_axis]] = {}};
          options.y_columns.forEach(function(name){
            labels[name] = true; if(rec[name] !== undefined) {
              if (!(name in temp[rec[options.x_axis]])){temp[rec[options.x_axis]][name] = rec[name]} 
              else {temp[rec[options.x_axis]][name] += rec[name]}}  }) ;
        });
        var labels = Object.keys(labels); result = [];
        for(var series in temp){
          var values = {y: 0, x: series};
          labels.forEach(function(label){
            if(temp[series][label] !== undefined){values.y = temp[series][label]}});
          result.push(values)}
      }; return result'''

  def click(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param js_funcs: List | String. A Javascript Python function.
    :param profile: Boolean. Optional. Set to true to get the profile for the function on the Javascript console.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    self.onReady("%s.pie.dispatch.on('elementClick', function(event){ %s })" % (
      self.dom.varName, JsUtils.jsConvertFncs(js_funcs, toStr=True)))
    return self

  def add_trace(self, data, name=""):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param data:
    :param name:
    """
    self.dom.color(self.options.colors)
    self._datasets = data
    return self


class ChartArea(ChartBar):

  @property
  def dom(self) -> JsNvd3.JsNvd3Area:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3Area
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3Area(page=self.page, js_code=self.chartId, component=self)
    return self._dom


class ChartHistoBar(ChartBar):

  @property
  def dom(self) -> JsNvd3.JsNvd3HistoricalBar:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3HistoricalBar
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3HistoricalBar(page=self.page, js_code=self.chartId, component=self)
    return self._dom


class ChartParallelCoord(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3ParallelCoordinates:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3ParallelCoordinates
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3ParallelCoordinates(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def set_dimension_names(self, dimensions):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param dimensions:
    """
    self.__dimensions = dimensions
    self.dom.dimensionNames(dimensions)
    return self

  def add_trace(self, data, name=""):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param data:
    :param name:
    """
    self._datasets = data
    return self


class ChartSunbrust(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3Sunburst:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3Sunburst
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3Sunburst(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def set_rcolors(self, color, data):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param color: String.
    :param data:
    """
    for rec in data:
      rec['color'] = color
      if 'children' in rec:
        self.set_rcolors(color, rec['children'])

  def add_trace(self, data, name=""):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param data:
    :param name: String. Optional.
    """
    for i, rec in enumerate(data):
      rec['color'] = self.page.theme.colors[i+1]
      self.set_rcolors(rec['color'], rec['children'])
    self._datasets = [{'name': name, 'children': data, 'color': self.options.colors[0]}]
    return self

  _js__builder__ = '''
      var result = [{name: options.x_axis, children: []}]; var sizeTree = options.y_columns.length-1;
      data.forEach(function(rec){
        var path = []; var tmpResultLevel = result[0].children; var branchVal = 0;
        options.y_columns.forEach(function(s, i){
          var treeLevel = -1; 
          tmpResultLevel.forEach(function(l, j){if(l.name == rec[s]){treeLevel = j}});
          if(i == sizeTree){
            if(treeLevel >= 0){
              tmpResultLevel[treeLevel].size += rec[options.x_axis]}
            else{tmpResultLevel.push({name: rec[s], size: rec[options.x_axis]})}
          }else{
            if(treeLevel < 0 ){
              tmpResultLevel.push({name: rec[s], children: []}); treeLevel = tmpResultLevel.length - 1};
              tmpResultLevel = tmpResultLevel[treeLevel].children}
        })}); return result'''


class ChartBoxPlot(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3BoxPlot:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3BoxPlot
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3BoxPlot(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def add_box(self, q1, q3=None, outliers=None, maxRegularValue=None, mean=None, median=None, minRegularValue=None,
              minOutlier=None, maxOutlier=None, title=None):
    """
    Description:
    ------------

    Usage::

    https://github.com/nvd3-community/nvd3/blob/gh-pages/examples/boxPlotCustomModel.html

    Attributes:
    ----------
    :param q1:
    :param q3:
    :param outliers:
    :param maxRegularValue:
    :param mean:
    :param median:
    :param minRegularValue:
    :param minOutlier:
    :param maxOutlier:
    """
    names = ['q1', 'median', 'q3', 'outlData', 'maxRegularValue', 'mean', 'minRegularValue', 'minOutlier', 'maxOutlier']
    row = {}
    for i, val in enumerate([q1, median, q3, outliers, maxRegularValue, mean, minRegularValue, minOutlier, maxOutlier]):
      if val is not None:
        row[names[i]] = val
      elif names[i] == 'outlData':
        row['outlData'] = []
    series_id = len(self._datasets) - 1
    row['seriesColor'] = self.options.colors[series_id]
    row['title'] = title or "Series %s" % series_id
    self._datasets.append(row)
    return self

  def add_trace(self, data, name=""):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param data:
    :param name:
    """
    self._datasets = data
    return self


class ChartCandlestick(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3CandlestickBar:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3CandlestickBar
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3CandlestickBar(page=self.page, js_code=self.chartId, component=self)
    return self._dom


class ChartOhlcBar(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3OhlcBar:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3OhlcBar
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3OhlcBar(page=self.page, js_code=self.chartId, component=self)
    return self._dom


class ChartForceDirected(Chart):

  @property
  def dom(self) -> JsNvd3.JsNvd3ForceDirectedGraph:
    """
    Description:
    ------------

    Usage::

    :rtype: JsNvd3.JsNvd3ForceDirectedGraph
    """
    if self._dom is None:
      self._dom = JsNvd3.JsNvd3ForceDirectedGraph(page=self.page, js_code=self.chartId, component=self)
    return self._dom

  def add_trace(self, data: dict, name: str = ""):
    """
    Description:
    ------------

    Usage::

    Attributes:
    ----------
    :param dict data:
    :param str name:
    """
    for d in data.get('nodes', []):
      d['color'] = self.options.colors[d.get('group', 1)]
    self._datasets = data
    return self
