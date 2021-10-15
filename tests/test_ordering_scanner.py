import unittest

from wtoolzargs.common import exceptions
from wtoolzargs.common import token_
from wtoolzargs.ordering import scanner
from wtoolzargs.ordering import tokentype

import common

Case = common.Case
ScanError = exceptions.ScanError
TT = tokentype.TokenType
Token = token_.Token


def func(source):
    return scanner.Scanner(source).scan()


class TestOrderingScanner(unittest.TestCase):
    def test_scan(self):
        cases = [
            Case(
                "a, b",
                [
                    Token(
                        type_=TT.IDENTIFIER, lexeme="a", literal=None, line=1
                    ),
                    Token(
                        type_=TT.SEPERATOR, lexeme=",", literal=None, line=1
                    ),
                    Token(
                        type_=TT.IDENTIFIER, lexeme="b", literal=None, line=1
                    ),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case(
                "a asc, b asc",
                [
                    Token(
                        type_=TT.IDENTIFIER, lexeme="a", literal=None, line=1
                    ),
                    Token(type_=TT.ASC, lexeme="asc", literal=None, line=1),
                    Token(
                        type_=TT.SEPERATOR, lexeme=",", literal=None, line=1
                    ),
                    Token(
                        type_=TT.IDENTIFIER, lexeme="b", literal=None, line=1
                    ),
                    Token(type_=TT.ASC, lexeme="asc", literal=None, line=1),
                    Token(type_=TT.EOF, lexeme="", literal=None, line=1),
                ],
            ),
            Case("a asc; b asc", ScanError),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main(module="test_ordering_scanner")
