import unittest

from wtoolzargs.common import exceptions
from wtoolzargs.common import token_
from wtoolzargs.filtering import scanner
from wtoolzargs.filtering import tokentype

import common

Case = common.Case
ScanError = exceptions.ScanError
TT = tokentype.TokenType
Token = token_.Token


def func(source):
    return scanner.Scanner(source).scan()


class TestFilteringScanner(unittest.TestCase):
    def test_scan(self):
        cases = [
            Case(
                "city eq True and price gt 3.5",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="city",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.EQUAL, lexeme="eq", literal=None, line=1),
                    Token(type_=TT.BOOL, lexeme="True", literal="1", line=1,),
                    Token(type_=TT.AND, lexeme="and", literal=None, line=1),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.GREATER_THAN,
                        lexeme="gt",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="3.5", literal=3.5, line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "city eq False",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="city",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.EQUAL, lexeme="eq", literal=None, line=1),
                    Token(type_=TT.BOOL, lexeme="False", literal="0", line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "True eq False",
                [
                    Token(type_=TT.BOOL, lexeme="True", literal="1", line=1,),
                    Token(type_=TT.EQUAL, lexeme="eq", literal=None, line=1),
                    Token(type_=TT.BOOL, lexeme="False", literal="0", line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "city like 'Redmond'",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="city",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.LIKE, lexeme="like", literal=None, line=1),
                    Token(
                        type_=TT.STRING,
                        lexeme="'Redmond'",
                        literal="Redmond",
                        line=1,
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "city eq 'Redmond'",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="city",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.EQUAL, lexeme="eq", literal=None, line=1,),
                    Token(
                        type_=TT.STRING,
                        lexeme="'Redmond'",
                        literal="Redmond",
                        line=1,
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "city ne 'London'",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="city",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.NOT_EQUAL, lexeme="ne", literal=None, line=1,
                    ),
                    Token(
                        type_=TT.STRING,
                        lexeme="'London'",
                        literal="London",
                        line=1,
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "price gt 20",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.GREATER_THAN,
                        lexeme="gt",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="20", literal=20.0, line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "price ge 10",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.GREATER_THAN_OR_EQUAL,
                        lexeme="ge",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="10", literal=10.0, line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "price lt 20",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.LESS_THAN, lexeme="lt", literal=None, line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="20", literal=20.0, line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "price le 100",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.LESS_THAN_OR_EQUAL,
                        lexeme="le",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.NUMBER, lexeme="100", literal=100.0, line=1,
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "price le 200 and price gt 3.5",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.LESS_THAN_OR_EQUAL,
                        lexeme="le",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.NUMBER, lexeme="200", literal=200.0, line=1,
                    ),
                    Token(type_=TT.AND, lexeme="and", literal=None, line=1),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.GREATER_THAN,
                        lexeme="gt",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="3.5", literal=3.5, line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "price le 3.5 or price gt 200",
                [
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.LESS_THAN_OR_EQUAL,
                        lexeme="le",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="3.5", literal=3.5, line=1,),
                    Token(type_=TT.OR, lexeme="or", literal=None, line=1),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.GREATER_THAN,
                        lexeme="gt",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.NUMBER, lexeme="200", literal=200.0, line=1,
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "not price le 3.5",
                [
                    Token(type_=TT.NOT, lexeme="not", literal=None, line=1),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.LESS_THAN_OR_EQUAL,
                        lexeme="le",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.NUMBER, lexeme="3.5", literal=3.5, line=1,),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "(priority eq 1 or city eq 'Redmond') and price gt 100",
                [
                    Token(
                        type_=TT.LEFT_PAREN, lexeme="(", literal=None, line=1,
                    ),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="priority",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.EQUAL, lexeme="eq", literal=None, line=1,),
                    Token(type_=TT.NUMBER, lexeme="1", literal=1.0, line=1),
                    Token(type_=TT.OR, lexeme="or", literal=None, line=1),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="city",
                        literal=None,
                        line=1,
                    ),
                    Token(type_=TT.EQUAL, lexeme="eq", literal=None, line=1,),
                    Token(
                        type_=TT.STRING,
                        lexeme="'Redmond'",
                        literal="Redmond",
                        line=1,
                    ),
                    Token(
                        type_=TT.RIGHT_PAREN, lexeme=")", literal=None, line=1,
                    ),
                    Token(type_=TT.AND, lexeme="and", literal=None, line=1),
                    Token(
                        type_=TT.IDENTIFIER,
                        lexeme="price",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.GREATER_THAN,
                        lexeme="gt",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type_=TT.NUMBER, lexeme="100", literal=100.0, line=1,
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case("!", ScanError),
            Case(
                "\n", [Token(type_=TT.EOF, lexeme="", literal=None, line=1)],
            ),
            Case(
                "\t", [Token(type_=TT.EOF, lexeme="", literal=None, line=1)],
            ),
            Case(
                "\n", [Token(type_=TT.EOF, lexeme="", literal=None, line=1)],
            ),
            Case(
                "\r", [Token(type_=TT.EOF, lexeme="", literal=None, line=1)],
            ),
            Case(
                "  ", [Token(type_=TT.EOF, lexeme="", literal=None, line=1)],
            ),
            Case("'a", ScanError,),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main()
