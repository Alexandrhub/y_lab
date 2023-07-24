from pydantic import BaseModel, Field
from typing import List, Optional


class MenuShema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class test(BaseModel):
    id: int
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class CreateMeny(BaseModel):
    title: str
    description: str


class UpdateMenu(BaseModel):
    title: str
    description: str


class RequestMeny(BaseModel):
    parameter: CreateMeny = Field(...)


class Response(BaseModel):
    code: str
    statuc: str
    message: str
