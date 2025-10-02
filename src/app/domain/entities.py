from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TextEntity(BaseModel):
    content: str

class AnalysisEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    text_input: str
    summary: str
    title: Optional[str]
    topics: List[str]
    sentiment: str
    keywords: List[str]
    confidence_score: Optional[float] = None

class Analyses(BaseModel):
    analyses: List[AnalysisEntity]