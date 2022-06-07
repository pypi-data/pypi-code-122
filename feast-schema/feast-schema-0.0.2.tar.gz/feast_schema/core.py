import json
import warnings

from feast import FeatureStore
from google.protobuf.json_format import MessageToDict
from IPython.core.display import HTML, display
from json2html import json2html

warnings.filterwarnings("ignore")


class FeastSchema:
    def __init__(self, repo_path: str):
        self.store = FeatureStore(repo_path=repo_path)

    def show_schema(self, skip_meta: bool = False):
        feast_schema = self.store_schema(skip_meta)
        display(HTML(json2html.convert(json=feast_schema)))

    def show_table_schema(self, table: str, skip_meta: bool = False):
        feasture_tables_dictionary = self.store_schema(skip_meta)
        display(
            HTML(json2html.convert(json={table: feasture_tables_dictionary[table]}))
        )

    def _entity_to_dict(self, entity):
        entity_dict = MessageToDict(entity.to_proto())

        if entity_dict["meta"] == {}:
            del entity_dict["meta"]

        return entity_dict

    def store_schema(self, skip_meta: bool = False):
        entities_dictionary = {}
        feast_entities = self.store.list_entities()
        for entity in feast_entities:
            entity_dictionary = self._entity_to_dict(entity)
            entity_spec = entity_dictionary["spec"]
            entities_dictionary[entity_spec["name"]] = entity_spec

        feasture_tables_dictionary = {}
        feast_feature_tables = self.store.list_feature_views()
        for feature_table in feast_feature_tables:
            feature_table_dict = json.loads(str(feature_table))
            feature_table_spec = feature_table_dict["spec"]
            feature_table_name = feature_table_spec["name"]
            feature_table_spec.pop("name", None)
            if "entities" in feature_table_spec:
                feature_table_entities = []
                for entity in feature_table_spec["entities"]:
                    feature_table_entities.append(entities_dictionary[entity])
                feature_table_spec["entities"] = feature_table_entities

            if not skip_meta:
                feature_table_spec["meta"] = feature_table_dict["meta"]
            else:
                feature_table_spec.pop("input", None)
                feature_table_spec.pop("ttl", None)
                feature_table_spec.pop("online", None)

            feasture_tables_dictionary[feature_table_name] = feature_table_spec

        return feasture_tables_dictionary
