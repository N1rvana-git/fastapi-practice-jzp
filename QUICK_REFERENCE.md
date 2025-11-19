# PostgreSQL Docker 快速参考

## 容器信息
- 容器名: fastapi-postgres
- 端口: 5433 (主机) -> 5432 (容器)
- 用户: fastapi_user
- 密码: fastapi_pass  
- 数据库: fastapi_db

## 常用命令

### 查看状态
```powershell
docker ps --filter "name=fastapi-postgres"
```

### 启停控制
```powershell
docker start fastapi-postgres   # 启动
docker stop fastapi-postgres    # 停止
docker restart fastapi-postgres # 重启
```

### 查看日志
```powershell
docker logs fastapi-postgres
docker logs -f fastapi-postgres  # 实时
```

### 进入数据库
```powershell
docker exec -it fastapi-postgres psql -U fastapi_user -d fastapi_db
```

### 验证连接
```powershell
python test_pg_connection.py
pytest -v
```

## 连接字符串
```
# FastAPI (.env)
DATABASE_URL="postgresql+asyncpg://fastapi_user:fastapi_pass@localhost:5433/fastapi_db"

# Alembic (alembic.ini)
sqlalchemy.url = postgresql://fastapi_user:fastapi_pass@localhost:5433/fastapi_db
```
