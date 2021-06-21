import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative

from wtoolzargs.common import exceptions
from wtoolzargs.ordering import interpreter
from wtoolzargs.ordering import parser
from wtoolzargs.ordering import scanner

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


def func(source):
    res = interpreter.Interpreter(Hacker, parse(tokens(source))).interpret()
    return str(
        [str(e.compile(compile_kwargs={"literal_binds": True})) for e in res]
    )


class TestFilteringInterpreter(unittest.TestCase):
    def test_interpret(self):
        cases = [
            Case("a asc", "['hacker.a ASC']"),
            Case("a desc", "['hacker.a DESC']"),
            Case("a", "['hacker.a ASC']"),
            Case(
                "a, b, c", "['hacker.a ASC', 'hacker.b ASC', 'hacker.c ASC']"
            ),
            Case("z", InterpretError),
        ]
        for e in cases:
            with self.subTest():
                e.assert_it(self, func)


if __name__ == "__main__":
    unittest.main()
