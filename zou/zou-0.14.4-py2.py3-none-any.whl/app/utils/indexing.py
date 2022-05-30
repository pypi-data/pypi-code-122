from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, NGRAMWORDS, ID
from whoosh.analysis import StemmingAnalyzer


def get_schema(schema):
    kwargs = {}
    for key, value in schema.items():
        if value == "indexed":
            kwargs[key] = NGRAMWORDS(minsize=2, sortable=True)
        elif value == "id_stored":
            kwargs[key] = ID(stored=True)
        elif value == "unique_id_stored":
            kwargs[key] = ID(unique=True, stored=True)
    return Schema(**kwargs)


def create_index(path, schema):
    return index.create_in(path, schema)


def get_index(path):
    return index.open_dir(path)


def index_data(ix, data):
    writer = ix.writer(limitmb=1024)
    writer.add_document(**data)
    writer.commit()
    return writer


def search(ix, query, limit=10):
    query_parser = QueryParser("name", schema=ix.schema)
    whoosh_query = query_parser.parse(query)
    ids = []
    with ix.searcher() as searcher:
        results = searcher.search(whoosh_query, limit=limit)
        for result in results:
            ids.append(result["id"])
    return ids
