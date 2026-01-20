#核心业务逻辑
from .schemas import ItemCreate, ItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import schemas
from . import models
from .utils import get_password_hash

async def create_item(db: AsyncSession, item: schemas.ItemCreate, owner_id: int) -> models.ItemModel:
    """创建物品，自动关联owner_id"""
    item_data = item.model_dump()
    db_item = models.ItemModel(**item_data, owner_id=owner_id)
    
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_item(db: AsyncSession, item_id: int) -> models.ItemModel | None:
    """根据 ID 查找物品"""
    result = await db.execute(select(models.ItemModel).where(models.ItemModel.id == item_id))
    return result.scalars().one_or_none()

async def delete_item(db: AsyncSession, item: models.ItemModel):
    """删除物品"""
    await db.delete(item)
    await db.commit()

async def update_item(db: AsyncSession, db_item: models.ItemModel, item_update: schemas.ItemUpdate):
    """更新物品逻辑"""
    # 只提取用户真正传了的字段
    update_data = item_update.model_dump(exclude_unset=True)
    
    # 遍历字典，更新数据库对象
    for key, value in update_data.items():
        setattr(db_item, key, value)

    # 提交保存
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
