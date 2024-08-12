# # SQLAlchemy Models

# from config.database import Base
# from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
# from sqlalchemy.orm import relationship


# class UserModel(Base):
#     __tablename__ = 'usertable'

#     id = Column(Integer, primary_key = True, index = True)
#     name = Column(String(100), nullable = True)
#     email = Column(String(100), unique = True, nullable = False)
#     password = Column(String(100), nullable = False)
#     city = Column(String(50), nullable = True)
#     state = Column(String(50), nullable = True)
#     country = Column(String(50), nullable = True)

#     created_at = Column(TIMESTAMP, nullable = False, server_default = text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, nullable = True, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    
#     # relationships
#     companies = relationship('CompanyModel', back_populates = 'company_creator', primaryjoin = 'CompanyModel.user_id == UserModel.id', lazy = 'joined')

#     user_companies = relationship('UserCompany', back_populates='user', lazy='joined')
    
#     role_id = Column(Integer, ForeignKey('role_table.id'), nullable=False)
#     role = relationship('Role', back_populates='users', primaryjoin='UserModel.role_id == Role.id', lazy='joined')



# SQLAlchemy Models
from config.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
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

    created_at = Column(TIMESTAMP, nullable = False, server_default = text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable = True, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    companies = relationship('CompanyModel', back_populates = 'company_creator', primaryjoin = 'CompanyModel.user_id == UserModel.id', lazy='joined')

    user_companies = relationship('UserCompany', back_populates='user', lazy='joined')

    role_id = Column(Integer, ForeignKey('role_table.id'), nullable = False)
    role = relationship('Role', back_populates ='users', primaryjoin = 'UserModel.role_id == Role.id', lazy = 'joined')
    