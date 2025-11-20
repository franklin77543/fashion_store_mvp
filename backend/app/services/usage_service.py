from typing import List, Optional
from app.repositories.usage_repository import UsageRepository
from app.schemas.usage_schema import UsageOut


class UsageService:
    def __init__(self, repo: UsageRepository):
        self.repo = repo

    def create_usage(self, data) -> UsageOut:
        usage = self.repo.create_usage(data)
        return UsageOut.model_validate(usage)

    def update_usage(self, usage_id: int, data) -> UsageOut:
        usage = self.repo.update_usage(usage_id, data)
        return UsageOut.model_validate(usage)

    def delete_usage(self, usage_id: int) -> None:
        self.repo.delete_usage(usage_id)

    def get_usage(self, usage_id: int) -> Optional[UsageOut]:
        usage = self.repo.get_usage_by_id(usage_id)
        if not usage:
            return None
        return UsageOut.model_validate(usage)

    def list_usages(self) -> List[UsageOut]:
        usages = self.repo.get_all_usages()
        return [UsageOut.model_validate(u) for u in usages]
