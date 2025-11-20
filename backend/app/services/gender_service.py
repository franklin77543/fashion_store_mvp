
from typing import List, Optional
from app.repositories.gender_repository import GenderRepository
from app.schemas.gender_schema import Gender


class GenderService:
    def __init__(self, repo: GenderRepository):
        self.repo = repo

    def list_genders(self) -> List[Gender]:
        genders = self.repo.get_all_genders()
        return [Gender.model_validate(g) for g in genders]

    def get_gender(self, gender_id: int) -> Optional[Gender]:
        gender = self.repo.get_gender_by_id(gender_id)
        if not gender:
            return None
        return Gender.model_validate(gender)

    def create_gender(self, data) -> Gender:
        gender = self.repo.create_gender(data)
        return Gender.model_validate(gender)

    def update_gender(self, gender_id: int, data) -> Gender:
        gender = self.repo.update_gender(gender_id, data)
        return Gender.model_validate(gender)

    def delete_gender(self, gender_id: int) -> None:
        self.repo.delete_gender(gender_id)
