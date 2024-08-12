from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

class UserCompany(Base):
    __tablename__ = 'user_company'

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey('usertable.id'))
    company_id = Column(Integer, ForeignKey('company_table.id'))

    # Relationships
    user = relationship('UserModel', back_populates = 'user_companies')
    company = relationship('CompanyModel', back_populates = 'company_users')

