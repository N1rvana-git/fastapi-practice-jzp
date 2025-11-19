# PostgreSQL Docker 部署文档

## 📦 容器信息

- **容器名称**: `fastapi-postgres`
- **镜像**: `postgres:14-alpine`
- **端口映射**: `5433:5432` (主机端口:容器端口)
- **数据卷**: `fastapi-postgres-data` (持久化存储)

## 🔐 数据库凭据

```
数据库名: fastapi_db
用户名: fastapi_user
密码: fastapi_pass
主机: localhost
端口: 5433
```

## 🚀 常用命令

### 查看容器状态
```powershell
docker ps --filter "name=fastapi-postgres"
```

### 停止容器
```powershell
docker stop fastapi-postgres
```

### 启动容器
```powershell
docker start fastapi-postgres
```

### 重启容器
```powershell
docker restart fastapi-postgres
```

### 查看容器日志
```powershell
docker logs fastapi-postgres
docker logs -f fastapi-postgres  # 实时查看
```

### 进入容器执行 SQL
```powershell
docker exec -it fastapi-postgres psql -U fastapi_user -d fastapi_db
```

### 删除容器（数据会保留在数据卷中）
```powershell
docker stop fastapi-postgres
docker rm fastapi-postgres
```

### 完全清理（包括数据卷）
```powershell
docker stop fastapi-postgres
docker rm fastapi-postgres
docker volume rm fastapi-postgres-data
```

## 🔄 重新创建容器

如果需要重新创建容器（保留数据）：

```powershell
docker stop fastapi-postgres
docker rm fastapi-postgres
docker run -d `
  --name fastapi-postgres `
  -e POSTGRES_USER=fastapi_user `
  -e POSTGRES_PASSWORD=fastapi_pass `
  -e POSTGRES_DB=fastapi_db `
  -p 5433:5432 `
  -v fastapi-postgres-data:/var/lib/postgresql/data `
  --restart unless-stopped `
  postgres:14-alpine
```

## 📊 数据库连接字符串

### FastAPI 应用（异步）
```
postgresql+asyncpg://fastapi_user:fastapi_pass@localhost:5433/fastapi_db
```

### Alembic 迁移（同步）
```
postgresql://fastapi_user:fastapi_pass@localhost:5433/fastapi_db
```

### Python 连接示例
```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://fastapi_user:fastapi_pass@localhost:5433/fastapi_db",
    echo=True
)
```

## 🔧 故障排查

### 端口被占用
如果 5433 端口被占用，可以修改映射：
```powershell
# 使用 5434 端口
docker run -d ... -p 5434:5432 ... postgres:14-alpine
```
然后更新 `.env` 中的端口号。

### 连接被拒绝
1. 检查容器是否运行: `docker ps`
2. 检查容器日志: `docker logs fastapi-postgres`
3. 验证防火墙设置

### 重置数据库
```powershell
# 删除并重新创建容器和数据卷
docker stop fastapi-postgres
docker rm fastapi-postgres
docker volume rm fastapi-postgres-data

# 重新运行容器创建命令
# 然后运行: python test_pg_connection.py
```

## 📝 备份与恢复

### 备份数据库
```powershell
docker exec fastapi-postgres pg_dump -U fastapi_user fastapi_db > backup.sql
```

### 恢复数据库
```powershell
Get-Content backup.sql | docker exec -i fastapi-postgres psql -U fastapi_user -d fastapi_db
```

## ✅ 验证部署

运行测试脚本验证连接：
```powershell
python test_pg_connection.py
```

运行完整测试套件：
```powershell
pytest -v
```
