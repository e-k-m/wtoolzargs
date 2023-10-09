from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.associationproxy import (
    ObjectAssociationProxyInstance as AssociationProxy,
)


from wtoolzargs.common import exceptions
from wtoolzargs.common import expressions
from wtoolzargs.ordering import tokentype

TT = tokentype.TokenType
InterpretError = exceptions.InterpretError


class Interpreter(expressions.Visitor):
    def __init__(self, query, model, expression, field_mapping):
        self.query = query
        self.model = model
        self.expression = expression
        self.field_mapping = field_mapping

    def interpret(self):
        order_by_args = self.evaluate(self.expression)
        if not isinstance(order_by_args, list):
            return self.query.order_by(order_by_args)
        return self.query.order_by(*order_by_args)

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        # HACK: Apply a better solution.
        if expr.operator.type == TT.SEPERATOR:
            if isinstance(left, list):
                left.append(right)
                return left
            if isinstance(right, list):
                right.append(left)
                return right
            return [left, right]

        return None

    def visit_grouping_expr(self, expr):
        pass

    def visit_literal_expr(self, expr):
        pass

    def visit_identifier_expr(self, expr):
        return expr.value

    def visit_unary_expr(self, expr):
        if self.is_relationship_indentifier(expr):
            return self.relationship_evaluate(expr)

        right = self.evaluate(expr.right)

        if expr.operator.type == TT.ASC:
            field = self.field(right)
            return getattr(field, "asc")()

        if expr.operator.type == TT.DESC:
            field = self.field(right)
            return getattr(field, "desc")()

        return None

    def evaluate(self, expr):
        return expr.accept(self)

    def field(self, name):
        model = self.model
        if self.field_mapping.has(name):
            name_mapped = self.field_mapping.get(name)
        else:
            name_mapped = name
        if not hasattr(model, name_mapped):
            raise InterpretError("No such field '{}' on model.".format(name))
        return getattr(model, name_mapped)

    def relationship_evaluate(self, expr):
        expr_tmp = expr.copy()
        field_mapping = self.field_mapping.copy()
        name, rest = self.relationship_field_name(expr.right.value)
        expr_tmp.right.value = rest
        field = self.field(name)

        if isinstance(field, InstrumentedAttribute):
            model = field.mapper.class_
        elif isinstance(field, AssociationProxy):
            model = self.association_proxy_model(field)
        else:
            raise InterpretError(f"Can not determine model for field {name}")

        self.query = self.query.join(model)
        return Interpreter(
            self.query, model, expr_tmp, field_mapping.move_to_next(name)
        ).evaluate(expr_tmp)

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
            isinstance(expr.right, expressions.Identifier)
            and "." in expr.right.value
        )
