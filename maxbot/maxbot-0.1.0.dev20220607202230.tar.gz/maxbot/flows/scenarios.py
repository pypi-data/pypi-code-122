from functools import singledispatch

import jinja2
from jinja2.ext import Extension
from jinja2.nodes import Assign, Call, ContextReference, Getattr, Keyword, Name


class VariablesExtension(Extension):

    tags = {"slot", "user"}

    def parse(self, parser):
        var = parser.stream.current.value
        lineno = next(parser.stream).lineno

        name = parser.stream.expect("name").value
        parser.stream.expect("assign")
        value = parser.parse_expression()

        # transform our custom statements into dict updates
        # {% user name = 'Bob' %}
        #   -> {% set _ = user.update({'name': 'Bob'}) %}
        # {% slot guests = entities.number %}
        #   -> {% set _ = slots.update({'guests': entities.number}) %}
        if var == "slot":
            var = "slots"
        method = Getattr(Name(var, "load"), "update", ContextReference())
        call = Call(method, [], [Keyword(name, value)], None, None)
        dummy = Name("_", "store")
        return Assign(dummy, call).set_lineno(lineno)


# nosec note: autoescape is not actual when rendering yaml
jinja_env = jinja2.Environment(extensions=[VariablesExtension], autoescape=False)  # nosec B701


def _build_params(context, params):
    result = vars(context)
    if params is not None:
        result.update(params)
    return result


def Expression(string):
    expr = jinja_env.compile_expression(string)

    def evaluate(context, **params):
        params = _build_params(context, params)
        return expr(**params)

    return evaluate


@singledispatch
def Scenario(raw):
    raise TypeError(f"Unexpected argument type {type(raw)}")


@Scenario.register(dict)
def Template(template):
    tpl = jinja_env.from_string(template["content"])
    schema = template["schema"]
    syntax = template["syntax"]

    def template(context, **params):
        params = _build_params(context, params)
        string = tpl.render(**params)
        if isinstance(string, str) and string.strip():
            if syntax == "raw":
                return schema.load(string)
            elif syntax == "yaml":
                return schema.loads(string)
            else:
                raise RuntimeError(f"Unknown content syntax {syntax}")
        else:
            return []

    return template


@Scenario.register(list)
def Commands(cmd_list):
    def commands(context, **params):
        return cmd_list

    return commands
