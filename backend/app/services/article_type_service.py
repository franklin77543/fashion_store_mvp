from typing import List, Optional
from app.repositories.article_type_repository import ArticleTypeRepository
from app.schemas.article_type_schema import ArticleTypeOut


class ArticleTypeService:
    def __init__(self, repo: ArticleTypeRepository):
        self.repo = repo

    def create_article_type(self, data) -> ArticleTypeOut:
        article_type = self.repo.create_article_type(data)
        return ArticleTypeOut.model_validate(article_type)

    def update_article_type(self, article_type_id: int, data) -> ArticleTypeOut:
        article_type = self.repo.update_article_type(article_type_id, data)
        return ArticleTypeOut.model_validate(article_type)

    def delete_article_type(self, article_type_id: int) -> None:
        self.repo.delete_article_type(article_type_id)

    def get_article_type(self, article_type_id: int) -> Optional[ArticleTypeOut]:
        article_type = self.repo.get_article_type_by_id(article_type_id)
        if not article_type:
            return None
        return ArticleTypeOut.model_validate(article_type)

    def list_article_types(self) -> List[ArticleTypeOut]:
        article_types = self.repo.get_all_article_types()
        return [ArticleTypeOut.model_validate(at) for at in article_types]
