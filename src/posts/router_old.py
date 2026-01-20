#处理http请求
from fastapi import APIRouter, Depends, params, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .schemas import Item,User,UpdateItemResponse
from . import service
from .dependencies import common_parameters, get_db_session
from typing import Union,List,Optional
from . import schemas
from . import models
from src.users import service as user_service
from src.users import schemas as user_schemas

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/", response_model=schemas.CreateItemWithUserResponse)
async def create_new_item(
    payload: Union[schemas.Item, schemas.CreateItemWithUserRequest],
    db: AsyncSession = Depends(get_db_session)
):
    """
    在数据库中创建一个新物品，可选地同时创建用户。
    - 接受单个 Item 模型
    - 或接受 {item: Item, user: User} 组合
    """
    # 判断负载类型
    if isinstance(payload, schemas.CreateItemWithUserRequest):
        # 组合模式：先创建用户（若提供），再创建物品
        username = None
        if payload.user:
            # 转换为 UserCreate 模型（补充必填字段 age）
            user_create = user_schemas.UserCreate(
                username=payload.user.username,
                email=payload.user.email,
                password=payload.user.password,
                age=0  # 默认值，满足 UserModel.age 非空约束
            )
            db_user = await user_service.create_user(db=db, user=user_create)
            username = db_user.username
        db_item = await service.create_item(db=db, item=payload.item)
        return schemas.CreateItemWithUserResponse(
            name=db_item.name,
            price=db_item.price,
            is_offer=db_item.is_offer,
            username=username
        )
    else:
        # 单一 Item 模式
        db_item = await service.create_item(db=db, item=payload)
        return schemas.CreateItemWithUserResponse(
            name=db_item.name,
            price=db_item.price,
            is_offer=db_item.is_offer,
            username=None
        )

@router.get("/", response_model=List[schemas.Item])
async def read_items_from_db(skip:int=Query(0,ge=0),
                             limit:int=Query(100,ge=10,le=200),
                             is_offer_filter:Optional[bool] = None,
                             db:AsyncSession=Depends(get_db_session)):
    #动态构建
    query = select(models.ItemModel)#基础查询
    if is_offer_filter is not None:
        query = query.where(models.ItemModel.is_offer == is_offer_filter)
    query = query.offset(skip).limit(limit)
    result=await db.execute(
        select(models.ItemModel).offset(skip).limit(limit)
    )
    result=await db.execute(query)
    items=result.scalars().all()
    return items