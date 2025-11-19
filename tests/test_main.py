from typing import AsyncGenerator
import pytest
import pytest_asyncio
from fastapi import HTTPException
from httpx import AsyncClient, ASGITransport
from starlette import status

# 1. 导入 sqlalchemy 与数据库相关 (已清理)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 导入我们 app 的核心组件
from src.database import Base
from src.posts.dependencies import get_db_session
from src.main import app
from src.config import settings  # 导入 settings 以便断言

# 2. 【关键修复】使用“内存”数据库进行测试隔离
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, autoflush=False
)


# 3. 创建“测试专用”的依赖项 (覆盖器)
async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


# 4. 【关键修复】修复了夹具的“返回类型”
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:  # 之前是 AsyncSession
    """
    创建一个拥有“干净”、“隔离”数据库的测试客户端
    """
    # 5. 将“真实”的依赖项替换为“测试”的
    app.dependency_overrides[get_db_session] = override_get_db_session

    # 在测试运行“之前”：创建所有表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 运行测试
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client  # 你 yield 的是 client

    # 在测试运行“之后”：删除所有表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    app.dependency_overrides.clear()


# --- 测试用例 ---

@pytest.mark.asyncio
async def test_read_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    response_json = response.json()

    # 6. 【关键修复】断言必须和你的 .env 配置一致
    assert response_json["message"] == f"Welcome to my practice"
    assert response_json["环境"] == "development"


@pytest.mark.asyncio
async def test_create_and_read_item(async_client: AsyncClient):
    """
    测试“创建”和“读取”的完整闭环
    """
    # --- 第 1 阶段：创建 (Arrange & Act) ---
    test_item_json = {
        "item": {"name": "Test Item", "price": 123.45, "is_offer": False},
        "user": {"username": "testuser", "email": "test@example.com", "password": "ValidPassword123!@#"}  # 使用一个“强”密码
    }

    # 7. 【关键修复】
    #    - 路径是 PUT /items/{item_id} (匹配 router.py)
    response_post = await async_client.post(
        "/items/",  # 匹配 @router.post("/{item_id}")
        json=test_item_json
    )

    # 8. 【关键修复】现在我们可以正确地断言 `response_put`
    assert response_post.status_code == 200  # 检查创建是否成功
    response_data = response_post.json()
    assert response_data["username"] == "testuser"
    assert response_data["price"] == 123.45  # 检查是否返回了数据库 ID

    # --- 第 2 阶段：读取 (Act & Assert) ---

    # 现在我们去 GET，看看数据是否真的被写入了（内存）数据库
    response_get = await async_client.get("/items/")
    assert response_get.status_code == 200

    # 9. 【关键修复】`items_list` 必须在这里定义
    items_list = response_get.json()

    assert len(items_list) == 1
    assert items_list[0]["name"] == "Test Item"
    assert items_list[0]["price"] == 123.45

@pytest.mark.asyncio
async def test_health_check_succeeds(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json()=={"status":"ok"}

@pytest.mark.asyncio
async def test_health_check_fails(async_client: AsyncClient,monkeypatch):
    async def mock_db_fail():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mock DB Failure"
        )
    app.dependency_overrides[get_db_session] = mock_db_fail

    try:
        response = await async_client.get("/health")
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json()=={"detail":"Mock DB Failure"}
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_items_with_filter(async_client: AsyncClient):
    item_offer_json = {"name":"on offer","price":10.0,"is_offer":True}
    item_not_offer_json = {"name":"not on offer","price":10.0,"is_offer":False}

    await async_client.post("/items/", json=item_offer_json)
    await async_client.post("/items/", json=item_not_offer_json)

    # 测试过滤器=true
    response_true = await async_client.get("/items/",params={"is_offer_filter":True})
    assert response_true.status_code == 200
    items_list_true = response_true.json()
    assert len(items_list_true) == 1
    assert items_list_true[0]["name"] == "on offer"

    #测试过滤器=false
    response_false = await async_client.get("/items/",params={"is_offer_filter":False})
    assert response_false.status_code == 200
    items_list_false = response_false.json()
    assert len(items_list_false) == 1
    assert items_list_false[0]["name"] == "not on offer"

    #测试不过滤
    reponse_all = await async_client.get("/items/")
    assert reponse_all.status_code == 200
    assert len(reponse_all.json()) == 2  # 创建了两个，不过滤时应返回全部

