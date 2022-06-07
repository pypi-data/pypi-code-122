""" math_parser.Parser """

from re import findall
from typing import List

from .Node import Node, TokenType


def lexical_analysis(s: str) -> List[Node]:
    """ Get all Nodes of a Mathematics Expression. """
    mapping = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTI,
        '/': TokenType.DIV,
        '^': TokenType.POW,
        '(': TokenType.L_PARENTHESIS,
        ')': TokenType.R_PARENTHESIS
    }

    token_values = findall(r"(\d*\.\d+|\d+|[+\-*^/]|[\(\)])", s)
    tokens = []
    for val in token_values:
        if val in mapping:
            token_type = mapping[val]
            token = Node(token_type, value=val)

        else:
            token = Node(TokenType.NUM, value=float(val))

        tokens.append(token)

    tokens.append(Node(TokenType.END))
    return tokens


def check(tokens: List[Node], token_type: TokenType) -> Node:
    """ Check if the First Node of the List corresponds To a certain TokenType. """
    if tokens[0].token_type == token_type:
        return tokens.pop(0)

    else:
        raise Exception(f'Invalid Syntax on Token {tokens[0].token_type}')


def parse_e(tokens: List[Node]) -> Node:
    """ Run through the First Group of Operators. (Plus and Minus) """
    left_node = parse_e2(tokens)

    while tokens[0].token_type in [TokenType.PLUS, TokenType.MINUS]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e2(tokens))
        left_node = node

    return left_node


def parse_e2(tokens: List[Node]) -> Node:
    """ Run through the Second Group of Operators. (Multiply and Divider) """
    left_node = parse_e3(tokens)

    while tokens[0].token_type in [TokenType.MULTI, TokenType.DIV]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e3(tokens))
        left_node = node

    return left_node


def parse_e3(tokens: List[Node]) -> Node:
    """ Run through the Third Group of Operators. (Power) """
    left_node = parse_e4(tokens)

    while tokens[0].token_type == TokenType.POW:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e4(tokens))
        left_node = node

    return left_node


def parse_e4(tokens: List[Node]) -> Node:
    """ Run through the End Group of Operators. (Number) """
    if tokens[0].token_type == TokenType.NUM:
        return tokens.pop(0)

    check(tokens, TokenType.L_PARENTHESIS)
    expression = parse_e(tokens)
    check(tokens, TokenType.R_PARENTHESIS)

    return expression


def parse(value: str) -> Node:
    """ Get all Nodes, and it's Child's, of the Expression. """
    tokens = lexical_analysis(value)
    node = parse_e(tokens)
    check(tokens, TokenType.END)
    return node
