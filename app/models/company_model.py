from config.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
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
    company_profile = Column(String(100), nullable = True)
    uuid = Column(String(50), nullable = False)

    # # store company images
    # company_images = Column(String(100), nullable = True)

    created_at = Column(TIMESTAMP, nullable = False, server_default = text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable = True, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user_id = Column(Integer, ForeignKey('usertable.id'))
    company_creator = relationship('UserModel', back_populates = 'companies', primaryjoin = 'CompanyModel.user_id == UserModel.id', lazy = 'joined')

    company_users = relationship('UserCompany', back_populates = 'company', lazy = 'joined')
    images = relationship('CompanyImage', back_populates='company', lazy='joined')