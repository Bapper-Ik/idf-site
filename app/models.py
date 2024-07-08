from app.database import Base

from sqlalchemy import Column, String, Integer, TIMESTAMP, text, TIME, ForeignKey, Boolean, DATE
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class TaAlim(Base):
    __tablename__ = "ta'alims"
    
    id = Column(Integer, primary_key=True, nullable=False)
    ta_alim_category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    category = relationship("Category")
    


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    venue = Column(String, nullable=False)
    time = Column(TIME, nullable=False)
    isCompleted = Column(Boolean, nullable=False, server_default='false')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Images(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, nullable=False)
    caption = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, nullable=False)
    
    
    

