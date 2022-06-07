""" math_parser.Compute """

import operator

from .Node import Node, TokenType
from .Parser import parse


operations = {
    TokenType.PLUS: operator.add,
    TokenType.MINUS: operator.sub,
    TokenType.MULTI: operator.mul,
    TokenType.DIV: operator.truediv,
    TokenType.POW: operator.pow
}


def compute(node: Node) -> float:
    """ Evaluate the Node Value. """
    if node.token_type == TokenType.NUM:
        return node.value

    left = compute(node.children[0])
    right = compute(node.children[1])
    operation = operations[node.token_type]

    return operation(left, right)


def evaluate(value: str, **kwargs) -> float:
    """ Evaluate a Math Expression, and it's Variables. """
    for key, val in kwargs.items():
        value = value.replace(key, str(val))

    return compute(parse(value))
