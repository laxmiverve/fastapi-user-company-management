from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = 'role_table'
    id = Column(Integer, primary_key = True, index = True)
    role_name = Column(String(100), nullable = False)

    # relationships
    users = relationship('UserModel', back_populates = 'role', primaryjoin = 'UserModel.role_id == Role.id', lazy = 'joined')