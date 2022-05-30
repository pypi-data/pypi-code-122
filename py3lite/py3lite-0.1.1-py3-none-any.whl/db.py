from collections import ChainMap
from .connection import Connection
from . import models
from .query import Query, InsertQuery, UpdateQuery, DeleteQuery, Index, MultiColumnIndex


class ModelMeta(type):
    """
    Metaclass that surgically instruments subclasses to support SQL operations.

    - It automatically creates an id field on all models, inserts all model column types
     into the class body.

    - Attaches the connection_class,  extracts fields, creates tables, triggers, views and indexes.

    - It also setsup reverse lookups and signals(hooks)

    """
    @classmethod
    def __prepare__(cls, name, bases):
        id_dict = dict(id=models.Integer(
            primary_key=True, auto_increment=True))

        columns = {key: val for key, val in models.__dict__.items()}
        return dict(ChainMap({}, columns, id_dict))

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)

        setattr(clsobj, 'connection_class', Connection)

        for key, val in vars(clsobj).items():
            if isinstance(val, models.Descriptor):
                setattr(val, 'name', key)

        fields = [key for key, val in clsobj.__dict__.items()
                  if isinstance(val, models.Descriptor)]

        setattr(clsobj, '_fields', fields)

        columns = {key: val for key, val in vars(clsobj).items()
                   if isinstance(val, models.Typed)}

        setattr(clsobj, 'columns', columns)
        setattr(clsobj, 'related_objects', [])

        # Register the model
        if clsname != 'Model':
            if clsobj not in models.MODELS:
                # Register the model if not base class
                models.MODELS.add(clsobj)

            # Create table automatically
            if not Connection.db_exits() or Connection.migrate:
                clsobj().create_table()
                clsobj().create_indexes()
                clsobj().create_triggers()

            if 'verbose_name' not in clsobj.Meta.__dict__:
                clsobj.verbose_name = clsobj.__name__.upper()

            if 'verbose_name_plural' not in clsobj.Meta.__dict__:
                clsobj.verbose_name_plural = clsobj.__name__.upper() + "S"

        def get_related(column, parent_model, fk):
            @property
            def __wrapper(self):
                if isinstance(column, models.OneToOneField):
                    obj = clsobj().get(**{fk: self.id})
                    return obj
                else:
                    qs = clsobj().query.where(**{fk: self.id})
                    return qs

            return __wrapper

        for key, column in columns.items():
            if isinstance(column, models.ForeignKey):
                related_name = column.related_name
                parent_model = column.to
                fk = column.name
                parent_model.related_objects.append((related_name, fk))
                setattr(parent_model, related_name,
                        get_related(column, parent_model, fk))

        # Default signals
        def call_back(*args, **kwargs):
            return None

        default_signals = ['pre_save_callback', 'post_save_callback',
                           'pre_update_callback', 'post_update_callback',
                           'pre_delete_callback', 'post_delete_callback']

        for sig in default_signals:
            setattr(clsobj, sig, call_back)

        return clsobj


class Model(metaclass=ModelMeta):
    """Base class for all instances

    Attributes:

    Meta:
        indexes: list of index columns
        index_together = list of dictionaries of composite indexes
        abstract: bool
        search_filter: list of cols to filter by
        search_filter_verbose: list of verbose names for search_filter
    """

    class Meta:
        indexes = []
        index_together = []
        abstract = False
        search_filter = ['id']
        search_filter_verbose = ['ID']

    def __init__(self, **kwargs):
        """Initialises instance fields and validates them."""

        for name, value in kwargs.items():
            setattr(self, name, value)

    @classmethod
    def __init_subclass__(cls):
        """Sets the table name using the lowercase class name.

        If the 'table' attribute already exists, its used instead

        """
        if not hasattr(cls, 'table'):
            setattr(cls, 'table', cls.__name__.lower())

        return cls

    def __repr__(self):
        params = ', '.join(
            f"{key}={val}" for key, val in self.__dict__.items() if key in self._fields)

        return "{}({})".format(type(self).__name__, params)

    def qualified_fields(self, fields=None):
        """Qualified column names, fit for use in SQL Join.

        Each colname is prefixed with the table name
        """
        return [self.table + "." + f for f in fields or self._fields]

    @property
    def pk(self):
        """Return an integer primary key"""

        return self.id

    @classmethod
    def describe(cls):
        """Returns a string of table schema"""
        with Connection() as cursor:
            cursor.execute(
                f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{cls.table}' ")
            return cursor.fetchone()[0]

    @classmethod
    def create_table(cls):
        """Creates the table associated with this model"""

        abstract = cls.Meta.__dict__.get('abstract', False)
        if abstract is False:
            schema = cls.schema()
            with Connection() as cursor:
                cursor.execute(schema)
            return True

    @classmethod
    def drop(cls):
        """Drops the table associated with this model"""

        with Connection() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {cls.table}")

    def get(self, **kwargs):
        """Query the database using specifying kwargs. kwargs can not be empty.

        Return a single model instance or None
        """

        if not kwargs:
            raise TypeError("No specified query kwargs")

        query = self.query.where(**kwargs)
        rows, cursor = query.fetchmany(1)

        if rows:
            desc = [i[0] for i in cursor.description]
            row = rows[0]
            if isinstance(row, dict):
                data = dict(zip(desc, row.values()))
            else:
                data = dict(zip(desc, row))
            return self.__class__(**data)

        return None

    def rename(self, new_table: str):
        """Rename the table with new_table"""
        with Connection() as cursor:
            cursor.execute(f"ALTER TABLE {self.table} RENAME TO {new_table}")
            return True

    @classmethod
    def schema(cls):
        sql = ",\n".join([f"{key} {value.schema()}" for key,
                         value in cls.__dict__.items() if key in cls._fields])

        sql = f"CREATE TABLE IF NOT EXISTS {cls.table}({sql}".strip()
        # Attach foreign keys, Unique constraint at table def level

        for key, value in cls.__dict__.items():
            if isinstance(value, (models.ForeignKey, models.Unique)):
                sql += f",\n{str(value)}"

        sql += ")"
        return sql

    def toDict(self, cursor):
        colnames = [row[0] for row in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(colnames, r)) for r in results]

    def count(self):
        sql = f'SELECT COUNT(*) FROM {self.table}'
        with Connection() as conn:
            cursor = conn.execute(sql)
            count = cursor.fetchone()
            return count[0]

    @property
    def query(self) -> Query:
        """Query the database."""
        return Query(self).with_table(self.table)

    def pre_process_instance(self, silence_error=False):
        """
        Extract column names and their data before saving the instance
        Raises a TypeError if NoneNullable fields are not specified.
        """
        columns = self.columns
        fields = set(self._fields)
        instance_data = self.__dict__

        db_data = {k: v for k, v in instance_data.items() if k in fields}
        colnames = instance_data.keys()

        if not silence_error:
            for field in (fields - colnames):
                column = columns[field]
                if not column.nullable and not column.default:
                    raise TypeError(
                        f"Non nullable field {field} with no default needs a value")
        return db_data

    def save(self):
        """Persist this instance into the database. Return id of inserted row"""
        insert_query = InsertQuery(self)
        lastrowid = insert_query.save()
        return lastrowid

    def update(self, **kwargs):
        """Update rows matching kwargs"""

        update_query = UpdateQuery(self)
        updated_count = update_query.save(**kwargs)
        return updated_count

    def delete(self, **kwargs):
        """Delete rows matching kwargs"""
        delete_query = DeleteQuery(self)
        deleted_count = delete_query.delete(**kwargs)
        return deleted_count

    def executemany(self, data, fields=None, exclude=None):
        """Run bulk-insert of data, match specified fields or all fields except those
        specified in exclude list.
        """

        if not isinstance(data, (list, tuple)):
            raise TypeError("data must be a tuple or list")

        exclude = exclude or []
        fields = fields or self._fields
        fields = [item for item in fields if item not in exclude]

        keys = ", ".join(fields)
        params = ", ".join(['?' for _ in range(len(fields))])
        sql = f"INSERT INTO {self.table}({keys}) VALUES({params})"

        with Connection() as conn:
            cursor = conn.executemany(sql, data)
            return cursor.rowcount

    @classmethod
    def table_info(cls):
        """Returns a dict of table cols and their schema"""

        sql = f"PRAGMA TABLE_INFO('{cls.table}');"
        with Connection() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            colnames = [item[1] for item in results]
            colschema = [item[2] for item in results]
            return dict(zip(colnames, colschema))

    @classmethod
    def add_index(cls, column):
        """Create an sql index"""
        return Index(cls, column, Connection)

    @classmethod
    def add_multi_index(cls, index_name, column_list):
        """Creates multi-column/composite indexes with idx_name"""
        return MultiColumnIndex(cls, index_name, column_list, Connection)

    @classmethod
    def from_csv(cls, filename, types, as_dict=False, as_obj=False):
        """
        Import table data for a model from a csv filename.
        types: tuple of callables that will cast each row into it's real datatype.
        e.g [imt, float, str] etc.
        Expects the first row to be a header. Failure to have a header in the csv will
        cause the first row to be skipped.

        if as_dict:
            returns a list of dictionaries
        if as_obj:
            returns a list of instances created with the parsed data.
        """

        import csv
        with open(filename, 'r', newline='') as f:
            headers = next(f).split(",")
            rows = csv.reader(f)

            dicts = []
            for _, row in enumerate(rows):
                row = [func(val.strip()) for func, val in zip(types, row)]
                row_dict = {k.strip(): v for k, v in zip(headers, row)}
                dicts.append(row_dict)

            if as_obj:
                instance_objs = [cls(**dict_obj) for dict_obj in dicts]
                return instance_objs

            elif as_dict:
                return dicts
            else:
                return []

    def create_triggers(self):
        """Creates triggers and views.

        All triggers/views should be functions that end with __sqltrigger and views with __sqlview
        """
        for key, val in vars(self.__class__).items():
            if callable(val) and val.__name__.endswith('__sqltrigger'):
                getattr(self, key)()

            if callable(val) and val.__name__.endswith('__sqlview'):
                getattr(self, key)()

    @classmethod
    def create_indexes(cls):
        """This class method introspects the class and creates single and composite indexes.
        Specify indexes as class attributes:

        indexes = ["name", "title"]
        index_together = [
            {
                "name_title": ["name", "title"]
            }
        ]
        """

        index_list = cls.Meta.__dict__.get('indexes', [])
        for column in index_list:
            cls.add_index(column)

        multi_index_list = cls.Meta.__dict__.get('index_together', [])
        for item_dict in multi_index_list:
            for index_name, column_list in item_dict.items():
                cls.add_multi_index(index_name, column_list)

    def pre_save(self):
        """Pre-save hook called before the model instance is saved"""
        return self.pre_save_callback()

    def post_save(self):
        """Post-save hook called after the model instance is saved"""
        return self.post_save_callback()

    def pre_update(self):
        """Pre-save hook called before the model instance is updated"""
        return self.pre_update_callback()

    def post_update(self):
        """Post-update hook called after the model instance is updated"""
        return self.post_update_callback()

    def pre_delete(self):
        """Pre-delete hook called before the model instance is deleted"""
        return self.pre_delete_callback()

    def post_delete(self):
        """Post-save hook called after the model instance is deleted"""
        return self.post_delete_callback()
