#区分“数据库表模型”（内部结构）和“API 模式”（外部合同）。
#定义数据表
from sqlalchemy import Column, Integer, String,Float,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class ItemModel(Base):
    __tablename__ = "item"#表名
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,index=True)
    price = Column(Float)
    is_offer = Column(Boolean,default=True)
    
    # 外键：指向 users 表的 id 列
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # 关系：反向查主人
    owner = relationship("UserModel", back_populates="items")

class UserModel(Base):
    __tablename__ = "users"#把 Python 类映射成 PostgreSQL 表
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String,index=True)
    age=Column(Integer,nullable=False)
    email = Column(String,index=True)
    phone = Column(String,index=True)
    hashed_password = Column(String)
    
    # 关系：反向查物品列表
    # cascade="all, delete-orphan" 表示：如果用户被删了，他的物品也会自动被删掉
    items = relationship("ItemModel", back_populates="owner", cascade="all, delete-orphan")
