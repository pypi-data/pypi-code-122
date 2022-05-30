#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Union, Optional
from epyk.core.html.options import Options
from epyk.core.js.packages import packageImport
from epyk.core.js import JsUtils
from epyk.core.html.options import OptChart


class OptionsChartSharedChartJs(OptChart.OptionsChartShared):

  def x_format(self, js_funcs, profile: Union[bool, dict] = None):
    self.component.options.xAxes.ticks.callback(js_funcs, profile)
    return self

  def x_format_money(self, symbol="", digit=0, thousand_sep=".", decimal_sep=",", fmt="%v %s", factor=None, alias=""):
    self.component.options.scales.xAxes.ticks.toMoney(symbol, digit, thousand_sep, decimal_sep, fmt, factor, alias)
    return self

  def x_format_number(self, factor=1, alias=None, digits=0, thousand_sep="."):
    self.component.options.scales.xAxes.ticks.scale(factor, alias, digits, thousand_sep)
    return self

  def x_label(self, value: str):
    """
    Description:
    -----------
    Set the label of the x axis.

    Attributes:
    ----------
    :param value: String. The axis label.
    """
    if min(self.component.page.imports.pkgs.chart_js.version) > '3.0.0':
      self.component.options.scales.xAxes.title.text = value
      self.component.options.scales.xAxes.title.display = True
    else:
      self.component.options.scales.xAxes.scaleLabel.label(value)
    return self

  def x_tick_count(self, num: int):
    self.component.options.scales.xAxes.ticks.maxTicksLimit = num
    return self

  def y_format(self, js_funcs, profile: Union[bool, dict] = None):
    self.component.options.yAxes.ticks.callback(js_funcs, profile)
    return self

  def y_format_money(self, symbol: str = "", digit: int = 0, thousand_sep: int = ".", decimal_sep: int = ",",
                     fmt: str = "%v %s", factor: int = None, alias: str = ""):
    self.component.options.scales.yAxes.ticks.toMoney(symbol, digit, thousand_sep, decimal_sep, fmt, factor, alias)
    return self

  def y_format_number(self, factor: int = 1, alias=None, digits=0, thousand_sep="."):
    self.component.options.scales.yAxes.ticks.scale(factor, alias, digits, thousand_sep)
    return self

  def y_label(self, value: str):
    """
    Description:
    -----------
    Set the label of the y axis.

    Attributes:
    ----------
    :param value: String. The axis label.
    """
    if min(self.component.page.imports.pkgs.chart_js.version) > '3.0.0':
      self.component.options.scales.yAxes.title.text = value
      self.component.options.scales.yAxes.title.display = True
    else:
      self.component.options.scales.yAxes.scaleLabel.label(value)
    return self

  def y_tick_count(self, num: int):
    self.component.options.scales.yAxes.ticks.maxTicksLimit = num
    return self


class OptionLabelFont(Options):

  @property
  def size(self):
    """
    Description:
    -----------
    Change the font-size.
    """
    return self._config_get()

  @size.setter
  def size(self, num: int):
    self._config(num)

  @property
  def family(self):
    """
    Description:
    -----------
    Change the font family.

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/subtitle/basic.html
    """
    return self._config_get()

  @family.setter
  def family(self, text: int):
    self._config(text)

  @property
  def weight(self):
    """
    Description:
    -----------
    Change the font weight.

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/subtitle/basic.html
    """
    return self._config_get()

  @weight.setter
  def weight(self, text: int):
    self._config(text)

  @property
  def style(self):
    """
    Description:
    -----------
    Change the CSS font style property.

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/subtitle/basic.html
    """
    return self._config_get()

  @style.setter
  def style(self, text: int):
    self._config(text)


class OptionAxesTicksMajor(Options):
  @property
  def fontColor(self):
    """
    Description:
    -----------
    Change the font color.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @fontColor.setter
  def fontColor(self, val: str):
    self._config(val)


class OptionAxesTicks(Options):

  @property
  def color(self):
    """
    Description:
    -----------
    Change the font color.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @color.setter
  def color(self, val: str):
    self._config(val)

  @property
  def fontColor(self):
    """
    Description:
    -----------
    Change the font color.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @fontColor.setter
  def fontColor(self, val: str):
    self._config(val)

  @property
  def textStrokeColor(self):
    """
    Description:
    -----------
    Change the font color.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @textStrokeColor.setter
  def textStrokeColor(self, val: str):
    self._config(val)

  @property
  def backdropColor(self):
    """
    Description:
    -----------
    Change the font color.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @backdropColor.setter
  def backdropColor(self, val: str):
    self._config(val)

  @property
  def fontSize(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @fontSize.setter
  def fontSize(self, val: int):
    self._config(val)

  @property
  def beginAtZero(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @beginAtZero.setter
  def beginAtZero(self, flag: bool):
    self._config(flag)

  @property
  def major(self) -> OptionAxesTicksMajor:
    """
    Description:
    ------------

    :rtype: OptionAxesTicksMajor
    """
    return self._config_sub_data("major", OptionAxesTicksMajor)

  @property
  def minor(self) -> OptionAxesTicksMajor:
    """
    Description:
    ------------

    :rtype: OptionAxesTicksMajor
    """
    return self._config_sub_data("minor", OptionAxesTicksMajor)

  @property
  def max(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @max.setter
  def max(self, val):
    self._config(val)

  @property
  def min(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @min.setter
  def min(self, val):
    self._config(val)

  @property
  def mirror(self):
    """
    Description:
    ------------
    Flips tick labels around axis, displaying the labels inside the chart instead of outside.
    Note: Only applicable to vertical scales.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @mirror.setter
  def mirror(self, val):
    self._config(val)

  @property
  def maxTicksLimit(self):
    """
    Description:
    ------------
    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @maxTicksLimit.setter
  def maxTicksLimit(self, val):
    self._config(val)

  @property
  def suggestedMin(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @suggestedMin.setter
  def suggestedMin(self, val):
    self._config(val)

  @property
  def suggestedMax(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @suggestedMax.setter
  def suggestedMax(self, val):
    self._config(val)

  @property
  def stepSize(self):
    """
    Description:
    -----------
    Force the step size.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
      https://www.chartjs.org/docs/3.7.0/samples/scales/linear-step-size.html
    """
    return self._config_get()

  @stepSize.setter
  def stepSize(self, val: int):
    self._config(val)

  @packageImport("accounting")
  def scale(self, factor: int = 1000, alias: str = None, digits: int = 0, thousand_sep: str = "."):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param factor:
    :param alias:
    :param digits:
    :param thousand_sep:
    """
    thousand_sep = JsUtils.jsConvertData(thousand_sep, None)
    alias = alias or {1000: "k", 1000000: "m"}.get(factor, "")
    self._config(
      "function(label, index, labels) {var pointVal = label/%s; return accounting.formatNumber(pointVal, %s, %s) + '%s'}" % (
        factor, digits, thousand_sep, alias), name="callback", js_type=True)
    return self

  @packageImport("accounting")
  def toMoney(self, symbol="", digit=0, thousand_sep=".", decimal_sep=",", fmt="%v %s", factor=None, alias=""):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param symbol:
    :param digit:
    :param thousand_sep:
    :param decimal_sep:
    """
    thousand_sep = JsUtils.jsConvertData(thousand_sep, None)
    decimal_sep = JsUtils.jsConvertData(decimal_sep, None)
    if not alias:
      alias = {1000: "k", 1000000: "m"}.get(factor, alias)
    self._config("function(label, index, labels) {return accounting.formatMoney(label, %s, %s, %s, %s, '%s')}" % (
      "'%s'+ %s" % (alias, symbol), digit, thousand_sep, decimal_sep, fmt), name="callback", js_type=True)
    return self

  @packageImport("accounting")
  def toNumber(self, digit=0, thousand_sep="."):
    """
    Description:
    -----------
    Convert to number using the accounting Javascript module-

    Related Pages:

      https://openexchangerates.github.io/accounting.js/

    Attributes:
    ----------
    :param digit: Integer. The number of digit to be displayed
    :param thousand_sep: The thousand symbol separator
    """
    thousand_sep = JsUtils.jsConvertData(thousand_sep, None)
    self._config("function(label, index, labels) {return accounting.formatNumber(label, %s, %s)}" % (
      digit, thousand_sep), name="callback", js_type=True)
    return self

  def callback(self, js_funcs, profile=None):
    """
    Description:
    -----------


    Related Pages:

      https://www.chartjs.org/docs/latest/samples/scale-options/ticks.html

    Attributes:
    ----------
    """
    self._config("function(val, index) {return (function(obj){return new Date(obj.getLabelForValue(val))})(this).toISOString().split('T')[0]}", js_type=True)
    return self

  def userCallback(self, js_funcs, profile=None):
    """
    Description:
    -----------
    Convert to number using the accounting Javascript module-

    Related Pages:

      https://openexchangerates.github.io/accounting.js/

    Attributes:
    ----------
    """
    self._config("function(label, index, labels) {console.log(label); return 1}", js_type=True)
    return self

  def mapTo(self, mapping: dict):
    """
    Description:
    -----------
    Map the values to a static dictionary.

    Attributes:
    ----------
    :param mapping: The mapping table.
    """
    self._config(
      "function(label, index, labels) {var mapping = %s; if (labels in mapping){return mapping[labels]}; return labels}" % mapping,
      name="callback", js_type=True)
    return self


class OptionLabels(Options):

  @property
  def fontColor(self):
    """
    Description:
    -----------
    Change the color.
    """
    return self._config_get()

  @fontColor.setter
  def fontColor(self, val: str):
    self._config(val)


class OptionAxesGridLine(Options):

  @property
  def display(self):
    """
    Description:
    -----------
    If false, do not display grid lines for this axis.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @display.setter
  def display(self, val: bool):
    self._config(val)

  @property
  def circular(self):
    """
    Description:
    -----------
    If true, gridlines are circular (on radar chart only).

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @circular.setter
  def circular(self, val):
    self._config(val)

  @property
  def color(self):
    """
    Description:
    -----------
    The color of the grid lines. If specified as an array, the first color applies to the first grid line, the second
    to the second grid line and so on.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @color.setter
  def color(self, val: str):
    self._config(val)

  @property
  def borderColor(self):
    """
    Description:
    -----------
    The color of the grid lines. If specified as an array, the first color applies to the first grid line, the second
    to the second grid line and so on.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @borderColor.setter
  def borderColor(self, val: str):
    self._config(val)

  @property
  def borderDash(self):
    """
    Description:
    -----------
    Length and spacing of dashes on grid lines.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @borderDash.setter
  def borderDash(self, val):
    self._config(val)

  @property
  def borderDashOffset(self):
    """
    Description:
    -----------
    Offset for line dashes.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @borderDashOffset.setter
  def borderDashOffset(self, val):
    self._config(val)

  @property
  def lineWidth(self):
    """
    Description:
    -----------
    Stroke width of grid lines.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @lineWidth.setter
  def lineWidth(self, val: int):
    self._config(val)

  @property
  def drawBorder(self):
    """
    Description:
    -----------
    If true, draw border at the edge between the axis and the chart area.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @drawBorder.setter
  def drawBorder(self, flag: bool):
    self._config(flag)

  @property
  def drawOnChartArea(self):
    """
    Description:
    -----------
    If true, draw lines on the chart area inside the axis lines.
    This is useful when there are multiple axes and you need to control which grid lines are drawn.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @drawOnChartArea.setter
  def drawOnChartArea(self, val):
    self._config(val)

  @property
  def drawTicks(self):
    """
    Description:
    -----------
    If true, draw lines beside the ticks in the axis area beside the chart.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @drawTicks.setter
  def drawTicks(self, val):
    self._config(val)

  @property
  def tickMarkLength(self):
    """
    Description:
    -----------
    Length in pixels that the grid lines will draw into the axis area.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @tickMarkLength.setter
  def tickMarkLength(self, val):
    self._config(val)

  @property
  def tickColor(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html
    """
    return self._config_get()

  @tickColor.setter
  def tickColor(self, val):
    self._config(val)

  @property
  def zeroLineWidth(self):
    """
    Description:
    -----------
    Stroke width of the grid line for the first index (index 0).

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @zeroLineWidth.setter
  def zeroLineWidth(self, val):
    self._config(val)

  @property
  def zeroLineColor(self):
    """
    Description:
    -----------
    Stroke color of the grid line for the first index (index 0).

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @zeroLineColor.setter
  def zeroLineColor(self, val: str):
    self._config(val)

  @property
  def zeroLineBorderDash(self):
    """
    Description:
    -----------
    Length and spacing of dashes of the grid line for the first index (index 0).

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @zeroLineBorderDash.setter
  def zeroLineBorderDash(self, val):
    self._config(val)

  @property
  def zeroLineBorderDashOffset(self):
    """
    Description:
    -----------
    Offset for line dashes of the grid line for the first index (index 0).

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @zeroLineBorderDashOffset.setter
  def zeroLineBorderDashOffset(self, val):
    self._config(val)

  @property
  def offsetGridLines(self):
    """
    Description:
    -----------
    If true, grid lines will be shifted to be between labels. This is set to true for a bar chart by default.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @offsetGridLines.setter
  def offsetGridLines(self, val):
    self._config(val)

  @property
  def z(self):
    """
    Description:
    -----------
    z-index of gridline layer. Values <= 0 are drawn under datasets, > 0 on top.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/styling.html#grid-line-configuration
    """
    return self._config_get()

  @z.setter
  def z(self, val):
    self._config(val)


class OptionAxesScaleLabel(Options):

  @property
  def display(self):
    return self._config_get()

  @display.setter
  def display(self, val: bool):
    self._config(val)

  @property
  def fontColor(self):
    return self._config_get()

  @fontColor.setter
  def fontColor(self, val: str):
    self._config(val)

  @property
  def labelString(self):
    return self._config_get()

  @labelString.setter
  def labelString(self, val: str):
    self._config(val)

  def label(self, value: str):
    """
    Description:
    ------------
    Shortcut to the labelString and display property.

    Attributes:
    ----------
    :param value: The label value.
    """
    self.labelString = value
    self.display = True


class OptionDisplayFormats(Options):

  @property
  def quarter(self):
    return self._config_get()

  @quarter.setter
  def quarter(self, val: str):
    self._config(val)


class OptionAxesTime(Options):

  @property
  def displayFormats(self) -> OptionDisplayFormats:
    """
    Description:
    ------------

    :rtype: OptionDisplayFormats
    """
    return self._config_sub_data("displayFormats", OptionDisplayFormats)


class OptionTitle(Options):

  @property
  def align(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/title/alignment.html
    """
    return self._config_get()

  @align.setter
  def align(self, text: str):
    self._config(text)

  @property
  def display(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/configuration/title.html
      https://www.chartjs.org/docs/latest/samples/other-charts/pie.html
    """
    return self._config_get()

  @display.setter
  def display(self, flag: bool):
    self._config(flag)

  @property
  def text(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/other-charts/pie.html
    """
    return self._config_get()

  @text.setter
  def text(self, val: str):
    self._config(val)

  @property
  def color(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/other-charts/pie.html
    """
    return self._config_get()

  @color.setter
  def color(self, val: str):
    self._config(val)

  @property
  def position(self):
    return self._config_get()

  @position.setter
  def position(self, val):
    self._config(val)

  @property
  def fontSize(self):
    return self._config_get()

  @fontSize.setter
  def fontSize(self, val):
    self._config(val)

  @property
  def fontFamily(self):
    return self._config_get()

  @fontFamily.setter
  def fontFamily(self, val):
    self._config(val)

  @property
  def fontColor(self):
    return self._config_get()

  @fontColor.setter
  def fontColor(self, val):
    self._config(val)

  @property
  def fontStyle(self):
    return self._config_get()

  @fontStyle.setter
  def fontStyle(self, val):
    self._config(val)

  @property
  def padding(self):
    return self._config_get()

  @padding.setter
  def padding(self, val):
    self._config(val)

  @property
  def lineHeight(self):
    return self._config_get()

  @lineHeight.setter
  def lineHeight(self, val):
    self._config(val)

  @property
  def font(self):
    """
    Description:
    ------------

    :rtype: OptionLabelFont
    """
    return self._config_sub_data("font", OptionLabelFont)


class OptionAxes(Options):

  @property
  def display(self):
    return self._config_get()

  @display.setter
  def display(self, flag: bool):
    self._config(flag)

  @property
  def distribution(self):
    return self._config_get()

  @distribution.setter
  def distribution(self, val):
    self._config(val)

  @property
  def reverse(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/other-charts/scatter-multi-axis.html
    """
    return self._config_get()

  @reverse.setter
  def reverse(self, flag: bool):
    self._config(flag)

  @property
  def type(self):
    return self._config_get()

  @type.setter
  def type(self, val: str):
    if val == "time":
      from epyk.core.js import Imports

      Imports.JS_IMPORTS["chart.js"]["req"] = [{'alias': 'moment'}]
      # Add the package moment.js is time is used
      # self._report.jsImports.add("moment")
    self._config(val)

  @property
  def stacked(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @stacked.setter
  def stacked(self, val: bool):
    self._config(val)

  @property
  def id(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @id.setter
  def id(self, val):
    self._config(val)

  @property
  def offset(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @offset.setter
  def offset(self, val):
    self._config(val)

  @property
  def position(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @position.setter
  def position(self, val):
    self._config(val)

  @property
  def suggestedMin(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @suggestedMin.setter
  def suggestedMin(self, val: float):
    self._config(val)

  @property
  def suggestedMax(self):
    """
    Description:
    -----------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @suggestedMax.setter
  def suggestedMax(self, val: float):
    self._config(val)

  @property
  def stepSize(self):
    """
    Description:
    -----------

    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @stepSize.setter
  def stepSize(self, val: int):
    self._config(val)

  @property
  def ticks(self) -> OptionAxesTicks:
    """
    Description:
    ------------

    :rtype: OptionAxesTicks
    """
    return self._config_sub_data("ticks", OptionAxesTicks)

  @property
  def time(self) -> OptionAxesTime:
    """
    Description:
    ------------

    :rtype: OptionAxesTime
    """
    return self._config_sub_data("time", OptionAxesTime)

  @property
  def gridLines(self) -> OptionAxesGridLine:
    """
    Description:
    ------------

    :rtype: OptionAxesGridLine
    """
    return self._config_sub_data("gridLines", OptionAxesGridLine)

  @property
  def grid(self) -> OptionAxesGridLine:
    """
    Description:
    ------------

    https://www.chartjs.org/docs/latest/samples/other-charts/scatter-multi-axis.html

    :rtype: OptionAxesGridLine
    """
    return self._config_sub_data("grid", OptionAxesGridLine)

  @property
  def ticks(self):
    """
    Description:
    ------------

    https://www.chartjs.org/docs/latest/axes/styling.html

    :rtype: OptionAxesTicks
    """
    return self._config_sub_data("grid", OptionAxesTicks)

  @property
  def title(self) -> OptionTitle:
    """
    Description:
    ------------
    Namespace: options.scales[scaleId].title, it defines options for the scale title.
    Note that this only applies to cartesian axes.

    Related Pages:

      https://www.chartjs.org/docs/latest/axes/labelling.html

    :rtype: OptionTitle
    """
    return self._config_sub_data("title", OptionTitle)

  @property
  def scaleLabel(self) -> OptionAxesScaleLabel:
    """
    Description:
    ------------

    :rtype: OptionAxesScaleLabel
    """
    return self._config_sub_data("scaleLabel", OptionAxesScaleLabel)

  def add_label(self, text: str, color: str = None):
    """
    Description:
    ------------

    :param text:
    :param color:
    """
    self.scaleLabel.display = True
    self.scaleLabel.labelString = text
    if color is not None:
      self.scaleLabel.fontColor = color
    return self

  def category(self, vals):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param vals:
    """
    self.type = "category"
    self.labels = vals


class OptionScalePointLabels(Options):

  @property
  def display(self):
    return self._config_get()

  @display.setter
  def display(self, flag: bool):
    self._config(flag)

  @property
  def centerPointLabels(self):
    return self._config_get()

  @centerPointLabels.setter
  def centerPointLabels(self, flag: bool):
    self._config(flag)

  @property
  def font(self) -> OptionLabelFont:
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/other-charts/polar-area-center-labels.html

    :rtype: OptionLabelFont
    """
    return self._config_sub_data("font", OptionLabelFont)


class OptionScaleR(Options):

  @property
  def pointLabels(self) -> OptionScalePointLabels:
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/other-charts/polar-area-center-labels.html

    :rtype: OptionScalePointLabels
    """
    return self._config_sub_data("pointLabels", OptionScalePointLabels)


class OptionScales(Options):

  @property
  def xAxes(self):
    """
    Description:
    ------------
    Shortcut property to the last x_axes definition.
    Use the function x_axes to be more specific.
    """
    return self.x_axes()

  @property
  def yAxes(self):
    """
    Description:
    ------------
    Shortcut property to the last y_axis definition.
    Use the function y_axis to be more specific.

    y_axis is useful when multiple y axes are used for the same chart.
    """
    return self.y_axis()

  def add_y_axis(self):
    """
    Description:
    ------------

    :rtype: OptionAxes
    """
    return self._config_sub_data("y", OptionAxes)

  def y_axis(self, i: int = None):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param i: Integer. optional. Default take the latest one.

    :rtype: OptionAxes
    """
    if min(self.component.page.imports.pkgs.chart_js.version) > '3.0.0':
      return self.add_y_axis()

    if "yAxes" not in self.js_tree:
      self._config_sub_data_enum("yAxes", OptionAxes)

    if i is None:
      return self.js_tree["yAxes"][-1]

    return self.js_tree["yAxes"][i]

  def add_x_axis(self):
    """
    Description:
    ------------
    Add a X axis to a chart component.

    :rtype: OptionAxes
    """
    return self._config_sub_data("x", OptionAxes)

  def x_axes(self, i: int = None):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param i: Integer. optional. Default take the latest one.

    :rtype: OptionAxes
    """
    if min(self.component.page.imports.pkgs.chart_js.version) > '3.0.0':
      return self.add_x_axis()

    if "xAxes" not in self.js_tree:
      self._config_sub_data_enum("xAxes", OptionAxes)

    if i is None:
      return self.js_tree["xAxes"][-1]

    return self.js_tree["xAxes"][i]

  @property
  def r(self) -> OptionScaleR:
    """
    Description:
    ------------

    :rtype: OptionScaleR
    """
    return self._config_sub_data("r", OptionScaleR)

  @property
  def x(self) -> OptionAxes:
    """
    Description:
    ------------

    :rtype: OptionScaleR
    """
    return self._config_sub_data("x", OptionAxes)

  @property
  def y(self) -> OptionAxes:
    """
    Description:
    ------------

    :rtype: OptionScaleR
    """
    return self._config_sub_data("y", OptionAxes)

  @property
  def y2(self) -> OptionAxes:
    """
    Description:
    ------------

    :rtype: OptionScaleR
    """
    return self._config_sub_data("y2", OptionAxes)


class OptionScaleGeo(Options):

  @property
  def projection(self):
    return self._config_get()

  @projection.setter
  def projection(self, val: str):
    self._config(val)

  @property
  def projectionScale(self):
    return self._config_get()

  @projectionScale.setter
  def projectionScale(self, num: int):
    self._config(num)

  def set_projection(self, js_funcs, profile: Union[bool, dict] = None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param js_funcs:
    :param profile:
    """
    self._config(
      "function (value){%s}" % JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile),
      name="projection", js_type=True)


class OptionScalesGeo(Options):

  @property
  def xy(self) -> OptionScaleGeo:
    """
    Description:
    ------------

    :rtype: OptionScaleGeo
    """
    return self._config_sub_data("xy", OptionScaleGeo)


class OptionPadding(Options):

  @property
  def left(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @left.setter
  def left(self, val):
    self._config(val)

  @property
  def right(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @right.setter
  def right(self, val):
    self._config(val)

  @property
  def top(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @top.setter
  def top(self, val):
    self._config(val)

  @property
  def bottom(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @bottom.setter
  def bottom(self, val):
    self._config(val)


class OptionLayout(Options):

  @property
  def padding(self) -> OptionScaleGeo:
    """
    Description:
    ------------

    :rtype: OptionPadding
    """
    return self._config_sub_data("padding", OptionPadding)


class OptionLegend(Options):

  @property
  def labels(self) -> OptionLabels:
    """
    Description:
    ------------

    :rtype: OptionLabels
    """
    return self._config_sub_data("labels", OptionLabels)

  @property
  def title(self) -> OptionTitle:
    """
    Description:
    ------------

    :rtype: OptionTitle
    """
    return self._config_sub_data("title", OptionTitle)

  @property
  def align(self):
    """
    Description:
    ------------
    Alignment of the legend.

    Related Pages:

      https://www.chartjs.org/docs/latest/configuration/legend.html

    """
    return self._config_get("center")

  @align.setter
  def align(self, val: str):
    self._config(val)

  @property
  def display(self):
    """
    Description:
    ------------
    Is the legend shown?

    Related Pages:

      https://www.chartjs.org/docs/latest/configuration/legend.html

    """
    return self._config_get(True)

  @display.setter
  def display(self, flag: bool):
    self._config(flag)

  @property
  def position(self):
    """
    Description:
    ------------
    Position of the legend
    values are top, left, bottom, right

    Related Pages:

      https://www.chartjs.org/docs/latest/configuration/legend.html

    """
    return self._config_get()

  @position.setter
  def position(self, val: str):
    self._config(val)

  @property
  def reverse(self):
    """
    Description:
    ------------
    Legend will show datasets in reverse order.

    Related Pages:

      https://www.chartjs.org/docs/latest/configuration/legend.html

    """
    return self._config_get(False)

  @reverse.setter
  def reverse(self, flag: bool):
    self._config(flag)

  @property
  def rtl(self):
    """
    Description:
    ------------
    true for rendering the legends from right to left.

    Related Pages:

      https://www.chartjs.org/docs/latest/configuration/legend.html

    """
    return self._config_get(False)

  @rtl.setter
  def rtl(self, flag):
    self._config(flag)


class OptionPoint(Options):

  @property
  def radius(self):
    """
    Description:
    ------------
    """
    return self._config_get(False)

  @radius.setter
  def radius(self, num: int):
    self._config(num)


class OptionLine(Options):

  @property
  def tension(self):
    """
    Description:
    ------------
    """
    return self._config_get()

  @tension.setter
  def tension(self, num: int):
    self._config(num)


class OptionInteractionLine(Options):

  @property
  def intersect(self):
    """
    Description:
    ------------

    https://www.chartjs.org/docs/latest/samples/line/interpolation.html
    """
    return self._config_get(False)

  @intersect.setter
  def intersect(self, flag: bool):
    self._config(flag)


class OptionElements(Options):

  @property
  def point(self) -> OptionPoint:
    """
    Description:
    ------------

    :rtype: OptionPoint
    """
    return self._config_sub_data("point", OptionPoint)


class OptionElementsLine(OptionElements):

  @property
  def line(self) -> OptionLine:
    """
    Description:
    ------------

    :rtype: OptionLine
    """
    return self._config_sub_data("line", OptionLine)


class OptionChartJsSize(Options):

  @property
  def height(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @height.setter
  def height(self, val: int):
    self._config(val)

  @property
  def width(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @width.setter
  def width(self, val: int):
    self._config(val)


class OptionChartAreaBorder(Options):

  @property
  def borderColor(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/chart-area-border.html
    """
    return self._config_get()

  @borderColor.setter
  def borderColor(self, text: str):
    self._config(text)

  @property
  def borderWidth(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/chart-area-border.html
    """
    return self._config_get()

  @borderWidth.setter
  def borderWidth(self, num: int):
    self._config(num)

  @property
  def borderDash(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/chart-area-border.html
    """
    return self._config_get()

  @borderDash.setter
  def borderDash(self, values: List[int]):
    self._config(values)

  @property
  def borderDashOffset(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/chart-area-border.html
    """
    return self._config_get()

  @borderDashOffset.setter
  def borderDashOffset(self, num: int):
    self._config(num)


class OptionQuadrants(Options):

  @property
  def topLeft(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/quadrants.html
    """
    return self._config_get()

  @topLeft.setter
  def topLeft(self, text: str):
    self._config(text)

  @property
  def topRight(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/quadrants.html
    """
    return self._config_get()

  @topRight.setter
  def topRight(self, text: str):
    self._config(text)

  @property
  def bottomRight(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/quadrants.html
    """
    return self._config_get()

  @bottomRight.setter
  def bottomRight(self, text: str):
    self._config(text)

  @property
  def bottomLeft(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/samples/plugins/quadrants.html
    """
    return self._config_get()

  @bottomLeft.setter
  def bottomLeft(self, text: str):
    self._config(text)


class OptionChartJsPlugins(Options):

  @property
  @packageImport('chartjs-plugin-labels')
  def labels(self):
    """
    Description:
    -----------
    Chart.js plugin to display labels on pie, doughnut and polar area chart. Original Chart.PieceLabel.js

    Related Pages:

      https://github.com/emn178/chartjs-plugin-labels

    :rtype: ChartJsLabels.Labels
    """
    from epyk.core.html.graph.exts import ChartJsLabels
    return self._config_sub_data("labels", ChartJsLabels.Labels)

  @property
  def legend(self):
    """
    Description:
    ------------

    :rtype: OptionLegend
    """
    return self._config_sub_data("legend", OptionLegend)

  @property
  def title(self):
    """
    Description:
    ------------

    :rtype: OptionTitle
    """
    return self._config_sub_data("title", OptionTitle)

  @property
  def subtitle(self):
    """
    Description:
    ------------

    https://www.chartjs.org/docs/latest/samples/subtitle/basic.html

    :rtype: OptionTitle
    """
    return self._config_sub_data("subtitle", OptionTitle)

  @property
  def quadrants(self) -> OptionQuadrants:
    return self._config_sub_data("quadrants", OptionQuadrants)

  @property
  @packageImport('chartjs-plugin-datalabels')
  def datalabels(self):
    """
    Description:
    -----------
    Display labels on data for any type of charts.

    Related Pages:

      https://chartjs-plugin-datalabels.netlify.app/

    :rtype: ChartJsLabels.Datalabels
    """
    from epyk.core.html.graph.exts import ChartJsDataLabels
    return self._config_sub_data("datalabels", ChartJsDataLabels.Datalabels)

  @property
  @packageImport('chartjs-plugin-zoom')
  def zoom(self):
    """
    Description:
    -----------
    A zoom and pan plugin for Chart.js. Currently requires Chart.js >= 2.6.0

    Related Pages:

      https://github.com/chartjs/chartjs-plugin-zoom

    :rtype: ChartJsZoom.Zoom
    """
    from epyk.core.html.graph.exts import ChartJsZoom
    return self._config_sub_data("zoom", ChartJsZoom.Zoom)

  @property
  @packageImport('chartjs-plugin-crosshair')
  def crosshair(self):
    """
    Description:
    -----------

    Related Pages:

      https://github.com/chartjs/chartjs-plugin-zoom

    :rtype: ChartJsCrosshair.Crosshair
    """
    from epyk.core.html.graph.exts import ChartJsCrosshair
    return self._config_sub_data("crosshair", ChartJsCrosshair.Crosshair)

  @property
  @packageImport('chartjs-plugin-annotation')
  def annotation(self):
    """
    Description:
    -----------
    An annotation plugin for Chart.js >= 2.4.0

    This plugin draws lines and boxes on the chart area.

    Annotations work with line, bar, scatter and bubble charts that use linear, logarithmic, time, or category scales.
    Annotations will not work on any chart that does not have exactly two axes, including pie, radar,
    and polar area charts.

    Related Pages:

      https://github.com/chartjs/chartjs-plugin-zoom

    :rtype: ChartJsAnnotation.Annotation
    """
    from epyk.core.html.graph.exts import ChartJsAnnotation
    return self._config_sub_data("annotation", ChartJsAnnotation.Annotation)

  @property
  def chartAreaBorder(self) -> OptionChartAreaBorder:
    return self._config_sub_data("chartAreaBorder", OptionChartAreaBorder)


class ChartJsOptions(OptChart.OptionsChart):

  @property
  def data(self):
    return self.component._data_attrs

  @data.setter
  def data(self, values: dict):
    self.component._data_attrs = values
    for d in values.get("datasets", []):
      self.component.add_dataset(**d)

  @property
  def indexAxis(self):
    return self._config_get()

  @indexAxis.setter
  @JsUtils.fromVersion({"chart.js": "3.0.0"})
  def indexAxis(self, flag: bool):
    self._config(flag)

  @property
  def responsive(self):
    return self._config_get()

  @responsive.setter
  def responsive(self, flag: bool):
    self._config(flag)

  @property
  def maintainAspectRatio(self):
    return self._config_get(True)

  @maintainAspectRatio.setter
  def maintainAspectRatio(self, flag: bool):
    self._config(flag)

  @property
  def elements(self) -> OptionElements:
    """
    Description:
    ------------

    :rtype: OptionElements
    """
    return self._config_sub_data("elements", OptionElements)

  @property
  def scales(self) -> OptionScales:
    """
    Description:
    ------------

    :rtype: OptionScales
    """
    return self._config_sub_data("scales", OptionScales)

  @property
  def layout(self) -> OptionLayout:
    """
    Description:
    ------------

    :rtype: OptionLayout
    """
    return self._config_sub_data("layout", OptionLayout)

  @property
  def title(self) -> OptionTitle:
    """
    Description:
    ------------

    :rtype: OptionTitle
    """
    return self._config_sub_data("title", OptionTitle)

  @property
  def legend(self) -> OptionLegend:
    """
    Description:
    ------------

    :rtype: OptionLegend
    """
    return self._config_sub_data("legend", OptionLegend)

  @property
  def plugins(self) -> OptionChartJsPlugins:
    """
    Description:
    ------------

    :rtype: OptionChartJsPlugins
    """
    return self._config_sub_data("plugins", OptionChartJsPlugins)

  @property
  def tooltips(self):
    """
    Description:
    ------------

    :rtype: OptionChartJsTooltips
    """
    return self._config_sub_data("tooltips", OptionChartJsTooltips)

  def add_title(self, text: str, color: str = None):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param text:
    :param color:
    """
    self.title.display = True
    self.title.text = text
    if color is not None:
      self.title.fontColor = color
    return self

  @property
  def size(self) -> OptionChartJsSize:
    """
    Description:
    -----------

    :rtype: OptionChartJsSize
    """
    return self._config_sub_data("size", OptionChartJsSize)


class OptionPieAnimation(Options):

  @property
  def animateRotate(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @animateRotate.setter
  def animateRotate(self, val):
    self._config(val)

  @property
  def animateScale(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @animateScale.setter
  def animateScale(self, val):
    self._config(val)


class OptionsBar(ChartJsOptions):

  @property
  def stacked(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/samples/latest/charts/bar/stacked.html
    """
    x_stacked = self.scales.x_axes().stacked
    y_stacked = self.scales.y_axis().stacked
    return x_stacked, y_stacked

  @stacked.setter
  def stacked(self, val: bool):
    self.scales.x_axes().stacked = val
    self.scales.y_axis().stacked = val


class OptionsPie(ChartJsOptions):

  @property
  def tooltips(self):
    """
    Description:
    ------------

    :rtype: OptionChartJsPieTooltips
    """
    return self._config_sub_data("tooltips", OptionChartJsPieTooltips)

  @property
  def cutoutPercentage(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @cutoutPercentage.setter
  def cutoutPercentage(self, val):
    self._config(val)

  @property
  def rotation(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @rotation.setter
  def rotation(self, val: int):
    self._config(val)

  @property
  def circumference(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/line.html
    """
    return self._config_get()

  @circumference.setter
  def circumference(self, val: int):
    self._config(val)

  @property
  def animation(self) -> OptionPieAnimation:
    """
    Description:
    ------------

    :rtype: OptionPieAnimation
    """
    return self._config_sub_data("animation", OptionPieAnimation)


class OptionsLine(ChartJsOptions):

  @property
  def showLines(self):
    """
    Description:
    ------------
    If false, the line is not drawn for this dataset.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/polar.html
      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @showLines.setter
  def showLines(self, flag: bool):
    self._config(flag)

  @property
  def spanGaps(self):
    """
    Description:
    ------------
    If true, lines will be drawn between points with no or null data.
    If false, points with null data will create a break in the line. Can also be a number specifying the maximum gap
    length to span. The unit of the value depends on the scale used.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/polar.html
      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @spanGaps.setter
  def spanGaps(self, val: Optional[bool]):
    self._config(val)

  @property
  def tension(self):
    """
    Description:
    ------------
    Bezier curve tension of the line.
    Set to 0 to draw straightlines. This option is ignored if monotone cubic interpolation is used.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @tension.setter
  def tension(self, val: int):
    self._config(val)

  @property
  def backgroundColor(self):
    """
    Description:
    ------------
    The line fill color.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @backgroundColor.setter
  def backgroundColor(self, val):
    self._config(val)

  @property
  def borderCapStyle(self):
    """
    Description:
    ------------
    Cap style of the line.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @borderCapStyle.setter
  def borderCapStyle(self, val):
    self._config(val)

  @property
  def borderColor(self):
    """
    Description:
    ------------
    The line color.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @borderColor.setter
  def borderColor(self, val: int):
    self._config(val)

  @property
  def borderDash(self):
    """
    Description:
    ------------
    Length and spacing of dashes.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @borderDash.setter
  def borderDash(self, val: int):
    self._config(val)

  @property
  def borderDashOffset(self):
    """
    Description:
    ------------
    Offset for line dashes.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @borderDashOffset.setter
  def borderDashOffset(self, val: int):
    self._config(val)

  @property
  def borderJoinStyle(self):
    """
    Description:
    ------------
    Line joint style.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @borderJoinStyle.setter
  def borderJoinStyle(self, val: str):
    self._config(val)

  @property
  def borderWidth(self):
    """
    Description:
    ------------
    The line width (in pixels).

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @borderWidth.setter
  def borderWidth(self, val: int):
    self._config(val)

  @property
  def interaction(self):
    """
    Description:
    ------------

    :rtype: OptionInteractionLine
    """
    return self._config_sub_data("interaction", OptionInteractionLine)

  @property
  def fill(self):
    """
    Description:
    ------------
    How to fill the area under the line.

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/charts/line.html
    """
    return self._config_get()

  @fill.setter
  def fill(self, val):
    self._config(val)

  @property
  def elements(self):
    """
    Description:
    ------------

    :rtype: OptionElementsLine
    """
    return self._config_sub_data("elements", OptionElementsLine)


class OptionsPolar(ChartJsOptions):

  @property
  def startAngle(self):
    """
    Description:
    ------------
    Starting angle to draw arcs for the first item in a dataset. In degrees, 0 is at top.

    Related Pages:

      https://www.chartjs.org/docs/latest/charts/polar.html
      https://www.chartjs.org/docs/3.7.0/api/interfaces/PolarAreaControllerChartOptions.html
    """
    return self._config_get(0)

  @startAngle.setter
  def startAngle(self, val: int):
    self._config(val)

  @property
  def animation(self) -> OptionPieAnimation:
    """
    Description:
    ------------

    :rtype: OptionPieAnimation
    """
    return self._config_sub_data("animation", OptionPieAnimation)


class OptionChartJsTooltipsCallbacks(Options):

  @property
  def label(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @label.setter
  def label(self, val: str):
    self._config("function(tooltipItem, data) { return '%s' }" % val, js_type=True)

  @packageImport("accounting")
  def labelNumber(self, digit=0, thousand_sep=".", decimal_sep=","):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param digit: String. Optional. Decimal point separator.
    :param thousand_sep: String. Optional. thousands separator.
    :param decimal_sep: String. Optional. Decimal point separator.
    """
    thousand_sep = JsUtils.jsConvertData(thousand_sep, None)
    decimal_sep = JsUtils.jsConvertData(decimal_sep, None)
    if self.component.options.type == 'horizontalBar':
      self._config("function(tooltipItem, data) {return data.datasets[tooltipItem.datasetIndex].label +': '+ accounting.formatNumber(tooltipItem.xLabel, %s, %s, %s) }" % (digit, thousand_sep, decimal_sep), name="label", js_type=True)
    else:
      self._config("function(tooltipItem, data) {return data.datasets[tooltipItem.datasetIndex].label +': '+ accounting.formatNumber(tooltipItem.yLabel, %s, %s, %s) }" % (digit, thousand_sep, decimal_sep), name="label", js_type=True)

  @packageImport("accounting")
  def labelCurrency(self, symbol="", digit=0, thousand_sep=".", decimal_sep=","):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param symbol: String. Optional. Default currency symbol is ''.
    :param digit: String. Optional. Decimal point separator.
    :param thousand_sep: String. Optional. thousands separator.
    :param decimal_sep: String. Optional. Decimal point separator.
    """
    symbol = JsUtils.jsConvertData(symbol, None)
    thousand_sep = JsUtils.jsConvertData(thousand_sep, None)
    decimal_sep = JsUtils.jsConvertData(decimal_sep, None)
    if self.component.options.type == 'horizontalBar':
      self._config("function(tooltipItem, data) { return data.datasets[tooltipItem.datasetIndex].label +': '+ accounting.formatMoney(tooltipItem.xLabel, %s, %s, %s, %s) }" % (symbol, digit, thousand_sep, decimal_sep), name="label", js_type=True)
    else:
      self._config(
        "function(tooltipItem, data) { return data.datasets[tooltipItem.datasetIndex].label +': '+ accounting.formatMoney(tooltipItem.yLabel, %s, %s, %s, %s) }" % (
        symbol, digit, thousand_sep, decimal_sep), name="label", js_type=True)

  @property
  def value(self):
    """
    Description:
    ------------

    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @value.setter
  def value(self, val):
    self._config(val)


class OptionChartJsTooltipsPieCallbacks(OptionChartJsTooltipsCallbacks):

  @packageImport("accounting")
  def labelNumber(self, digit=0, thousand_sep="."):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param digit: String. Optional. Decimal point separator
    :param thousand_sep: String. Optional. thousands separator
    """
    self._config(
        "function(tooltipItem, data) { var indice = tooltipItem.index; return data.labels[indice] +': '+ accounting.formatNumber(data.datasets[0].data[indice], %s, '%s') }" % (
        digit, thousand_sep), name="label", js_type=True)

  @packageImport("accounting")
  def labelCurrency(self, symbol="", digit=0, thousand_sep=".", decimal_sep=","):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param symbol: String. Optional. Default currency symbol is ''
    :param digit: String. Optional. Decimal point separator
    :param thousand_sep: String. Optional. thousands separator
    :param decimal_sep: String. Optional. Decimal point separator
    """
    symbol = JsUtils.jsConvertData(symbol, None)
    thousand_sep = JsUtils.jsConvertData(thousand_sep, None)
    decimal_sep = JsUtils.jsConvertData(decimal_sep, None)
    self._config(
        "function(tooltipItem, data) {var indice = tooltipItem.index; return data.labels[indice] +': '+ accounting.formatMoney(data.datasets[0].data[indice], %s, %s, %s, %s) }" % (
        symbol, digit, thousand_sep, decimal_sep), name="label", js_type=True)


class OptionChartJsTooltips(Options):

  @property
  def enabled(self):
    """

    https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @enabled.setter
  def enabled(self, flag: bool):
    self._config(flag)

  @property
  def mode(self):
    return self._config_get()

  @mode.setter
  def mode(self, value):
    self._config(value)

  @property
  def intersect(self):
    return self._config_get()

  @intersect.setter
  def intersect(self, flag: bool):
    self._config(flag)

  @property
  def position(self):
    """

    https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @position.setter
  def position(self, text: str):
    self._config(text)

  @property
  def callbacks(self):
    """
    Description:
    ------------

    :rtype: OptionChartJsTooltipsCallbacks
    """
    return self._config_sub_data("callbacks", OptionChartJsTooltipsCallbacks)

  def itemSort(self):
    ...

  def filter(self):
    ...

  @property
  def backgroundColor(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @backgroundColor.setter
  def backgroundColor(self, code: str):
    self._config(code)

  @property
  def titleColor(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('#fff')

  @titleColor.setter
  def titleColor(self, code: str):
    self._config(code)

  @property
  def titleAlign(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('left')

  @titleAlign.setter
  def titleAlign(self, text: str):
    self._config(text)

  @property
  def titleSpacing(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(2)

  @titleSpacing.setter
  def titleSpacing(self, num: float):
    self._config(num)

  @property
  def titleMarginBottom(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(6)

  @titleMarginBottom.setter
  def titleMarginBottom(self, num: float):
    self._config(num)

  @property
  def bodyColor(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('#fff')

  @bodyColor.setter
  def bodyColor(self, code: str):
    self._config(code)

  @property
  def bodyAlign(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('left')

  @bodyAlign.setter
  def bodyAlign(self, text: str):
    self._config(text)

  @property
  def bodySpacing(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(2)

  @bodySpacing.setter
  def bodySpacing(self, num: float):
    self._config(num)

  @property
  def footerColor(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('#fff')

  @footerColor.setter
  def footerColor(self, code: str):
    self._config(code)

  @property
  def footerAlign(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('left')

  @footerAlign.setter
  def footerAlign(self, text: str):
    self._config(text)

  @property
  def footerSpacing(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(2)

  @footerSpacing.setter
  def footerSpacing(self, num: float):
    self._config(num)

  @property
  def footerMarginTop(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(6)

  @footerMarginTop.setter
  def footerMarginTop(self, num: float):
    self._config(num)

  @property
  def caretPadding(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(2)

  @caretPadding.setter
  def caretPadding(self, num: float):
    self._config(num)

  @property
  def caretSize(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(5)

  @caretSize.setter
  def caretSize(self, num: float):
    self._config(num)

  @property
  def cornerRadius(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(6)

  @cornerRadius.setter
  def cornerRadius(self, num: float):
    self._config(num)

  @property
  def multiKeyBackground(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('#fff')

  @multiKeyBackground.setter
  def multiKeyBackground(self, code: str):
    self._config(code)

  @property
  def displayColors(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(True)

  @displayColors.setter
  def displayColors(self, flag: bool):
    self._config(flag)

  @property
  def boxWidth(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @boxWidth.setter
  def boxWidth(self, num: float):
    self._config(num)

  @property
  def boxHeight(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @boxHeight.setter
  def boxHeight(self, num: float):
    self._config(num)

  @property
  def boxPadding(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(1)

  @boxPadding.setter
  def boxPadding(self, num: float):
    self._config(num)

  @property
  def usePointStyle(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(False)

  @usePointStyle.setter
  def usePointStyle(self, flag: bool):
    self._config(flag)

  @property
  def borderColor(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get('rgba(0, 0, 0, 0)')

  @borderColor.setter
  def borderColor(self, code: str):
    self._config(code)

  @property
  def borderWidth(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(0)

  @borderWidth.setter
  def borderWidth(self, num: float):
    self._config(num)

  @property
  def rtl(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @rtl.setter
  def rtl(self, flag: bool):
    self._config(flag)

  @property
  def textDirection(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get()

  @textDirection.setter
  def textDirection(self, text: str):
    self._config(text)

  @property
  def xAlign(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(None)

  @xAlign.setter
  def xAlign(self, text: str):
    self._config(text)

  @property
  def yAlign(self):
    """
    Description:
    ------------


    Related Pages:

      https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html
    """
    return self._config_get(None)

  @yAlign.setter
  def yAlign(self, text: str):
    self._config(text)


class OptionChartJsPieTooltips(Options):

  @property
  def callbacks(self):
    """
    Description:
    ------------

    :rtype: OptionChartJsTooltipsPieCallbacks
    """
    return self._config_sub_data("callbacks", OptionChartJsTooltipsPieCallbacks)


class OptionGeoColorScale(Options):

  @property
  def display(self):
    return self._config_get()

  @display.setter
  def display(self, val):
    self._config(val)

  @property
  def quantize(self):
    return self._config_get()

  @quantize.setter
  def quantize(self, val):
    self._config(val)

  @property
  def position(self):
    return self._config_get()

  @position.setter
  def position(self, val: str):
    self._config(val)

  @property
  def legend(self):
    """
    Description:
    ------------

    :rtype: OptionLegend
    """
    return self._config_sub_data("legend", OptionLegend)


class OptionGeoRadiusScale(Options):

  @property
  def display(self):
    return self._config_get()

  @display.setter
  def display(self, val):
    self._config(val)

  @property
  def size(self):
    return self._config_get()

  @size.setter
  def size(self, val):
    self._config(val)


class OptionGeo(Options):

  @property
  def colorScale(self):
    """
    Description:
    ------------

    :rtype: OptionGeoColorScale
    """
    return self._config_sub_data("colorScale", OptionGeoColorScale)

  @property
  def radiusScale(self):
    """
    Description:
    ------------

    :rtype: OptionGeoRadiusScale
    """
    return self._config_sub_data("radiusScale", OptionGeoRadiusScale)


class OptionPlugins(Options):

  @property
  def legend(self) -> OptionLegend:
    """
    Description:
    ------------

    :rtype: OptionLegend
    """
    return self._config_sub_data("legend", OptionLegend)


class OptionsGeo(ChartJsOptions):

  @property
  def showOutline(self):
    return self._config_get()

  @showOutline.setter
  def showOutline(self, val):
    self._config(val)

  @property
  def showGraticule(self):
    return self._config_get()

  @showGraticule.setter
  def showGraticule(self, val):
    self._config(val)

  @property
  def scale(self):
    """
    Description:
    ------------

    :rtype: OptionScaleGeo
    """
    return self._config_sub_data("scale", OptionScaleGeo)

  @property
  def scales(self):
    """
    Description:
    ------------

    :rtype: OptionScalesGeo
    """
    return self._config_sub_data("scales", OptionScalesGeo)

  @property
  def geo(self):
    """
    Description:
    ------------

    :rtype: OptionGeo
    """
    return self._config_sub_data("geo", OptionGeo)

  @property
  def plugins(self) -> OptionPlugins:
    """
    Description:
    ------------

    :rtype: OptionPlugins
    """
    return self._config_sub_data("plugins", OptionPlugins)


class OptionsTreeMap(ChartJsOptions):
  ...
