from pydantic import BaseModel, FutureDatetime, FutureDate

from datetime import date, time, datetime



class Admin(BaseModel):
    id: int
    username: str
    password: str  
    role: int
    

class Taalim(BaseModel):
    id: int
    name: str
    

class Category(BaseModel):
    id: int
    name: str
    created_at: datetime
    

class CreateCategory(BaseModel):
    name: str
    created_at: datetime


class UpdateCategory(BaseModel):
    name: str
    
    
class BaseTaalim(BaseModel):
    id: int
    name: str
    url: str    
    created_at: datetime 


class CreateTaalim(BaseModel):
    name: str
    url: str
    created_at: datetime


class UpdateTaAlim(BaseModel):
    name: str
    url: str
    ta_alim_category_id: int


class BaseImgae(BaseModel):
    id: int
    url: str
    caption: str
    created_at: datetime


class CreateImage(BaseModel):
    url: str
    caption: str


class UpdateImage(CreateImage):
    pass


class BaseEvent(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    venue: str  
    isCompleted: bool
    created_at: datetime


class CreateEvent(BaseModel):
    name: str
    start_date: date
    end_date: date
    venue: str
    time: time


class UpdateEvent(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    venue: str
    time: datetime
    isCompleted: bool


# Response Models
class CategoryResponseModel(BaseModel):
    id: int
    name: str
    created_at: datetime


class TaAlimResponseModel(BaseModel):
    id: int
    name: str
    url: str
    created_at: datetime
    category: Category
    
    