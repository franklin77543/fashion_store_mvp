from typing import List, Optional
from app.repositories.sub_category_repository import SubCategoryRepository
from app.schemas.sub_category_schema import SubCategoryOut


class SubCategoryService:
    def __init__(self, repo: SubCategoryRepository):
        self.repo = repo

    def create_sub_category(self, data) -> SubCategoryOut:
        sub_category = self.repo.create_sub_category(data)
        return SubCategoryOut.model_validate(sub_category)

    def update_sub_category(self, sub_category_id: int, data) -> SubCategoryOut:
        sub_category = self.repo.update_sub_category(sub_category_id, data)
        return SubCategoryOut.model_validate(sub_category)

    def delete_sub_category(self, sub_category_id: int) -> None:
        self.repo.delete_sub_category(sub_category_id)

    def get_sub_category(self, sub_category_id: int) -> Optional[SubCategoryOut]:
        sub_category = self.repo.get_sub_category_by_id(sub_category_id)
        if not sub_category:
            return None
        return SubCategoryOut.model_validate(sub_category)

    def list_sub_categories(self) -> List[SubCategoryOut]:
        sub_categories = self.repo.get_all_sub_categories()
        return [SubCategoryOut.model_validate(sc) for sc in sub_categories]
