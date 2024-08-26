from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from newsmgrbot.models import Source


class SourceRepository(SQLAlchemyAsyncRepository[Source]):
    model_type = Source


class SourceService(SQLAlchemyAsyncRepositoryService[Source]):
    repository_type = SourceRepository
