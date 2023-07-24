import sys

from fastapi import APIRouter, HTTPException, Path, Depends, Response as res, status
from sqlalchemy.orm import Session
from typing import List
from . import crud
from .shemas import Response, UpdateSubmenu, CreateSubmenu

sys.path = ["", ".."] + sys.path[1:]
from src.config import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{target_menu_id}/submenus", status_code=201)
async def create(
    target_menu_id: int, request: CreateSubmenu, db: Session = Depends(get_db)
):
    await crud.create_submenu(db, request.title, request.description, target_menu_id)
    return Response(code=200, statuc="OK", message="Create").dict(exclude_none=True)


@router.get("/{target_menu_id}/submenus")
async def submenu_list(target_menu_id: int, db: Session = Depends(get_db)):
    return await crud.get_submenu_list(target_menu_id, db)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}")
async def get_submenu(
    target_menu_id: int,
    target_submenu_id: int,
    response: res,
    db: Session = Depends(get_db),
):
    submenu = await crud.get_submenu_by_id(target_menu_id, target_submenu_id, db)
    if submenu != "404":
        return submenu
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "submenu not found"}


@router.patch("/{target_menu_id}/submenus/{target_submenu_id}")
async def update(
    target_menu_id: int,
    target_submenu_id: int,
    request: UpdateSubmenu,
    db: Session = Depends(get_db),
):
    return await crud.update_submenu(
        target_menu_id, target_submenu_id, request.title, request.description, db
    )


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_menu(
    target_menu_id: int, target_submenu_id: int, db: Session = Depends(get_db)
):
    return await crud.delete_submenu_by_id(target_menu_id, target_submenu_id, db)
