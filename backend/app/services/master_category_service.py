from typing import List, Optional
from app.repositories.master_category_repository import MasterCategoryRepository
from app.schemas.master_category_schema import MasterCategory


class MasterCategoryService:
    def __init__(self, repo: MasterCategoryRepository):
        self.repo = repo

    def create_master_category(self, data) -> MasterCategory:
        category = self.repo.create_master_category(data)
        return MasterCategory.model_validate(category)

    def update_master_category(self, category_id: int, data) -> MasterCategory:
        category = self.repo.update_master_category(category_id, data)
        return MasterCategory.model_validate(category)

    def delete_master_category(self, category_id: int) -> None:
        self.repo.delete_master_category(category_id)

    def get_master_category(self, category_id: int) -> Optional[MasterCategory]:
        category = self.repo.get_master_category_by_id(category_id)
        if not category:
            return None
        return MasterCategory.model_validate(category)

    def list_master_categories(self) -> List[MasterCategory]:
        categories = self.repo.get_all_master_categories()
        return [MasterCategory.model_validate(c) for c in categories]
