# SQLAlchemy Models
from config.database import Base
from sqlalchemy import Column, Integer, String


# create new user
class UserModel(Base):
    __tablename__ = 'companyTable'

    id = Column(Integer, primary_key = True, index = True)
    company_name = Column(String(100), nullable = False)
    company_email = Column(String(100), unique = True, nullable = False)
    password = Column(String(100), nullable = False)
    company_zipcode = Column(String(10), nullable = True)
    company_city = Column(String(50), nullable = True)
    company_state = Column(String(50), nullable = True)
    company_country = Column(String(50), nullable = False)
