import unittest

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext import declarative
from sqlalchemy.orm.scoping import scoped_session

import wtoolzargs

import common

# TODO: Maybe add test where queries happen against in-memory database.

Case = common.Case


DBSession = scoped_session(sessionmaker())


class _Base(object):
    query = DBSession.query_property()


Base = declarative.declarative_base(cls=_Base)

wtoolzargsError = wtoolzargs.wtoolzargsError


class GrandParent(Base):
    __tablename__ = "grandparent"
    id = Column(Integer, primary_key=True)
    a = Column(String)
    b = Column(String)
    c = Column(String)

    children = relationship("Parent", back_populates="parent")


class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    a = Column(String)
    b = Column(String)
    c = Column(String)

    parent_id = Column(Integer, ForeignKey("grandparent.id"))

    hackers = relationship("Hacker", back_populates="parent")
    parent = relationship("GrandParent", back_populates="children")


class Hacker(Base):
    __tablename__ = "hacker"
    id = Column(Integer, primary_key=True)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    e = Column(String)

    parent_id = Column(Integer, ForeignKey("parent.id"))

    parent = relationship("Parent", back_populates="hackers")


def func_filter(args):
    source, field_mapping, value_mapping = args
    res = wtoolzargs.filter_(
        Hacker.query, Hacker, source, field_mapping, value_mapping
    )
    return str(
        res.statement.compile(compile_kwargs={"literal_binds": True})
    ).replace("\n", "")


def func_order(args):
    source, field_mapping = args
    res = wtoolzargs.order(Hacker.query, Hacker, source, field_mapping)
    return str(res).replace("\n", "")


class WToolzFilter(unittest.TestCase):
    def test_filter_(self):
        should_template = (
            "SELECT hacker.id, hacker.a, hacker.b, "
            "hacker.c, hacker.d, hacker.e, hacker.parent_id "
            "FROM hacker WHERE {where_clause}"
        )

        cases = [
            Case(
                ("a eq 'a'", {}, {}),
                should_template.format(where_clause="hacker.a = 'a'"),
            ),
            Case(
                ("a eq 'a'", {"z": "a"}, {}),
                should_template.format(where_clause="hacker.a = 'a'"),
            ),
            Case(
                ("a eq True", {}, {}),
                should_template.format(where_clause="hacker.a = '1'"),
            ),
            Case(
                ("a eq 10", {}, {}),
                should_template.format(where_clause="hacker.a = 10.0"),
            ),
            Case(
                ("a ne 10", {}, {}),
                should_template.format(where_clause="hacker.a != 10.0"),
            ),
            Case(
                ("a gt 10", {}, {}),
                should_template.format(where_clause="hacker.a > 10.0"),
            ),
            Case(
                ("a ge 10", {}, {}),
                should_template.format(where_clause="hacker.a >= 10.0"),
            ),
            Case(
                ("a lt 10", {}, {}),
                should_template.format(where_clause="hacker.a < 10.0"),
            ),
            Case(
                ("a le 10", {}, {}),
                should_template.format(where_clause="hacker.a <= 10.0"),
            ),
            Case(
                ("a eq not 10", {}, {}),
                should_template.format(where_clause="hacker.a = (NOT 10.0)"),
            ),
            Case(
                ("a eq 10 and b eq 10", {}, {}),
                should_template.format(
                    where_clause="hacker.a = 10.0 AND hacker.b = 10.0"
                ),
            ),
            Case(
                ("a eq 10 or b eq 10", {}, {}),
                should_template.format(
                    where_clause="hacker.a = 10.0 OR hacker.b = 10.0"
                ),
            ),
            Case(
                ("(a eq 10 or b eq 10) and c eq 10", {}, {}),
                should_template.format(
                    where_clause=(
                        "(hacker.a = 10.0 OR hacker.b = 10.0) AND "
                        "hacker.c = 10.0"
                    )
                ),
            ),
            Case(
                ("a eq 'a'", {}, {}),
                should_template.format(where_clause="hacker.a = 'a'"),
            ),
            Case(
                ("a eq 'a' and b eq 'b'", {}, {}),
                should_template.format(
                    where_clause="hacker.a = 'a' AND hacker.b = 'b'"
                ),
            ),
            Case(
                ("not a eq not 'b'", {}, {}),
                should_template.format(where_clause="hacker.a != (NOT 'b')"),
            ),
            Case(
                ("not (a eq 'a' and b eq 'b')", {}, {}),
                should_template.format(
                    where_clause="NOT (hacker.a = 'a' AND hacker.b = 'b')"
                ),
            ),
            Case(
                ("(a eq 'a' or b eq 'b') and c eq 'c'", {}, {}),
                should_template.format(
                    where_clause=(
                        "(hacker.a = 'a' OR hacker.b = 'b') AND "
                        "hacker.c = 'c'"
                    )
                ),
            ),
            Case(
                ("a eq 'a' or b eq 'b' and d eq 'd' or e eq 'e'", {}, {}),
                should_template.format(
                    where_clause=(
                        "hacker.a = 'a' OR hacker.b = 'b' AND "
                        "hacker.d = 'd' OR hacker.e = 'e'"
                    )
                ),
            ),
            Case(("z eq 'a'", {}, {}), wtoolzargsError),
            Case(("!", {}, {}), wtoolzargsError),
            Case(("\n", {}, {}), wtoolzargsError),
            Case(("\t", {}, {}), wtoolzargsError),
            Case(("\r", {}, {}), wtoolzargsError),
            Case(("  ", {}, {}), wtoolzargsError),
            Case(("'a", {}, {}), wtoolzargsError),
            Case(("a eq 'a' b eq 'b'", {}, {}), wtoolzargsError),
            Case(("a eq a", {}, {}), wtoolzargsError),
            Case(("a eq b eq 'c'", {}, {}), wtoolzargsError),
            Case(("a eq (b eq 'c')", {}, {}), wtoolzargsError),
            Case(("a", {}, {}), wtoolzargsError),
            Case(("a and b", {}, {}), wtoolzargsError),
            Case(
                ("parent.parent.a eq True", {}, {}),
                should_template.format(
                    where_clause=(
                        (
                            "EXISTS (SELECT 1 FROM parent WHERE "
                            "parent.id = hacker.parent_id AND "
                            "(EXISTS (SELECT 1 FROM grandparent WHERE "
                            "grandparent.id = parent.parent_id AND "
                            "grandparent.a = '1')))"
                        )
                    )
                ),
            ),
            Case(
                ("parent.a eq True", {}, {}),
                should_template.format(
                    where_clause=(
                        "EXISTS (SELECT 1 FROM parent WHERE "
                        "parent.id = hacker.parent_id AND parent.a = '1')"
                    )
                ),
            ),
            Case(
                ("yal.more eq True", {"yal.more": "parent.a"}, {}),
                should_template.format(
                    where_clause=(
                        "EXISTS (SELECT 1 FROM parent WHERE "
                        "parent.id = hacker.parent_id AND parent.a = '1')"
                    )
                ),
            ),
            Case(
                ("z eq 'a'", {"z": "a"}, {"z": ("a", lambda x: x.upper())}),
                should_template.format(where_clause="hacker.a = 'A'"),
            ),
            Case(
                (
                    "yal.more eq True",
                    {"yal.more": "parent.a"},
                    {"yal.more": ("parent.a", lambda x: x.upper())},
                ),
                should_template.format(
                    where_clause=(
                        "EXISTS (SELECT 1 FROM parent WHERE "
                        "parent.id = hacker.parent_id AND parent.a = '1')"
                    )
                ),
            ),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func_filter)

    def test_order(self):
        should_template = (
            "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
            "hacker.b AS hacker_b, hacker.c AS hacker_c, "
            "hacker.d AS hacker_d, hacker.e AS hacker_e, "
            "hacker.parent_id AS hacker_parent_id FROM "
            "hacker ORDER BY {order_by}"
        )

        cases = [
            Case(
                ("parent.a asc", {}),
                (
                    "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
                    "hacker.b AS hacker_b, hacker.c AS hacker_c, "
                    "hacker.d AS hacker_d, hacker.e AS hacker_e, "
                    "hacker.parent_id AS hacker_parent_id "
                    "FROM hacker JOIN parent ON parent.id = hacker.parent_id "
                    "ORDER BY parent.a ASC"
                ),
            ),
            Case(
                ("a asc", {}),
                (
                    "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
                    "hacker.b AS hacker_b, hacker.c AS hacker_c, "
                    "hacker.d AS hacker_d, hacker.e AS hacker_e, "
                    "hacker.parent_id AS hacker_parent_id FROM "
                    "hacker ORDER BY hacker.a ASC"
                ),
            ),
            Case(
                ("a asc, parent.b desc", {}),
                (
                    "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
                    "hacker.b AS hacker_b, hacker.c AS hacker_c, "
                    "hacker.d AS hacker_d, hacker.e AS hacker_e, "
                    "hacker.parent_id AS hacker_parent_id FROM "
                    "hacker JOIN parent ON parent.id = hacker.parent_id "
                    "ORDER BY hacker.a ASC, parent.b DESC"
                ),
            ),
            Case(
                ("z asc", {"z": "a"}),
                (
                    "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
                    "hacker.b AS hacker_b, hacker.c AS hacker_c, "
                    "hacker.d AS hacker_d, hacker.e AS hacker_e, "
                    "hacker.parent_id AS hacker_parent_id FROM "
                    "hacker ORDER BY hacker.a ASC"
                ),
            ),
            Case(
                ("a desc", {}),
                should_template.format(order_by="hacker.a DESC"),
            ),
            Case(
                ("a, b, c desc", {}),
                should_template.format(
                    order_by="hacker.a ASC, hacker.b ASC, hacker.c DESC"
                ),
            ),
            Case(("z", {}), wtoolzargsError),
            Case(
                (
                    "randomRelationship.z asc",
                    {"randomRelationship.z": "parent.a"},
                ),
                (
                    "SELECT hacker.id AS hacker_id, hacker.a AS hacker_a, "
                    "hacker.b AS hacker_b, hacker.c AS hacker_c, "
                    "hacker.d AS hacker_d, hacker.e AS hacker_e, "
                    "hacker.parent_id AS hacker_parent_id "
                    "FROM hacker JOIN parent ON parent.id = hacker.parent_id "
                    "ORDER BY parent.a ASC"
                ),
            ),
        ]

        for e in cases:
            with self.subTest():
                e.assert_it(self, func_order)


if __name__ == "__main__":
    unittest.main(module="test_wtoolzargs")
