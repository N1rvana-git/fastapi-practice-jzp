from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException,status

from src.posts.dependencies import get_db_session

async def ping_database(db: AsyncSession = Depends(get_db_session)):
    try:
        await db.execute(select(1))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    return None