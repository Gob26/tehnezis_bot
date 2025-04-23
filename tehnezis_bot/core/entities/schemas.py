from typing import Optional
from pydantic import BaseModel, HttpUrl

class CrawlingTargetCreate(BaseModel):
    title: str
    url: HttpUrl
    xpath: str
    price: Optional[int] = None

class CrawlingTargetOut(CrawlingTargetCreate):
    id: int

    class Config:
        from_attributes = True