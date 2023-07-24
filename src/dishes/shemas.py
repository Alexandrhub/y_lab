from pydantic import BaseModel, Field
from typing import List, Optional


from pydantic import BaseModel, Field
from typing import List, Optional


class CreateDishes(BaseModel):
    title: str
    description: str
    price: float


class Dishes_shem(BaseModel):
    title: str
    id: int
    pries: float
    description: str
    submenu_id: int

    class Config:
        orm_mode = True


class UpdateDishes(BaseModel):
    title: str
    description: str
    price: float


class RequestDishes(BaseModel):
    parameter: CreateDishes = Field(...)


class Response(BaseModel):
    code: str
    statuc: str
    message: str
