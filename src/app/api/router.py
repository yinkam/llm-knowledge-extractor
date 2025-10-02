from fastapi import APIRouter,Depends, Query, HTTPException
from typing import Annotated

from src.app.domain.entities import TextEntity
from src.app.domain.use_cases import AnalyzeTextUseCase, SearchAnalysesUseCase
from src.app.api.models import AnalysisResponse, TextInput, SearchResponse

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(text_input: TextInput, use_case: Annotated[AnalyzeTextUseCase, Depends()]):
    try:
        text_data = TextEntity(**text_input.model_dump())
        analysis = await use_case.execute(text_data)
        return AnalysisResponse(**analysis.model_dump())
    except HTTPException as e:
        raise e

@router.get("/search", response_model=SearchResponse)
async def search(use_case: Annotated[SearchAnalysesUseCase, Depends()], topic: str = Query()):
    try:
        return await use_case.execute(topic)
    except HTTPException as e:
        raise e

