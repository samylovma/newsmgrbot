__all__ = (
    "registry",
    "News",
    "Source",
    "User",
    "user_source",
)

import sqlalchemy.orm
from advanced_alchemy.base import orm_registry

from ._news import News
from ._source import Source
from ._user import User
from ._user_source import user_source

registry: sqlalchemy.orm.registry = orm_registry
