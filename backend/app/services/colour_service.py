
from typing import List, Optional
from app.repositories.colour_repository import ColourRepository
from app.schemas.colour_schema import ColourOut


class ColourService:
    def __init__(self, repo: ColourRepository):
        self.repo = repo

    def list_colours(self) -> List[ColourOut]:
        colours = self.repo.get_all_colours()
        return [ColourOut.model_validate(c) for c in colours]

    def get_colour(self, colour_id: int) -> Optional[ColourOut]:
        colour = self.repo.get_colour_by_id(colour_id)
        if not colour:
            return None
        return ColourOut.model_validate(colour)

    def create_colour(self, data) -> ColourOut:
        colour = self.repo.create_colour(data)
        return ColourOut.model_validate(colour)

    def update_colour(self, colour_id: int, data) -> ColourOut:
        colour = self.repo.update_colour(colour_id, data)
        return ColourOut.model_validate(colour)

    def delete_colour(self, colour_id: int) -> None:
        self.repo.delete_colour(colour_id)
