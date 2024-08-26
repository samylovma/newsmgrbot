from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from newsmgrbot.models import News


class NewsRepository(SQLAlchemyAsyncRepository[News]):
    model_type = News


class NewsService(SQLAlchemyAsyncRepositoryService[News]):
    repository_type = NewsRepository
