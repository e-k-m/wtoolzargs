from wtoolzargs.common import mapping
from wtoolzargs.ordering import interpreter
from wtoolzargs.ordering import parser
from wtoolzargs.ordering import scanner


def order(query, model, source, field_mapping={}):
    """
    Returns the sqlalchemy query with order_by applied for
    models order expression.

    Paramaters
    ----------
    query: sqlalchemy query
      sqlalchemy query.
    model: sqlalchemy model
      sqlalchemy model.
    source: str
      Order DSL (see grammar in details).
    field_mapping: dict
      Optional field mapping. Maps field names in source to field names of
      model. Dict of string keys and string values. Example:
      {'payloadProperty': 'orm_property'}.

    Returns
    -------
    _: [sqlalchemy.sql.elements.XYExpression]
      A thing that can be *passed to query.order_by.

    Raises
    ------
    _: wtoolzargs.wtoolzargsError

    Details
    -------

    Order DSL grammar is:

    expression  -> orderings ;
    orderings   -> order ("," order )* ;
    order       -> identifier ("asc" | "desc")? ;
    identifier  -> IDENTIFIER ;

    And some productions:

    a asc
    a desc
    a desc, b desc

    Please note, it supports relationship identifiers like
    parent.a asc.
    """

    tokens = scanner.Scanner(source).scan()
    expression = parser.Parser(tokens).parse()
    field_mapping = mapping.Mappings.create_from_dict(field_mapping)
    return interpreter.Interpreter(
        query, model, expression, field_mapping
    ).interpret()
