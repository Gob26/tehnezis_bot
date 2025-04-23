from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()   

class CrawlingTarget(Base):
    __tablename__ = 'crawling_target'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    xpath = Column(String)
    price = Column(Integer)