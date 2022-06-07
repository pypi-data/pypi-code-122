""" math_parser.Node """

import enum


class TokenType(enum.Enum):
    NUM = 1
    PLUS = 2
    MINUS = 3
    MULTI = 4
    DIV = 5
    POW = 6
    L_PARENTHESIS = 7
    R_PARENTHESIS = 8
    END = 9


OPERATIONS_ALLOWED = [
    '+', '-', '*', '/', '^'
]


class Node:
    def __init__(self, token_type: TokenType, value: any = None):
        self.token_type = token_type
        self.value = value
        self.children = []
        self.id = None
