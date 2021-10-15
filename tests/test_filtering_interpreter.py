import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative

from wtoolzargs.common import exceptions
from wtoolzargs.filtering import interpreter
from wtoolzargs.filtering import parser
from wtoolzargs.filtering import scanner

import common

Base = declarative.declarative_base()
Case = common.Case
InterpretError = exceptions.InterpretError


class Hacker(Base):
    __tablename__ = "hacker"
    id = Column(Integer, primary_key=True)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    e = Column(String)


def tokens(source):
    return scanner.Scanner(source).scan()


def parse(tokens):
    return parser.Parser(tokens).parse()


def func(args):
    source, field_mapping = args
    res = interpreter.Interpreter(
        Hacker, parse(tokens(source)), field_mapping
    ).interpret()
    return str(res.compile(compile_kwargs={"literal_binds": True}))


class FilteringInterpreter(unittest.TestCase):
    def test_interpret(self):
        cases = [
            Case(("a eq True", {}), "hacker.a = '1'"),
            Case(("a like '%some%'", {}), "hacker.a LIKE '%some%'"),
            Case(("a eq 10", {}), "hacker.a = 10.0"),
            Case(("a eq -10", {}), "hacker.a = -10.0"),
            Case(("a ne 10", {}), "hacker.a != 10.0"),
            Case(("a gt 10", {}), "hacker.a > 10.0"),
            Case(("a ge 10", {}), "hacker.a >= 10.0"),
            Case(("a lt 10", {}), "hacker.a < 10.0"),
            Case(("a le 10", {}), "hacker.a <= 10.0"),
            Case(("a eq not 10", {}), "hacker.a = (NOT 10.0)"),
            Case(
                ("a eq 10 and b eq 10", {}),
                "hacker.a = 10.0 AND hacker.b = 10.0",
            ),
            Case(
                ("a eq 10 or b eq 10", {}),
                "hacker.a = 10.0 OR hacker.b = 10.0",
            ),
            Case(
                ("(a eq 10 or b eq 10) and c eq 10", {}),
                "(hacker.a = 10.0 OR hacker.b = 10.0) AND hacker.c = 10.0",
            ),
            Case(("a eq 'a'", {}), "hacker.a = 'a'"),
            Case(
                ("a eq 'a' and b eq 'b'", {}),
                "hacker.a = 'a' AND hacker.b = 'b'",
            ),
            Case(("not a eq not 'b'", {}), "hacker.a != (NOT 'b')"),
            Case(
                ("not (a eq 'a' and b eq 'b')", {}),
                "NOT (hacker.a = 'a' AND hacker.b = 'b')",
            ),
            Case(
                ("(a eq 'a' or b eq 'b') and c eq 'c'", {}),
                "(hacker.a = 'a' OR hacker.b = 'b') AND hacker.c = 'c'",
            ),
            Case(
                ("a eq 'a' or b eq 'b' and d eq 'd' or e eq 'e'", {}),
                (
                    "hacker.a = 'a' OR hacker.b = 'b' AND "
                    "hacker.d = 'd' OR hacker.e = 'e'"
                ),
            ),
            Case(("z eq 'a'", {"z": "a"}), "hacker.a = 'a'"),
            Case(("z eq 'a'", {}), InterpretError),
        ]
        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main()
