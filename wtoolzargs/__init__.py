"""
wtoolzargs contains core filtering and ordering logic for web applications
"""

# TODO: Review private vs public methods.
# TODO: Add typing
# TODO: Update docstring to google style and also add sphinx docs.
# TODO: Test relationship stuff with mapping
# TODO: TRY code with relationship between filter and order.
# TODO: Import statments
# TODO: Review motation vs not and the naming accordingly.
# TODO: __repr__
# TODO: Stricter args checking for filter_ and order, since if arity
#       is wrong it explodes weird!
# TODO: Refactor value mapping. Is similar to name.

from wtoolzargs import version
from wtoolzargs.filtering import filter_
from wtoolzargs.ordering import order
from wtoolzargs.common.exceptions import wtoolzargsError

__author__ = "Eric Matti"
__version__ = version.__version__
__all__ = [filter_, order, wtoolzargsError]
