from typing import List, Optional
from app.repositories.season_repository import SeasonRepository
from app.schemas.season_schema import SeasonOut


class SeasonService:
    def __init__(self, repo: SeasonRepository):
        self.repo = repo

    def create_season(self, data) -> SeasonOut:
        season = self.repo.create_season(data)
        return SeasonOut.model_validate(season)

    def update_season(self, season_id: int, data) -> SeasonOut:
        season = self.repo.update_season(season_id, data)
        return SeasonOut.model_validate(season)

    def delete_season(self, season_id: int) -> None:
        self.repo.delete_season(season_id)

    def get_season(self, season_id: int) -> Optional[SeasonOut]:
        season = self.repo.get_season_by_id(season_id)
        if not season:
            return None
        return SeasonOut.model_validate(season)

    def list_seasons(self) -> List[SeasonOut]:
        seasons = self.repo.get_all_seasons()
        return [SeasonOut.model_validate(s) for s in seasons]
