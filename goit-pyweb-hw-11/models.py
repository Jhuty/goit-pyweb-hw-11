from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from db import Base
from sqlalchemy import create_engine

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)

engine = create_engine("postgresql://boris:ytunymuny@localhost:5432/mydatabase")
Base.metadata.create_all(bind=engine)