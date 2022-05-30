#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Union, Optional
from epyk.core.py import primitives
from epyk.core.js import JsUtils
from epyk.core.js.packages import JsPackage


class LTooltip:

  def __init__(self, latlng=None, options=None, selector=None):
    self._selector = selector
    self._js, self.__is_attached = [], False
    self.varId = "L.marker(%s)" % latlng

  def openTooltip(self, latlng=None, options=None):
    """
    Description:
    -----------
    Opens the specified tooltip.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#map-opentooltip
    """
    if latlng is not None:
      self.varId = "L.marker(%s)" % latlng
    self._js.append("openTooltip()")
    return self

  def unbindTooltip(self):
    """
    Description:
    -----------
    Removes the tooltip previously bound with bindTooltip.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#layer-unbindtooltip
    """
    self._js.append("unbindTooltip()")
    return self

  def closeTooltip(self):
    """
    Description:
    -----------
    Closes the tooltip given as parameter.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#map-closetooltip
    """
    self._js.append("closeTooltip()")
    return self

  def toStr(self):
    js_fnc = ".".join(self._js)
    self._js = []
    return "%s.%s" % (self.varId, js_fnc)


class Layer:
  pass


class LMarker:

  def __init__(self, latlng, options=None, leaflet_map=None):
    self.leaflet_map, self.latlng = leaflet_map, latlng
    self._js, self.__is_attached, self.options = [], False, options or {}
    self.varId = "L.marker"

  def addTo(self, selector=None):
    """
    Description:
    -----------
    Add the marker to the defined map.

    Attributes:
    ----------
    :param selector: String. Optional. The map reference variable.
    """
    self._js.append("addTo(%s)" % selector)
    self.__is_attached = True
    return self

  def bindPopup(self, content):
    """
    Description:
    -----------
    Binds a popup to all of the layers at once.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#marker

    Attributes:
    ----------
    :param content: String. The market content.
    """
    self._js.append("bindPopup(%s)" % JsUtils.jsConvertData(content, None))
    popup = LPopup()
    popup.varId = self.toStr()
    return popup

  def bindTooltip(self, content):
    """
    Description:
    -----------
    Binds a tooltip to the layer with the passed content and sets up the necessary event listeners.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#layer-bindtooltip

    Attributes:
    ----------
    :param content: String. The tooltip content.
    """
    self._js.append("bindTooltip(%s)" % JsUtils.jsConvertData(content, None))
    tooltip = LTooltip()
    tooltip.varId = self.toStr()
    return tooltip

  def setLatLng(self, latlng):
    """
    Description:
    -----------
    Changes the marker position to the given point.

    https://leafletjs.com/reference-1.7.1.html#marker-setlatlng

    Attributes:
    ----------
    :param latlng:
    """
    self._js.append("setLatLng(%s)" % latlng)
    return self

  def setIcon(self, icon):
    """
    Description:
    -----------
    Changes the marker icon.

    https://leafletjs.com/reference-1.7.1.html#marker-seticon

    Attributes:
    ----------
    :param icon:
    """
    self._js.append("setIcon(%s)" % icon)
    return self

  def setOpacity(self, opacity):
    """
    Description:
    -----------
    Changes the opacity of the marker.

    https://leafletjs.com/reference-1.7.1.html#marker-setopacity

    Attributes:
    ----------
    :param opacity:
    """
    self._js.append("setOpacity(%s)" % opacity)
    return self

  def setZIndexOffset(self, offset):
    """
    Description:
    -----------
    Changes the zIndex offset of the marker.

    https://leafletjs.com/reference-1.7.1.html#marker-setzindexoffset

    Attributes:
    ----------
    :param offset:
    """
    self._js.append("setZIndexOffset(%s)" % offset)
    return self

  def toStr(self):
    if not self.__is_attached and self.leaflet_map is not None:
      self.addTo(self.leaflet_map.varName)
    js_fnc = ".".join(self._js)
    self._js = []
    return "%s(%s, %s).%s" % (self.varId, self.latlng, JsUtils.jsConvertData(self.options, None), js_fnc)


class LCircle(LMarker):

  def __init__(self, latlng, options=None, shape="circle", leaflet_map=None):
    super(LCircle, self).__init__(latlng, options, leaflet_map)
    self.varId = "L.%s" % shape

  def radius(self, num):
    """
    Radius of the circle, in meters.

    https://leafletjs.com/reference-1.7.1.html#circle-radius

    :param num:
    """
    self.options["radius"] = num
    return self

  def color(self, hexcode):
    """
    Color of the circle.

    https://leafletjs.com/reference-1.7.1.html#path

    :param hexcode:
    """
    self.options["color"] = hexcode
    return self

  def fillOpacity(self, num):
    self.options["fillOpacity"] = num
    return self

  def fillColor(self, hexcode):
    self.options["fillColor"] = hexcode
    return self

  def weight(self, num):
    self.options["weight"] = num
    return self


class LPopup:

  def __init__(self, latlng=None, options=None, selector=None):
    self._selector = selector
    self._js, self.__is_attached = [], False
    self.varId = "L.marker(%s)" % latlng

  def openPopup(self, latlng=None):
    """
    Description:
    -----------
    Opens the bound popup at the specified latlng or at the default popup anchor if no latlng is passed.

    https://leafletjs.com/reference-1.7.1.html#layer-openpopup
    """
    if latlng is not None:
      self.setLatLng(latlng)
    self._js.append("openPopup()")
    return self

  def setLatLng(self, latlng):
    """
    Description:
    -----------
    Changes the marker position to the given point.

    https://leafletjs.com/reference-1.7.1.html#marker-setlatlng

    Attributes:
    ----------
    :param latlng:
    """
    self._js.append("setLatLng(%s)" % latlng)
    return self

  def setZIndexOffset(self, offset):
    """
    Description:
    -----------
    Changes the zIndex offset of the marker.

    https://leafletjs.com/reference-1.7.1.html#marker-setzindexoffset

    Attributes:
    ----------
    :param offset:
    """
    self._js.append("setZIndexOffset(%s)" % offset)
    return self

  def setContent(self, content):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param content: String. The popup content.
    """
    self._js.append("setContent(%s)" % JsUtils.jsConvertData(content, None))
    return self

  def openOn(self):
    pass

  def toStr(self):
    if not self._js:
      return self.varId

    js_fnc = ".".join(self._js)
    self._js = []
    return "%s.%s" % (self.varId, js_fnc)


class LtileLayer:

  def __init__(self, component, token, url, options, leaflet_map=None):
    self.component, self.leaflet_map = component, leaflet_map
    self.srv_url = "%s?access_token=%s" % (url, token)
    self.options, self.__is_attached, self._js = options or {}, False, []

  def attribution(self, text):
    """
    The attribution control allows you to display attribution data in a small text box on a map.

    :param text:
    """
    self.options["attribution"] = text
    return self

  def maxBounds(self, latLngBounds):
    """
    When this option is set, the map restricts the view to the given geographical bounds, bouncing the user back if the user tries to pan outside the view.
    To set the restriction dynamically, use setMaxBounds method.

    https://leafletjs.com/reference-1.7.1.html#map-maxbounds

    :param latLngBounds:
    """
    self.options["maxBounds"] = latLngBounds
    return self

  def maxZoom(self, num):
    """
    Maximum zoom level of the map.
    If not specified and at least one GridLayer or TileLayer is in the map, the highest of their maxZoom options will be used instead.

    https://leafletjs.com/reference-1.7.1.html#map-maxzoom

    :param num:
    """
    self.options["maxZoom"] = num
    return self

  def minZoom(self, num):
    """
    Minimum zoom level of the map. If not specified and at least one GridLayer or TileLayer is in the map, the lowest of their minZoom options will be used instead.

    https://leafletjs.com/reference-1.7.1.html#map-minzoom

    :param num:
    """
    self.options["minZoom"] = num
    return self

  def id(self, value):
    self.options["id"] = value
    return self

  def tileSize(self, num):
    """
    Width and height of tiles in the grid. Use a number if width and height are equal, or L.point(width, height) otherwise.

    https://leafletjs.com/reference-1.7.1.html#gridlayer-tilesize

    :param num:
    """
    self.options["tileSize"] = num
    return self

  def zoomOffset(self, num):
    """
    The zoom number used in tile URLs will be offset with this value.

    https://leafletjs.com/reference-1.7.1.html#tilelayer-zoomoffset

    :param num:
    :return:
    """
    self.options["zoomOffset"] = num
    return self

  def accessToken(self, token):
    self.srv_url = "%s?access_token=%s" % (self.srv_url.split("?")[0], token)
    return self

  def addTo(self, map):
    self.__is_attached = True
    self._js.append("addTo(%s)" % map)
    return self

  def toStr(self):
    if not self.__is_attached and self.leaflet_map is not None:
      self.addTo(self.leaflet_map.varName)
    js_fnc = ".".join(self._js)
    self._js = []
    return "L.tileLayer(%s, %s).%s" % (
      JsUtils.jsConvertData(self.srv_url, None), JsUtils.jsConvertData(self.options, None), js_fnc)


class LMapAttributionControl:

  def __init__(self, varId=None):
    self._js = []
    self.varId = varId

  def addAttribution(self, text):
    """
    The attribution control allows you to display attribution data in a small text box on a map.


    :param text:
    """
    return "%s.addAttribution(%s)" % (self.varId, JsUtils.jsConvertData(text, None))


class LMap:

  def __init__(self, component: primitives.HtmlModel = None, set_var: bool = None):
    self.component = component
    self._js, self.set_var = [], set_var
    self.varId = "L.map(%s)" % JsUtils.jsConvertData(component.htmlCode, None)

  @property
  def varName(self):
    return self.varId or self.set_var or "window['%s']" % self.component.chartId

  def setView(self, LatLng, zoom=None):
    """
    Description:
    -----------
    Sets the view of the map (geographical center and zoom) with the given animation options.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#map-example

    Attributes:
    ----------
    :param LatLng: List.
    :param zoom: Integer. Optional.
    """
    if zoom is not None:
      self._js.append("setView(%s, %s)" % (LatLng, zoom))
    else:
      self._js.append("setView(%s)" % LatLng)
    return self

  def on(self, typeEvent, js_funcs: Union[list, str], profile: Optional[Union[dict, bool]] = None):
    """

    :param typeEvent:
    :param js_funcs:
    :param profile:
    """
    return JsUtils.jsWrap("%s; %s.on('%s', function(event){%s})" % (
      self.toStr(), self.varName, typeEvent, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))

  def locationfound(self, js_funcs: Union[list, str], profile: Optional[Union[dict, bool]] = None):
    """
    Fired when geolocation (using the locate method) went successfully.

    https://leafletjs.com/reference-1.7.1.html#map-locationfound
    https://leafletjs.com/examples/mobile/

    :param js_funcs:
    :param profile:
    """
    return self.on("locationfound", js_funcs, profile)

  def locationerror(self, js_funcs: Union[list, str], profile: Optional[Union[dict, bool]] = None):
    """
    Fired when geolocation (using the locate method) failed.

    https://leafletjs.com/examples/mobile/
    https://leafletjs.com/reference-1.7.1.html#map-locationerror

    :param js_funcs:
    :param profile:
    """
    return self.on("locationerror", js_funcs, profile)

  def createPane(self, text):
    """
    Stops watching location previously initiated by map.locate({watch: true}) and aborts resetting the map view
    if map.locate was called with {setView: true}.

    https://leafletjs.com/reference-1.7.1.html#map-createpane

    :param text:
    """
    return JsUtils.jsWrap("%s; %s.createPane(%s)" % (self.toStr(), self.varName, JsUtils.jsConvertData(text, None)))

  def remove(self):
    """
    Destroys the map and clears all related event listeners.

    https://leafletjs.com/reference-1.7.1.html#map-remove
    """
    return JsUtils.jsWrap("%s; %s.remove()" % (self.toStr(), self.varName))

  def fitBounds(self):
    pass

  def whenReady(self):
    pass

  @property
  def attributionControl(self):
    return LMapAttributionControl("%s.attributionControl" % self.toStr())

  def fitWorld(self):
    self._js.append("fitWorld()")
    return self

  def locate(self, options=None):
    """
    Tries to locate the user using the Geolocation API, firing a locationfound event with location data on success or a
    locationerror event on failure, and optionally sets the map view to the user's location with respect to detection accuracy

    https://leafletjs.com/reference-1.7.1.html#map-locate

    :param options:
    """
    options = options or {"setView": True, "maxZoom": 16}
    self._js.append("locate(%s)" % JsUtils.jsConvertData(options, None))
    return self

  def stopLocate(self):
    """
    Stops watching location previously initiated by map.locate({watch: true}) and aborts resetting the map view
    if map.locate was called with {setView: true}.

    https://leafletjs.com/reference-1.7.1.html#map-stoplocate
    """
    self._js.append("stopLocate()")
    return self

  def toStr(self):
    if not self._js:
      return self.varName

    js_fnc = ".".join(self._js)
    self._js = []
    if self.set_var is not None:
      expr = "%s = %s.%s" % (self.set_var, self.varId, js_fnc)
      self.set_var = None
      self.varId = self.set_var
      return expr

    return "%s.%s" % (self.varId, js_fnc)


class LGeoJSON(LMarker):

  def __init__(self, shapes, options=None, leaflet_map=None):
    super(LGeoJSON, self).__init__(JsUtils.jsConvertData(shapes, None), options, leaflet_map)
    self.varId = "L.geoJSON"


class LControl:

  def __init__(self, component=None, options=None, set_var=None):
    self.component = component
    self._js, self.set_var = [], set_var
    self.varId, self.varName = "L.control()" if options is None else "L.control(%s)" % JsUtils.jsConvertData(options, None), None

  def onAdd(self, js_funcs: Union[list, str], profile: Optional[Union[dict, bool]] = None):
    pass

  def update(self, js_funcs: Union[list, str], profile: Optional[Union[dict, bool]] = None):
    pass

  def addTo(self):
    pass

  def toStr(self):
    if not self._js:
      return self.varId

    js_fnc = ".".join(self._js)
    self._js = []
    if self.set_var is not None:
      expr = "var %s = %s.%s" % (self.set_var, self.varId, js_fnc)
      self.set_var = None
      self.varId = self.set_var
      return expr

    return "%s.%s" % (self.varId, js_fnc)


class LEventlLatlng:

  @property
  def lat(self):
    """
    Return the latitude.

    """
    return "event.latlng.lat"

  @property
  def lng(self):
    """
    Return the longitude.

    """
    return "event.latlng.lng"

  def toStr(self):
    return "event.latlng"


class LEvent(JsPackage):
  lib_alias = {'js': "leaflet", 'css': 'leaflet'}

  @property
  def latlng(self):
    """
    Get coordinate from an event on a map.
    """
    return LEventlLatlng()


class LeafLet(JsPackage):
  lib_alias = {'js': "leaflet", 'css': 'leaflet'}

  def __init__(self, html_code=None, config=None, component=None, js_code=None, selector=None, set_var=False,
               page=None):
    self.component, self.page = component, page
    if page is None and component is not None:
      self.page = component.page
    self._selector = selector
    self.varName, self.setVar = js_code or self._selector, set_var
    self.component.jsImports.add(self.lib_alias['js'])
    self.component.cssImport.add(self.lib_alias['css'])
    self._js, self._map, self._control = [], None, {}

  @property
  def map(self):
    if self._map is None:
      self._map = LMap(self.component, set_var=self._selector)
    return self._map

  def control(self, alias, options=None):
    """

    :param alias:
    :param options:
    """
    if alias not in self._control:
      self._control[alias] = LControl(self.component, options=options, set_var=self._selector)
    return self._control[alias]

  def setZoom(self, zoom):
    """
    Description:
    -----------
    Sets the zoom of the map.

    hRelated Pages:

      ttps://leafletjs.com/reference-1.7.1.html#map-example

    Attributes:
    ----------
    :param zoom:
    """
    return JsUtils.jsWrap("%s.setZoom(%s)" % (self._selector, zoom))

  def setView(self, LatLng, zoom=None):
    """
    Description:
    -----------
    Sets the view of the map (geographical center and zoom) with the given animation options.

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#map-example

    Attributes:
    ----------
    :param LatLng:
    :param zoom:
    """
    if zoom is not None:
      return JsUtils.jsWrap("%s.setView(%s, %s)" % (self._selector, LatLng, zoom))

    return JsUtils.jsWrap("%s.setView(%s)" % (self._selector, LatLng))

  def zoomIn(self, delta):
    """
    Description:
    -----------
    Increases the zoom of the map by delta (zoomDelta by default).

    Attributes:
    ----------
    :param delta:
    """
    return JsUtils.jsWrap("%s.zoomIn(%s)" % (self._selector, delta))

  def marker(self, latlng, options=None):
    """
    Description:
    -----------

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#marker

    Attributes:
    ----------
    :param latlng:
    :param options:
    """
    return LMarker(latlng, options, leaflet_map=self.map)

  def circle(self, latlng, options=None):
    """

    :param latlng:
    :param options:
    """
    return LCircle(latlng, options, leaflet_map=self.map)

  def tileLayer(self, token, options=None, url="https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}"):
    """

    :param token:
    :param options:
    :param url:
    """
    return LtileLayer(self.component, token, url, options, leaflet_map=self.map)

  def popup(self, options=None, source=None):
    """
    Description:
    -----------

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#popup-l-popup

    Attributes:
    ----------
    :param options:
    :param source:
    """
    pass

  def tooltip(self, options=None, source=None):
    """
    Description:
    -----------

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#tooltip-l-tooltip

    Attributes:
    ----------
    :param options:
    :param source:
    """
    return LTooltip(options, self._selector)

  def imageOverlay(self):
    """
    Description:
    -----------

    Related Pages:

      https://leafletjs.com/reference-1.7.1.html#imageoverlay-l-imageoverlay

    """
    pass

  def videoOverlay (self):
    pass

  def svgOverlay(self):
    pass

  def polyline(self, latlng1, latlng2, options=None):
    """

    :param latlng1:
    :param latlng2:
    :param options:
    """
    return LCircle([latlng1, latlng2], options, shape="polyline", leaflet_map=self.map)

  def polygon(self, latlng1, latlng2, options=None):
    """

    :param latlng1:
    :param latlng2:
    :param options:
    """
    return LCircle([latlng1, latlng2], options, shape="polygon", leaflet_map=self.map)

  def rectangle(self, latlng1, latlng2, options=None):
    """

    :param latlng1:
    :param latlng2:
    :param options:
    """
    return LCircle([latlng1, latlng2], options, shape="rectangle", leaflet_map=self.map)

  def circleMarker(self):
    pass

  def layerGroup(self):
    pass

  def featureGroup(self):
    pass

  def geoJSON(self, shapes, options=None):
    """

    https://leafletjs.com/examples/geojson/

    """
    return LGeoJSON(shapes, options, leaflet_map=self.map)

  def latLng(self):
    pass
