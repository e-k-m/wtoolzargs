import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative

import wtoolzargs

import common

# TODO: Maybe add test where queries happen agains in-memory database.

Case = common.Case
Base = declarative.declarative_base()
wtoolzargsError = wtoolzargs.wtoolzargsError


class Hacker(Base):
    __tablename__ = "hacker"
    id = Column(Integer, primary_key=True)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    e = Column(String)


def func_filter(args):
    source, field_mapping = args
    res = wtoolzargs.filter_(Hacker, source, field_mapping)
    return str(res.compile(compile_kwargs={"literal_binds": True}))


def func_order(args):
    source, field_mapping = args
    res = wtoolzargs.order(Hacker, source, field_mapping)
    return str(
        [str(e.compile(compile_kwargs={"literal_binds": True})) for e in res]
    )


class WToolzFilter(unittest.TestCase):
    def test_filter_(self):
        cases = [
            Case(("a eq True", {}), "hacker.a = '1'"),
            Case(("a eq 10", {}), "hacker.a = 10.0"),
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
            Case(("z eq 'a'", {}), wtoolzargsError),
            Case(("!", {}), wtoolzargsError),
            Case(("\n", {}), wtoolzargsError),
            Case(("\t", {}), wtoolzargsError),
            Case(("\r", {}), wtoolzargsError),
            Case(("  ", {}), wtoolzargsError),
            Case(("'a", {}), wtoolzargsError),
            Case(("a eq 'a' b eq 'b'", {}), wtoolzargsError),
            Case(("a eq a", {}), wtoolzargsError),
            Case(("a eq b eq 'c'", {}), wtoolzargsError),
            Case(("a eq (b eq 'c')", {}), wtoolzargsError),
            Case(("a", {}), wtoolzargsError),
            Case(("a and b", {}), wtoolzargsError),
        ]
        for e in cases:
            with self.subTest():
                e.assert_it(self, func_filter)

    def test_order(self):
        cases = [
            Case(("z asc", {"z": "a"}), "['hacker.a ASC']"),
            Case(("a asc", {}), "['hacker.a ASC']"),
            Case(("a desc", {}), "['hacker.a DESC']"),
            Case(("a", {}), "['hacker.a ASC']"),
            Case(
                ("a, b, c", {}),
                "['hacker.a ASC', 'hacker.b ASC', 'hacker.c ASC']",
            ),
            Case(("z", {}), wtoolzargsError),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func_order)


if __name__ == "__main__":
    unittest.main()
