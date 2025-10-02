from abc import ABC, abstractmethod
from typing import List

from src.app.domain.entities import AnalysisEntity


class LLMClientInterface(ABC):

    @abstractmethod
    async def analyze(self, text: str) -> dict:
        raise NotImplementedError


class RepositoryInterface(ABC):

    @abstractmethod
    async def add(self, analysis: AnalysisEntity) -> AnalysisEntity:
        raise NotImplementedError

    @abstractmethod
    async def search_by_topic_or_keyword(self, query: str) -> List[AnalysisEntity]:
        raise NotImplementedError

class KeywordExtractorInterface(ABC):

    @abstractmethod
    def extract(self, text: str) -> List[str]:
        raise NotImplementedError
