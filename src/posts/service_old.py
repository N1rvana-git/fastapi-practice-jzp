#核心业务逻辑
from .schemas import Item,User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import schemas
from . import models
from .utils import get_password_hash
#它将接收 Pydantic 模型（来自 router）和数据库会话（来自 Depends），
# 然后把数据转换成数据库模型（models.py）并存入数据库。
async def create_item(db: AsyncSession, item: schemas.Item)-> models.ItemModel:
    db_item = models.ItemModel(
        name=item.name,
        price=item.price,
        is_offer=item.is_offer,
    )

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item