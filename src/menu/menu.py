import sys

from fastapi import APIRouter, HTTPException, Path, Depends, Response as res, status
from sqlalchemy.orm import Session
from typing import List
from . import crud
from .shemas import Response, UpdateMenu, CreateMeny

sys.path = ["", ".."] + sys.path[1:]

from src.config import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
async def create(request: CreateMeny, db: Session = Depends(get_db)):
    await crud.create_menu(db, request.title, request.description)
    return Response(code=201, statuc="OK", message="Create").dict(exclude_none=True)


@router.get("/")
async def menu_list(db: Session = Depends(get_db)):
    return await crud.get_menu_list(db)


@router.get("/{target_menu_id}")
async def get_menu(target_menu_id: int, response: res, db: Session = Depends(get_db)):
    menu = await crud.get_menu_by_id(db, target_menu_id)
    if menu != "404":
        return menu

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "menu not found"}


@router.patch("/{target_menu_id}")
async def update(
    target_menu_id: int, request: UpdateMenu, db: Session = Depends(get_db)
):
    return await crud.update_menu(
        target_menu_id, request.title, request.description, db
    )


@router.delete("/{target_menu_id}")
async def delete_menu(target_menu_id: int, db: Session = Depends(get_db)):
    return await crud.delete_menu_by_id(db, target_menu_id)
