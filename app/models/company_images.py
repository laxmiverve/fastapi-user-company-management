from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class CompanyImage(Base):
    __tablename__ = 'company_image_table'

    id = Column(Integer, primary_key = True, index = True)
    image_path = Column(String(255), nullable = False)
    company_id = Column(Integer, ForeignKey('company_table.id'))

    company = relationship('CompanyModel', back_populates='images')
