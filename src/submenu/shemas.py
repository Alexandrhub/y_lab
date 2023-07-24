from pydantic import BaseModel, Field
from typing import List, Optional


class CreateSubmenu(BaseModel):
    title: str
    description: str


class UpdateSubmenu(BaseModel):
    title: str
    description: str


class RequestSubmeny(BaseModel):
    parameter: CreateSubmenu = Field(...)


class Response(BaseModel):
    code: str
    statuc: str
    message: str
