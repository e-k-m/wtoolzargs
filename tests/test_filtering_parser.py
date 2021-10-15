import unittest

from wtoolzargs.filtering import parser
from wtoolzargs.filtering import scanner
from wtoolzargs.common import astprinter
from wtoolzargs.common import exceptions

import common

Case = common.Case
ParseError = exceptions.ParseError


def tokens(source):
    return scanner.Scanner(source).scan()


def parse(tokens):
    return parser.Parser(tokens).parse()


def func(source):
    return astprinter.AstPrinter().print(parse(tokens(source)))


class TestFilteringParser(unittest.TestCase):
    def test_parse(self):
        cases = [
            Case("a like True", "(like a '1')"),
            Case("a like False", "(like a '0')"),
            Case("a like not False", "(like a (not '0'))"),
            Case("a like '10'", "(like a '10')"),
            Case("a eq 10", "(eq a 10.0)"),
            Case("a eq 'a'", "(eq a 'a')"),
            Case("a eq 'a' and b eq 'b'", "(and (eq a 'a') (eq b 'b'))"),
            Case("a eq not 'a'", "(eq a (not 'a'))"),
            Case("not a eq not 'b'", "(not (eq a (not 'b')))"),
            Case(
                "not (a eq 'a' and b eq 'b')",
                "(not (group (and (eq a 'a') (eq b 'b'))))",
            ),
            Case(
                "(a eq 'a' or b eq 'b') and c eq 'c'",
                "(and (group (or (eq a 'a') (eq b 'b'))) (eq c 'c'))",
            ),
            Case(
                "a eq 'a' or b eq 'b' and d eq 'd' or e eq 'e'",
                "(or (or (eq a 'a') (and (eq b 'b') (eq d 'd'))) (eq e 'e'))",
            ),
            Case("a eq 'a' b eq 'b'", ParseError),
            Case("a eq a", ParseError),
            Case("a eq b eq 'c'", ParseError),
            Case("a eq (b eq 'c')", ParseError),
            Case("a", ParseError),
            Case("a and b", ParseError),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main(module="test_ordering_scanner")
