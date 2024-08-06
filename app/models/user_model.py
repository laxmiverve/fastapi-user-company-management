# SQLAlchemy Models

from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = 'usertable'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), nullable = True)
    email = Column(String(100), unique = True, nullable = False)
    password = Column(String(100), nullable = False)
    city = Column(String(50), nullable = True)
    state = Column(String(50), nullable = True)
    country = Column(String(50), nullable = True)


    # companies = relationship( 'CompanyModel', back_populates = 'company_creator', primaryjoin = 'CompanyModel.user_id == UserModel.id', lazy = 'joined')
