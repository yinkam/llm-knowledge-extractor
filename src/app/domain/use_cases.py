from typing import Annotated, List

from fastapi import Depends, HTTPException

from src.app.database.repositories import AnalysisRepository
from src.app.domain.entities import TextEntity, AnalysisEntity, Analyses
from src.app.interfaces import LLMClientInterface, RepositoryInterface, KeywordExtractorInterface
from src.app.domain.keyword_extractor import KeywordExtractor
from src.app.llm.openai_client import OpenAIClient

# Naive confidence score based on model success
MODEL_CONFIDENCE_MAP = {
    "llm_success": 0.90,
    "llm_failure": 0.50
}

class AnalyzeTextUseCase:
    def __init__(self,
        llm: Annotated[LLMClientInterface, Depends(OpenAIClient)],
        repo: Annotated[RepositoryInterface, Depends(AnalysisRepository)],
        keyword_extractor: Annotated[KeywordExtractorInterface, Depends(KeywordExtractor)]
    ):
        self.llm = llm
        self.repo = repo
        self.keyword_extractor = keyword_extractor

    async def execute(self, text_input: TextEntity) -> AnalysisEntity:
        if not text_input.content.strip():
            raise HTTPException(400)

        try:
            llm_result = await self.llm.analyze(text_input.content)
            confidence_score = MODEL_CONFIDENCE_MAP["llm_success"]
        except (Exception) as e:
            print(f"ERROR: LLM analysis failed: {e}")
            confidence_score = MODEL_CONFIDENCE_MAP["llm_failure"]
            raise HTTPException(status_code=500, detail="LLM analysis failed to complete or structure data correctly.")

        keywords = self.keyword_extractor.extract(text_input.content)

        analysis = AnalysisEntity(
            text_input=text_input.content,
            summary=llm_result.get("summary", "LLM summary not available."),
            title=llm_result.get("title"),
            topics=llm_result.get("topics", []),
            sentiment=llm_result.get("sentiment", "unknown"),
            keywords=keywords,
            confidence_score=confidence_score
        )

        db_analysis = await self.repo.add(analysis)
        return AnalysisEntity.model_validate(db_analysis)



class SearchAnalysesUseCase:

    def __init__(self, repo: Annotated[RepositoryInterface, Depends(AnalysisRepository)]):
        self.repo = repo

    async def execute(self, query: str) -> Analyses:
        db_analyses = await self.repo.search_by_topic_or_keyword(query)

        analyses = [AnalysisEntity.model_validate(a) for a in db_analyses]
        return Analyses(analyses=analyses)