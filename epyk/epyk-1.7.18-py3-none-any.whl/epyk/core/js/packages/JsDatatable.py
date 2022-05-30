#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.js import JsUtils
from epyk.core.py import primitives

from epyk.core.js.primitives import JsObjects
from epyk.core.js.objects import JsNodeDom
from epyk.core.js.packages import JsQuery
from epyk.core.js.packages import JsPackage


class SelectAPI(JsPackage):

  def blurable(self):
    """
    Description:
    -----------
    Get the blurable state for the table.

    Related Pages:

      https://datatables.net/reference/api/select.blurable()
    """
    return JsObjects.JsBoolean.JsBoolean("%s.blurable()" % self._selector)

  def info(self, flag=None):
    """
    Description:
    -----------
    Get / set the information summary display state.

    Related Pages:

      https://datatables.net/reference/api/select.info()

    Attributes:
    ----------
    :param flag: Value to set for the information summary display state - true to enable, false to disable.
    """
    if flag is None:
      return JsObjects.JsBoolean.JsBoolean("%s.info()" % self._selector)

    return JsObjects.JsObject.JsObject("%s.info(%s)" % (self._selector, JsUtils.jsConvertData(flag, None)))

  def items(self):
    """
    Description:
    -----------
    Get / set the items that Select will select based on user interaction (rows, columns or cells).

    Related Pages:

      https://datatables.net/reference/api/select.items()
    """
    return JsObjects.JsString.JsString("%s.items()" % self._selector)

  def selector(self):
    """
    Description:
    -----------
    Get the current item selector string applied to the table.

    Related Pages:

      https://datatables.net/reference/api/select.selector()
    """
    return JsObjects.JsString.JsString("%s.selector()" % self._selector)

  def style(self):
    """
    Description:
    -----------
    Get / set the style by which the end user can select items in the table.

    Related Pages:

      https://datatables.net/reference/api/select.style()
    """
    return JsObjects.JsString.JsString("%s.style()" % self._selector)


class CellAPI(JsPackage):
  lib_alias = {'js': "datatables", 'css': 'datatables'}
  lib_selector = 'cell'
  lib_set_var = False

  def deselect(self):
    """
    Description:
    -----------
    Deselect a single cell

    Related Pages:

      https://datatables.net/reference/api/column().deselect()

    :return: DataTables API instance for chaining
    """
    return self.fnc("deselect()")

  def select(self):
    """
    Description:
    -----------
    Select a single cell.

    Related Pages:

      https://datatables.net/reference/api/cell().select()

    :return: DataTables API instance for chaining
    """
    return self.fnc("select()")

  def render(self):
    """
    Description:
    -----------
    Get rendered data for a cell.

    Related Pages:

      https://datatables.net/reference/api/cell().render()

    :return: DataTables API instance for chaining
    """
    return self.fnc("render()")

  def node(self):
    """
    Description:
    -----------
    Get the DOM element for the selected cell.

    Related Pages:

      https://datatables.net/reference/api/cell().node()

    :return: DataTables API instance for chaining
    """
    self.fnc("node()")

  def jquery_nodes(self):
    """
    Description:
    -----------
    Get the cell nodes for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().nodes()

    :return:
    """
    self.nodes()
    self._js.append("nodes().to$()")
    return JsQuery.JQuery(jqId=self.toStr())

  def invalidate(self):
    """
    Description:
    -----------
    Invalidate the data held in DataTables for the selected cells.

    Related Pages:

      https://datatables.net/reference/api/cell().invalidate()

    :return: DataTables API instance for chaining.
    """
    return self.fnc("invalidate()")

  def index(self):
    """
    Description:
    -----------
    Get index information about the selected cell.

    Related Pages:

      https://datatables.net/reference/api/cell().index()
    """
    return JsObjects.JsNumber.JsNumber("%s.index()" % self.getStr())

  def cache(self):
    """
    Description:
    -----------
    Get cached data of the cache type specified.

    Related Pages:

      https://datatables.net/reference/api/cell().cache()
    """

  def data(self):
    """
    Description:
    -----------
    Get / set data for the selected cell.

    Related Pages:

      https://datatables.net/reference/api/cell().data()
    """
    return self.fnc("data()")

  def focus(self):
    """
    Description:
    -----------
    Focus on a cell.

    Related Pages:

      https://datatables.net/reference/api/cell().focus()
    """
    return self.fnc("focus()")

  def blur(self):
    """
    Description:
    -----------
    Blur focus from the table.

    Related Pages:

      https://datatables.net/reference/api/cell.blur()
    """
    return self.fnc("blur()")


class ColumnAPI(JsPackage):
  lib_alias = {'js': "datatables", 'css': 'datatables'}
  lib_selector = 'column'
  lib_set_var = False

  def deselect(self):
    """
    Description:
    -----------
    Deselect a single column.

    Related Pages:

      https://datatables.net/reference/api/column().deselect()

    :return: DataTables API instance for chaining
    """
    return self.fnc("deselect()")

  def select(self):
    """
    Description:
    -----------
    Select a single column.

    Related Pages:

      https://datatables.net/reference/api/column().select()

    :return: DataTables API instance for chaining
    """
    self.fnc("select()")

  def cache(self):
    """
    Description:
    -----------
    Get the DataTables cached data for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().cache()

    :return:
    """

  def data(self):
    """
    Description:
    -----------
    Get the data for the cells in the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().data()

    :return:
    """
    return self.fnc("data()")

  def dataSrc(self):
    """
    Description:
    -----------
    Get the data source property for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().dataSrc()
    """

  def footer(self):
    """
    Description:
    -----------
    Get the footer node for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().footer()
    """

  def header(self):
    """
    Description:
    -----------
    Get the header node for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().header()

    :return:
    """

  def index(self):
    """
    Description:
    -----------
    Get the column index of the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().index()
    """
    return JsObjects.JsNumber.JsNumber("%s.index()" % self.getStr())

  def nodes(self):
    """
    Description:
    -----------
    Get the cell nodes for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().nodes()
    """
    self._js.append("nodes()")
    return self

  def jquery_nodes(self):
    """
    Description:
    -----------
    Get the cell nodes for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().nodes()
    """
    self.nodes()
    self._js.append("to$()")
    return JsQuery.JQuery(js_code=self.toStr())

  def order(self):
    """
    Description:
    -----------
    Order the table by the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().order()
    """

  def search(self, data):
    """
    Description:
    -----------
    Search for data in the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().search()
    """
    return self.fnc("search(%s)" % JsUtils.jsConvertData(data, None))

  def visible(self):
    """
    Description:
    -----------
    Get / set the visibility of a single selected column.

    Related Pages:

      https://datatables.net/reference/api/column().visible()

    :return: DataTables API instance for chaining
    """
    return self.fnc("visible()")

  def draw(self, target=None):
    """
    Description:
    -----------
    Redraw the DataTables in the current context, optionally updating ordering, searching and paging as required.

    Related Pages:

      https://datatables.net/reference/api/draw()

    :return: DataTables API instance for chaining
    """
    if target is not None:
      return self.fnc("draw(%s)" % JsUtils.jsConvertData(target, None))

    return self.fnc("draw()")


class RowChildAPI(JsPackage):
  lib_selector = 'child'
  lib_set_var = False

  def remove(self):
    pass

  def show(self):
    pass

  def hide(self):
    """
    Description:
    -----------
    Hide the child row(s) of a parent row.

    Related Pages:

      https://datatables.net/reference/api/row().child.hide()
    """
    return self.fnc("hide()")

  def isShown(self):
    pass


class RowAPI(JsPackage):
  lib_alias = {'js': "datatables", 'css': 'datatables'}
  lib_selector = 'row'
  lib_set_var = False

  def _mapVarId(self, func, js_code):
    """
    Description:
    -----------
    Change the varIs for row.add.
    This is done at class level and not object level on the Javascript side

    This mapping is done according to the Package API definition.

    Related Pages:

      https://datatables.net/reference/api/

    :param func: The function string
    :param js_code: The object reference for the Javascript side

    :return: The object reference on the Javascript side
    """
    if func.startswith("add("):
      return js_code[:-2]

    return js_code

  def deselect(self):
    """
    Description:
    -----------
    This method simply deselects a single row that has been found by the row() selector method.

    Related Pages:

      https://datatables.net/reference/api/row().deselect()

    :return: DataTables API instance for chaining
    """
    return self.fnc("deselect()")

  def select(self):
    """
    Description:
    -----------
    This method simply selects a single row that has been found by the row() selector method.

    Related Pages:

      https://datatables.net/reference/api/row().select()

    :return: DataTables API instance for chaining
    """
    return self.fnc("select()")

  def scrollTo(self, animate=True):
    """
    Description:
    -----------
    Redraw the table's scrolling display to show the row selected by the row() method.

    Related Pages:

      https://datatables.net/reference/api/row().scrollTo()

    :param animate: Animate the scroll (true) or not (false).

    :return: DataTables API instance for chaining
    """
    return self.fnc("scrollTo()")

  def cache(self, dtype):
    """
    Description:
    -----------
    Get the DataTables cached data for the selected row.

    Related Pages:

      https://datatables.net/reference/api/row().cache()

    :param dtype: Specify which cache the data should be read from. Can take one of two values: search or order.
                  Defaults to order if no value is given.

    :return: DataTables API instance for chaining
    """
    if dtype not in ("search", "order"):
      raise ValueError("dtype %s not recognised" % dtype)

    dtype = JsUtils.jsConvertData(dtype, None)
    return self.fnc("scrollTo(%s)" % dtype)

  def data(self):
    """
    Description:
    -----------
    Retrieve the data for the whole table, in row index order.

    Related Pages:

      https://datatables.net/reference/api/row().data()

    :return: DataTables API instance for chaining
    """
    return self.fnc("data()")

  def id(self, hash=True):
    """
    Description:
    -----------
    This method can be used to get a row's id, as specified by the row's data and the rowId option.
    Optionally it can also prepend a hash (#) to the row id allowing it to then easily be used as a selector.

    Related Pages:

      https://datatables.net/reference/api/row().id()

    :param hash: Append a hash (#) to the start of the row id. This can be useful for then using the id as a selector
    """
    hash = JsUtils.jsConvertData(hash, None)
    return self.fnc("id(%s)" % hash)

  def index(self):
    """
    Description:
    -----------
    Get the row index of the selected row.

    Related Pages:

      https://datatables.net/reference/api/row().index()

    :return: Row index
    """
    return JsObjects.JsNumber.JsNumber("%s.index()" % self.getStr())

  def invalidate(self, source=None):
    """
    Description:
    -----------
    Invalidate the data held in DataTables for the selected row.

    Related Pages:

      https://datatables.net/reference/api/row().invalidate()

    :param source:
    """
    return self.fnc("invalidate(%s)")

  def node(self):
    """
    Description:
    -----------
    Get the row TR node for the selected row.

    Related Pages:

      https://datatables.net/reference/api/row().node()
    """
    return self.fnc("node()")

  def jquery_node(self):
    """
    Description:
    -----------
    Get the cell nodes for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().nodes()
    """
    self.node()
    self._js.append("to$()")
    return JsQuery.JQuery(component=self.component, selector=self.toStr(), set_var=False)

  def remove(self, update=False):
    """
    Description:
    -----------
    Delete the selected row from the DataTable.

    Related Pages:

      https://datatables.net/reference/api/row().remove()

    :param update:
    """
    if update:
      self.fnc("remove()")
      return self.draw()

    return self.fnc("remove()")

  def add(self, data, to_array=False, update=False):
    """
    Description:
    -----------
    Add a new row to the table.

    Related Pages:

      https://datatables.net/reference/api/row.add()

    :param data: The input data
    :param to_array: Boolean. Convert a python dictionary to a list
    :param update:
    """
    if to_array:
      if isinstance(data, list):
        rows = []
        for r in data:
          rows.append([r.get(h["title"], '') for h in self.component.vals['columns']])
        data = rows
      else:
        data = [data.get(h["title"], '') for h in self.component.vals['columns']]
    data = JsUtils.jsConvertData(data, None)
    self.fnc("add(%s)" % data)
    if update:
      self.draw()
      self._js.append([])
      return self

    self._js.append([])
    return self

  def draw(self, target=None):
    """
    Description:
    -----------
    Redraw the DataTables in the current context, optionally updating ordering, searching and paging as required.

    Related Pages:

      https://datatables.net/reference/api/draw()
    """
    if target is not None:
      return self.fnc("draw(%s)" % JsUtils.jsConvertData(target, None))

    return self.fnc("draw()")

  def child(self, namespace=True):
    """
    Description:
    -----------
    Row child method.
    Get / set the child rows of the selected main table row.

    Related Pages:

      https://datatables.net/reference/api/row().child

    :param namespace: Boolean to set the level of this method, selected rows or namespace
    """
    if namespace:
      return RowChildAPI(
        component=self.component, selector="%s.child" % self.getStr(), set_var=False, page=self.page)

    return RowChildAPI(
      component=self.component, selector="%s.child()" % self.getStr(), set_var=False, page=self.page)


class DatatableAPI(JsPackage):
  """
  Javascript Interface to the Datatable Module.

  Related Pages:

      https://datatables.net/reference/api/
  """
  lib_alias = {'js': "datatables", 'css': 'datatables'}
  lib_selector = 'datatable'

  def body(self):
    """
    Description:
    -----------
    Get the tbody node for the table in the API's context.

    Related Pages:

      https://datatables.net/reference/api/table().body()

    :return:
    """
    raise NotImplementedError()

  @property
  def row(self):
    """
    Description:
    -----------
    Link to the single row API.

    Related Pages:

      https://datatables.net/reference/api/row()
    """
    return RowAPI(self.component, selector="%s.row()" % self.varId, set_var=False, page=self.page)

  @property
  def rows(self):
    """
    Description:
    -----------
    Link to the rows API.

    Related Pages:

      https://datatables.net/reference/api/rows()
    """
    return RowAPI(self.component, selector="%s.rows()" % self.varId, set_var=False, page=self.page)

  def adjust(self):
    """
    Description:
    -----------
    Adjust the column sizes of a newly shown table:

    Related Pages:

      https://datatables.net/reference/api/columns.adjust()
    """
    return JsObjects.JsVoid("%s.columns.adjust()" % self.varId)

  def container_jquery(self):
    """
    Description:
    -----------
    Get the div container node for the table in the API's context.

    Related Pages:

      https://datatables.net/reference/api/table().container()
    """
    return JsQuery.JQuery(
      component=self.component, selector="jQuery(%s.table().container())" % self.varId, set_var=False)

  def container_dom(self):
    """
    Description:
    -----------
    Get the div container node for the table in the API's context.

    Related Pages:

      https://datatables.net/reference/api/table().container()
    """
    return JsNodeDom.JsDoms(component=self.component, js_code="%s.table().container()" % self.varId, set_var=False)

  def footer(self):
    """
    Description:
    -----------
    Get the tfoot node for the table in the API's context.

    Related Pages:

      https://datatables.net/reference/api/table().footer()
    """

  def header(self):
    """
    Description:
    -----------
    Get the thead node for the table in the API's context.

    Related Pages:

      https://datatables.net/reference/api/table().header()
    """

  def nodes(self):
    """
    Description:
    -----------
    Get the table node for the table in the API's context.

    Related Pages:

      https://datatables.net/reference/api/table().node()
    """
    return self.fnc("nodes()")

  def jquery_node(self):
    """
    Description:
    -----------
    Get the cell nodes for the selected column.

    Related Pages:

      https://datatables.net/reference/api/column().nodes()
    """
    return JsQuery.JQuery(component=self.component, selector="%s.nodes().to$()" % self.varId, set_var=False)

  def clear(self, update=False):
    """
    Description:
    -----------
    Clear the table of all data:

    Related Pages:

      https://datatables.net/reference/api/clear()

    :param update: Boolean
    """
    if update:
      self.fnc("clear()")
      return self.draw()

    return self.fnc("clear()")

  def data(self):
    """
    Description:
    -----------
    Retrieve the data for the whole table, in row index order.

    Related Pages:

      https://datatables.net/reference/api/data()
    """
    return JsObjects.JsArray.JsArray.get("%s.data()" % self.varId)

  def destroy(self, remove=False, check_undefined=False):
    """
    Description:
    -----------
    Restore the tables in the current context to its original state in the DOM by removing all of DataTables
    enhancements, alterations to the DOM structure of the table and event listeners.

    Related Pages:

      https://datatables.net/reference/api/destroy()

    :param remove: Boolean, Completely remove the table from the DOM (true) or leave it in the DOM in its original
    plain un-enhanced HTML state (default, false).
    :param check_undefined: Boolean
    """
    return self.fnc_closure("destroy(%s)" % JsUtils.jsConvertData(remove, None), check_undefined=check_undefined)

  def draw(self, target=None):
    """
    Description:
    -----------
    Redraw the DataTables in the current context, optionally updating ordering, searching and paging as required.

    Related Pages:

      https://datatables.net/reference/api/draw()
    """
    if target is not None:
      return self.fnc_closure("draw(%s)" % JsUtils.jsConvertData(target, None))

    return self.fnc_closure("draw()")

  def order(self, data=None):
    """
    Description:
    -----------

    Related Pages:

      https://datatables.net/reference/api/order()
    """
    if data is not None:
      data = JsUtils.jsConvertData(data, None)
      return self.fnc("order(%s)" % data)

    return self.fnc("order()")

  def page(self, action: str):
    """
    Description:
    -----------

    Related Pages:

      https://datatables.net/reference/api/page()

    :return:
    """
    if action not in ("first", "next", "previous", "last"):
      raise ValueError("Action not defined")

    return self

  def search(self, data):
    """
    Description:
    -----------

    Related Pages:

      https://datatables.net/reference/api/search()

    :param jsData:
    """

    return self

  def settings(self):
    """
    Description:
    -----------

    Related Pages:

      https://datatables.net/reference/api/settings()
    """
    return self.fnc("settings()")

  def state(self):
    """
    Description:
    -----------
    Get the last saved state of the table.

    Related Pages:

      https://datatables.net/reference/api/state()
    """
    return JsObjects.JsObject.JsObject.get("%s.state()" % self.varId)

  def cell(self, cellSelector=None, rowColSelector=None):
    """
    Description:
    -----------
    Select cells found by both row and column selectors

    Related Pages:

      https://datatables.net/reference/api/cells()
      https://datatables.net/reference/api/cell()
    """
    if cellSelector is not None:
      selector = "%s.cell(%s)" % self.toStr()
    elif rowColSelector is not None:
      selector = "%s.cell(%s, %s)" % (self.toStr(), rowColSelector[0], rowColSelector[1])
    else:
      selector = "%s.cell()" % self.toStr()
    return CellAPI(selector)

  def column(self, colSelector):
    """
    Description:
    -----------

    :param colSelector:
    """
    if colSelector is not None:
      selector = "%s.column(%s)" % (self.toStr(), JsUtils.jsConvertData(colSelector, None))
    else:
      selector = "%s.column()" % self.toStr()
    return ColumnAPI(selector)

  def columns(self, colSelector):
    """
    Description:
    -----------

    :param colSelector:
    """
    if colSelector is not None:
      selector = "%s.column(%s)" % (self.varId, JsUtils.jsConvertData(colSelector, None))
    else:
      selector = "%s.column()" % self.varId
    return ColumnAPI(selector)

  def select(self):
    """
    Description:
    -----------
    Initialise Select from outside of the constructor.

    Related Pages:

      https://datatables.net/reference/api/select()

    TODO add the select true
    """
    return SelectAPI(selector="%s.select()", set_var=False)
