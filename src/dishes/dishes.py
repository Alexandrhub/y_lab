import sys

from fastapi import APIRouter, HTTPException, Path, Depends, Response as res, status
from sqlalchemy.orm import Session
from typing import List
from . import crud
from .shemas import Response, UpdateDishes, CreateDishes

sys.path = ["", ".."] + sys.path[1:]
from src.config import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{target_menu_id}/submenus/{target_submenu_id}/dishes", status_code=201)
async def create(
    target_menu_id: int,
    target_submenu_id: int,
    request: CreateDishes,
    db: Session = Depends(get_db),
):
    create = await crud.create_dishes(
        db,
        request.title,
        request.description,
        request.price,
        target_menu_id,
        target_submenu_id,
    )
    if create == []:
        return Response(code=400, statuc="OK", message="Not Create").dict(
            exclude_none=True
        )
    return Response(code=201, statuc="OK", message="Create").dict(exclude_none=True)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}/dishes")
async def dishes_list(
    target_menu_id: int, target_submenu_id: int, db: Session = Depends(get_db)
):
    return await crud.get_dishes_list(target_menu_id, target_submenu_id, db)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def get_dishes(
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
    response: res,
    db: Session = Depends(get_db),
):
    dishes = await crud.get_dishes_by_id(
        target_menu_id, target_submenu_id, target_dish_id, db
    )
    if dishes != "404":
        return dishes
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "dish not found"}


@router.patch("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def update(
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
    request: UpdateDishes,
    db: Session = Depends(get_db),
):
    return await crud.update_dishes(
        target_menu_id,
        target_submenu_id,
        target_dish_id,
        request.title,
        request.description,
        request.price,
        db,
    )


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def delete_dishes(
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
    db: Session = Depends(get_db),
):
    return await crud.delete_dishes_by_id(
        target_menu_id, target_submenu_id, target_dish_id, db
    )
