from pydantic import BaseModel

from src.app.domain.entities import AnalysisEntity, Analyses


class TextInput(BaseModel):
    content: str


class AnalysisResponse(AnalysisEntity):
    pass


class SearchResponse(Analyses):
    pass