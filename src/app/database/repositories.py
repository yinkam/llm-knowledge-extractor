from fastapi import Depends, HTTPException
from sqlalchemy import select, or_, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.app.database.connection import get_async_db
from src.app.domain.entities import AnalysisEntity
from src.app.interfaces import RepositoryInterface
from src.app.database.models import Analysis


class AnalysisRepository(RepositoryInterface):

    def __init__(self, db: Annotated[AsyncSession, Depends(get_async_db)]):
        self.db = db

    async def add(self, data: AnalysisEntity) -> Analysis:
        """Creates a new analysis record."""
        try:
            db_data = data.model_dump(exclude={"id"})

            db_model = Analysis(**db_data)

            self.db.add(db_model)

            await self.db.commit()
            await self.db.refresh(db_model)

            return db_model

        except SQLAlchemyError:
            await self.db.rollback()
            print("ERROR: Database error during analysis creation.")
            raise HTTPException(status_code=500, detail="Database error occurred while creating analysis.")

    async def search_by_topic_or_keyword(self, query: str) -> Sequence[Analysis]:
        """
        Search for analyses by matching the query against the 'topics' OR the 'keywords'.
        """
        try:
            stmt = (
                select(Analysis)
                .filter(
                    or_(
                        Analysis.topics.contains(query),
                        Analysis.keywords.contains(query),
                    )
                )
            )

            result = await self.db.execute(stmt)
            analyses = result.scalars().all()

            return analyses

        except SQLAlchemyError:
            print("ERROR: Database error during analysis search.")
            raise HTTPException(status_code=500, detail="Database error occurred during search.")