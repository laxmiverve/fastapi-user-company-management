# SQLAlchemy Models
from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class CompanyModel(Base):
    __tablename__ = 'company_table'

    id = Column(Integer, primary_key = True, index = True)
    company_name = Column(String(100), nullable = False)
    company_email = Column(String(100), unique = True, nullable = False)
    company_number = Column(String(50), nullable = False)
    company_zipcode = Column(String(10), nullable = True)
    company_city = Column(String(50), nullable = True)
    company_state = Column(String(50), nullable = True)
    company_country = Column(String(50), nullable = False)


    user_id = Column(Integer, ForeignKey('usertable.id'))

    company_creator = relationship( 'UserModel', back_populates = 'companies', primaryjoin = 'CompanyModel.user_id == UserModel.id', lazy = 'joined')