import os
import json
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

metadata = MetaData()

Base = declarative_base()

load_dotenv()

user = os.getenv("DB_USER")
database = os.getenv("DB_NAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

MYSQL_URL = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

file = open(os.getcwd() + '/respone_message.json')
msg = json.load(file)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        print("Error getting DB session : ", ex)
        return ex
    finally:
        db.close()
