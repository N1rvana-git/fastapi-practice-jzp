from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import AsyncSessionLocal
# 这是一个可复用的依赖项，用于处理通用的分页和搜索查询
# 任何需要分页的路由都可以
def common_parameters(
        q:Union[str,None]=None,
        skip:int=0,
        limit:int=100
):
    return{"q":q,"skip":skip,"limit":limit}

#数据库会话依赖项，管理“生命周期”
async def get_db_session()->AsyncSession:
    async with AsyncSessionLocal() as db_session:
        try:
            # "yield" 关键字是关键
            #    它会把 session "注入" 到路由函数中
            #    并在这里暂停，直到路由函数执行完毕
            yield db_session
        except Exception :#异常回滚
            await db_session.rollback()
            raise
        finally:#关闭
            await db_session.close()