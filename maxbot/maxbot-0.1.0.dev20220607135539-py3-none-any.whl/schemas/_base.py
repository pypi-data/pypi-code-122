from types import SimpleNamespace

from marshmallow import Schema, post_load, pre_load
from marshmallow.exceptions import ValidationError

from ._render import Yaml, YamlConfig


class Config(Schema):
    class Meta:
        render_module = YamlConfig()

    def from_yaml(self, filename, variables=None):
        with open(filename, "r") as f:
            return self.loads(f.read(), variables=variables)

    @post_load
    def create(self, data, **kwargs):
        for name in self._declared_fields:
            data.setdefault(name, None)
        return SimpleNamespace(**data)


class DataObject(Schema):
    @pre_load
    def short_syntax(self, data, **kwargs):
        # short syntax for schemas class with one required argument
        if isinstance(data, str):
            for name, field in self._declared_fields.items():
                if field.required:
                    data = {name: data}
                    break
        return data

    @post_load
    def create(self, data, **kwargs):
        for name in self._declared_fields:
            data.setdefault(name, None)
        return data


class Envelope(Schema):
    class Meta:
        render_module = Yaml()

    @post_load
    def unwrap_envelope(self, data, **kwargs):
        if not isinstance(data, dict):
            raise ValidationError("Input data must be a dict.")
        if len(data) != 1:
            raise ValidationError("Input dict must contain exactly one key.")
        name, args = next(iter(data.items()))
        # TODO use dataclasses
        return SimpleNamespace(name=name, **args)
