import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm import sessionmaker

from wtoolzargs.common import exceptions
from wtoolzargs.common import mapping
from wtoolzargs.filtering import interpreter
from wtoolzargs.filtering import parser
from wtoolzargs.filtering import scanner

import common


DBSession = scoped_session(sessionmaker())


class _Base(object):
    query = DBSession.query_property()


Base = declarative.declarative_base(cls=_Base)

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
        Hacker.query,
        Hacker,
        parse(tokens(source)),
        mapping.Mappings.create_from_dict(field_mapping),
        mapping.Mappings.create_from_dict({}),
    ).interpret()
    return str(
        res.statement.compile(compile_kwargs={"literal_binds": True})
    ).replace("\n", "")


class FilteringInterpreter(unittest.TestCase):
    def test_interpret(self):
        should_template = (
            "SELECT hacker.id, hacker.a, hacker.b, "
            "hacker.c, hacker.d, hacker.e FROM "
            "hacker WHERE {where_clause}"
        )

        cases = [
            Case(
                ("a eq True", {}),
                should_template.format(where_clause="hacker.a = '1'"),
            ),
            Case(
                ("a like '%some%'", {}),
                should_template.format(where_clause="hacker.a LIKE '%some%'"),
            ),
            Case(
                ("a eq 10", {}),
                should_template.format(where_clause="hacker.a = 10.0"),
            ),
            Case(
                ("a eq -10", {}),
                should_template.format(where_clause="hacker.a = -10.0"),
            ),
            Case(
                ("a ne 10", {}),
                should_template.format(where_clause="hacker.a != 10.0"),
            ),
            Case(
                ("a gt 10", {}),
                should_template.format(where_clause="hacker.a > 10.0"),
            ),
            Case(
                ("a ge 10", {}),
                should_template.format(where_clause="hacker.a >= 10.0"),
            ),
            Case(
                ("a lt 10", {}),
                should_template.format(where_clause="hacker.a < 10.0"),
            ),
            Case(
                ("a le 10", {}),
                should_template.format(where_clause="hacker.a <= 10.0"),
            ),
            Case(
                ("a eq not 10", {}),
                should_template.format(where_clause="hacker.a = (NOT 10.0)"),
            ),
            Case(
                ("a eq 10 and b eq 10", {}),
                should_template.format(
                    where_clause="hacker.a = 10.0 AND hacker.b = 10.0"
                ),
            ),
            Case(
                ("a eq 10 or b eq 10", {}),
                should_template.format(
                    where_clause="hacker.a = 10.0 OR hacker.b = 10.0"
                ),
            ),
            Case(
                ("(a eq 10 or b eq 10) and c eq 10", {}),
                should_template.format(
                    where_clause=(
                        "(hacker.a = 10.0 OR hacker.b = 10.0) AND "
                        "hacker.c = 10.0"
                    )
                ),
            ),
            Case(
                ("a eq 'a'", {}),
                should_template.format(where_clause="hacker.a = 'a'"),
            ),
            Case(
                ("a eq 'a' and b eq 'b'", {}),
                should_template.format(
                    where_clause="hacker.a = 'a' AND hacker.b = 'b'"
                ),
            ),
            Case(
                ("not a eq not 'b'", {}),
                should_template.format(where_clause="hacker.a != (NOT 'b')"),
            ),
            Case(
                ("not (a eq 'a' and b eq 'b')", {}),
                should_template.format(
                    where_clause="NOT (hacker.a = 'a' AND hacker.b = 'b')"
                ),
            ),
            Case(
                ("(a eq 'a' or b eq 'b') and c eq 'c'", {}),
                should_template.format(
                    where_clause=(
                        "(hacker.a = 'a' OR hacker.b = 'b') AND "
                        "hacker.c = 'c'"
                    )
                ),
            ),
            Case(
                ("a eq 'a' or b eq 'b' and d eq 'd' or e eq 'e'", {}),
                should_template.format(
                    where_clause=(
                        "hacker.a = 'a' OR hacker.b = 'b' AND "
                        "hacker.d = 'd' OR hacker.e = 'e'"
                    )
                ),
            ),
            Case(
                ("z eq 'a'", {"z": "a"}),
                should_template.format(where_clause="hacker.a = 'a'"),
            ),
            Case(("z eq 'a'", {}), InterpretError),
        ]
        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main(module="test_filtering_interpreter")
