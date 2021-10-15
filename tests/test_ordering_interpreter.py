import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session


from wtoolzargs.common import exceptions
from wtoolzargs.common import mapping
from wtoolzargs.ordering import interpreter
from wtoolzargs.ordering import parser
from wtoolzargs.ordering import scanner

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
    ).interpret()
    return str(res).replace("\n", "")


class FilteringInterpreter(unittest.TestCase):
    def test_interpret(self):

        should_template = (
            "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
            "hacker.b AS hacker_b, hacker.c AS hacker_c, "
            "hacker.d AS hacker_d, hacker.e AS hacker_e FROM "
            "hacker ORDER BY {order_by}"
        )

        cases = [
            Case(
                ("z asc", {"z": "a"}),
                should_template.format(order_by="hacker.a ASC"),
            ),
            Case(
                ("a asc", {}), should_template.format(order_by="hacker.a ASC")
            ),
            Case(
                ("a desc", {}),
                should_template.format(order_by="hacker.a DESC"),
            ),
            Case(("a", {}), should_template.format(order_by="hacker.a ASC")),
            Case(
                ("a, b, c", {}),
                should_template.format(
                    order_by="hacker.a ASC, hacker.b ASC, hacker.c ASC"
                ),
            ),
            Case(("z", {}), InterpretError),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main(module="test_ordering_scanner")
