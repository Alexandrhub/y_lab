import sys
from sqlalchemy.orm import Session
from .shemas import CreateDishes, UpdateDishes

sys.path = ["", ".."] + sys.path[1:]
from src.models import Dishes, Submenu


async def create_dishes(
    db: Session,
    title: CreateDishes,
    description: CreateDishes,
    pries: CreateDishes,
    target_menu_id: int,
    target_submenu_id: int,
):
    _submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .first()
    )

    if _submenu != None:
        _dishes = Dishes(
            title=title, description=description, pries=pries, submenu_id=_submenu.id
        )

        _dishes.submenus = _submenu
        db.add(_dishes)
        db.commit()
        db.refresh(_dishes)
        return _dishes
    else:
        return []


async def get_dishes_list(target_menu_id: int, target_submenu_id: int, db: Session):
    _submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .first()
    )

    if _submenu != None:
        _dishes = db.query(Dishes).filter(Dishes.submenu_id == _submenu.id).all()
        arr_data = []
        for i in _dishes:
            i.pries = round(i.pries, 2)
            arr_data.append(i)
        return arr_data
    else:
        return []


async def get_dishes_by_id(
    target_menu_id: int, target_submenu_id: int, target_dish_id: int, db: Session
):
    _submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .first()
    )
    if _submenu != None:
        _dishes = (
            db.query(Dishes)
            .filter(Dishes.submenu_id == _submenu.id)
            .filter(Dishes.id == target_dish_id)
            .first()
        )
        if _dishes != None:
            _dishes.pries = round(_dishes.pries, 2)
            return [_dishes]
        else:
            return "404"
    else:
        return []


async def update_dishes(
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
    title: UpdateDishes,
    description: UpdateDishes,
    pries: UpdateDishes,
    db: Session,
):
    _submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .first()
    )
    if _submenu != None:
        _dishes = (
            db.query(Dishes)
            .filter(Dishes.submenu_id == _submenu.id)
            .filter(Dishes.id == target_dish_id)
        )
        _dishes_update = _dishes.update(
            {"title": title, "description": description, "pries": 14.50}
        )
        db.commit()
        dishes = _dishes.first()
        return {
            "title": dishes.title,
            "description": dishes.description,
            "price": str(dishes.pries),
        }
    else:
        return []


async def delete_dishes_by_id(
    target_menu_id: int, target_submenu_id: int, target_dish_id: int, db: Session
):
    _submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .first()
    )
    if _submenu != None:
        _dishes = (
            db.query(Dishes)
            .filter(Dishes.submenu_id == _submenu.id)
            .filter(Dishes.id == target_dish_id)
            .delete()
        )
        db.commit()
        return _dishes
    else:
        return []
