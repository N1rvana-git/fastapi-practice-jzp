#区分“数据库表模型”（内部结构）和“API 模式”（外部合同）。
#定义数据表
from sqlalchemy import Column, Integer, String,Float,Boolean
from src.database import Base

class ItemModel(Base):
    __tablename__ = "item"#表名
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,index=True)
    price = Column(Float)
    is_offer = Column(Boolean,default=True)

class UserModel(Base):
    __tablename__ = "users"#把 Python 类映射成 PostgreSQL 表
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String,index=True)
    age=Column(Integer,nullable=False)
    email = Column(String,index=True)
    phone = Column(String,index=True)
    hashed_password = Column(String)
