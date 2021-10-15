from sqlalchemy import and_
from sqlalchemy import inspect
from sqlalchemy import not_
from sqlalchemy import or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.associationproxy import (
    ObjectAssociationProxyInstance as AssociationProxy,
)

from wtoolzargs.common import exceptions
from wtoolzargs.common import expressions
from wtoolzargs.filtering import tokentype

# TODO: Review types casting?

TT = tokentype.TokenType
InterpretError = exceptions.InterpretError


class Interpreter(expressions.Visitor):
    def __init__(self, query, model, expression, field_mapping, value_mapping):
        self.query = query
        self.model = model
        self.expression = expression
        self.field_mapping = field_mapping
        self.value_mapping = value_mapping

    def interpret(self):
        return self.query.filter(self.evaluate(self.expression))

    def visit_binary_expr(self, expr):
        if self.is_relationship_indentifier(expr):
            return self.relationship_evaluate(expr)

        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TT.EQUAL:
            field = self.field(left)
            return field == self.value(left, right)
        elif expr.operator.type == TT.NOT_EQUAL:
            field = self.field(left)
            return field != self.value(left, right)
        elif expr.operator.type == TT.GREATER_THAN:
            field = self.field(left)
            return field > self.value(left, right)
        elif expr.operator.type == TT.GREATER_THAN_OR_EQUAL:
            field = self.field(left)
            return field >= self.value(left, right)
        elif expr.operator.type == TT.LESS_THAN:
            field = self.field(left)
            return field < self.value(left, right)
        elif expr.operator.type == TT.LESS_THAN_OR_EQUAL:
            field = self.field(left)
            return field <= self.value(left, right)
        elif expr.operator.type == TT.LIKE:
            # NOTE: Can you find out what wrong here? :-)
            field = self.field(left)
            return field.like(self.value(left, right))

        elif expr.operator.type == TT.AND:
            return and_(left, right)
        elif expr.operator.type == TT.OR:
            return or_(left, right)
        return None

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_identifier_expr(self, expr):
        return expr.value

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TT.NOT:
            return not_(right)
        return None

    def evaluate(self, expr):
        return expr.accept(self)

    def field(self, name):
        model = self.model
        name_mapped = self.mapped_name(name)

        if not hasattr(model, name_mapped):
            raise InterpretError("No such field '{}' on model.".format(name))
        return getattr(model, name_mapped)

    def value(self, name, value):
        if self.value_mapping.has(name):
            return self.value_mapping.transform(name, value)
        return value

    def relationship_evaluate(self, expr):
        expr_tmp = expr.copy()
        field_mapping = self.field_mapping.copy()
        value_mapping = self.value_mapping.copy()
        name, rest = self.relationship_field_name(expr.left.value)
        expr_tmp.left.value = rest
        field = self.field(name)
        relationship_direction = self.relationship_direction(name)

        if isinstance(field, InstrumentedAttribute):
            model = field.mapper.class_
        elif isinstance(field, AssociationProxy):
            model = self.association_proxy_model(field)
        else:
            raise InterpretError(f"Can not determine model for field {name}")

        if relationship_direction == "MANYTOONE":
            return field.has(
                Interpreter(
                    self.query,
                    model,
                    expr_tmp,
                    field_mapping.move_to_next(name),
                    value_mapping.move_to_next(name),
                ).evaluate(expr_tmp)
            )
        elif relationship_direction == "ONETOMANY":
            return field.any(
                Interpreter(
                    self.query,
                    model,
                    expr_tmp,
                    field_mapping.move_to_next(name),
                    value_mapping.move_to_next(name),
                ).evaluate(expr_tmp)
            )
        else:
            raise InterpretError(
                f"Can not relationship direction for field {name}"
            )

    def mapped_name(self, name):
        if self.field_mapping.has(name):
            name_mapped = self.field_mapping.get(name)
        else:
            name_mapped = name
        return name_mapped

    def relationship_direction(self, name):
        name_mapped = self.mapped_name(name)
        relationships = inspect(self.model).relationships
        if name_mapped not in relationships:
            return None
        return relationships[name_mapped].direction.name

    @staticmethod
    def association_proxy_model(field):
        property_ = field.remote_attr.property
        for e in ("mapper", "parent"):
            if hasattr(property_, e):
                return getattr(property_, e).class_

    @staticmethod
    def relationship_field_name(s):
        name, *rest = s.split(".")
        return name, ".".join(rest)

    @staticmethod
    def is_relationship_indentifier(expr):
        return (
            isinstance(expr.left, expressions.Identifier)
            and "." in expr.left.value
        )
