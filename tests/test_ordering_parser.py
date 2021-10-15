import unittest

from wtoolzargs.ordering import scanner
from wtoolzargs.ordering import parser
from wtoolzargs.common import exceptions
from wtoolzargs.common import astprinter

import common

Case = common.Case
ParseError = exceptions.ParseError


def tokens(source):
    return scanner.Scanner(source).scan()


def parse(tokens):
    return parser.Parser(tokens).parse()


def func(source):
    return astprinter.AstPrinter().print(parse(tokens(source)))


class TestOrderingParser(unittest.TestCase):
    def test_parse(self):
        cases = [
            Case("b", "(asc b)"),
            Case("a asc", "(asc a)"),
            Case("a desc", "(desc a)"),
            Case("b ascdesc", ParseError),
            Case(" ", ParseError),
            Case("", ParseError),
            Case("b   ", "(asc b)"),
            Case("b       asc", "(asc b)"),
            Case("   b       asc", "(asc b)"),
            Case("   b       asc   ", "(asc b)"),
            Case("a asc, b desc", "(, (asc a) (desc b))"),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main(module="test_ordering_scanner")
