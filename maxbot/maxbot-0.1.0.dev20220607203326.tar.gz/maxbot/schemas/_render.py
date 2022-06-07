import re

import yaml


class Yaml:
    def loads(self, string):
        return yaml.safe_load(string)


class YamlConfig:
    def loads(self, string, variables=None):
        Loader = type("ConfigLoader", (yaml.SafeLoader,), {})
        _register_scenario_syntax(Loader)
        _register_variable_substitution(Loader, variables)
        # nosec note: actualy we derive a safe loader
        return yaml.load(string, Loader=Loader)  # nosec B506


def _register_scenario_syntax(Loader):
    def jinja_syntax(syntax):
        def constructor(loader, node):
            return {"content": loader.construct_scalar(node), "syntax": syntax}

        if syntax == "raw":
            # raw syntax is default
            Loader.add_constructor("!jinja", constructor)
        Loader.add_constructor(f"!jinja/{syntax}", constructor)

    jinja_syntax("raw")
    jinja_syntax("yaml")


def _register_variable_substitution(Loader, variables):
    variables = variables or {}
    VARIABLE = re.compile(r".*?\$\{([^}{:]+)(:([^}]+))?\}.*?")

    def substitute_variables(loader, node):
        string = loader.construct_scalar(node)
        for name, with_colon, default in VARIABLE.findall(string):
            if with_colon:
                value = variables.get(name, default)
            else:
                value = variables[name]
            # replace only first occurance because the same variable can occur
            # with different default values
            string = string.replace(f"${{{name}{with_colon}}}", value, 1)
        return string

    Loader.add_constructor("!ENV", substitute_variables)
