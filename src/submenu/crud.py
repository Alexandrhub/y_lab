import sys
from sqlalchemy.orm import Session
from .shemas import CreateSubmenu, UpdateSubmenu

sys.path = ["", ".."] + sys.path[1:]
from src.models import Submenu, Dishes


async def get_submenu_list(target_menu_id: int, db: Session):
    submenu_list = db.query(Submenu).filter(Submenu.menu == target_menu_id).all()

    dop_param_submenu = []
    _dishes = db.query(Dishes)
    for s in submenu_list:
        dishes_count = len(_dishes.filter(Dishes.submenu_id == s.id).all())
        dop_param_submenu.append(
            {
                "title": s.title,
                "description": s.description,
                "id": s.id,
                "dishes_count": dishes_count,
            }
        )

    return dop_param_submenu


async def get_submenu_by_id(target_menu_id: int, target_submenu_id: int, db: Session):
    submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .first()
    )
    if submenu != None:
        _dishes = db.query(Dishes)
        dishes_count = len(_dishes.filter(Dishes.submenu_id == submenu.id).all())

        return {
            "data": {
                "title": submenu.title,
                "description": submenu.description,
                "id": submenu.id,
            },
            "dishes_count": dishes_count,
        }
    else:
        return "404"


async def delete_submenu_by_id(
    target_menu_id: int, target_submenu_id: int, db: Session
):
    delete_data = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .delete()
    )
    db.commit()
    return delete_data


async def update_submenu(
    target_menu_id: int,
    target_submenu_id: int,
    title: UpdateSubmenu,
    description: UpdateSubmenu,
    db: Session,
):
    submenu = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
    )
    update = (
        db.query(Submenu)
        .filter(Submenu.menu == target_menu_id)
        .filter(Submenu.id == target_submenu_id)
        .update({"title": title, "description": description})
    )
    db.commit()

    return submenu.first()


async def create_submenu(
    db: Session, title: CreateSubmenu, description: CreateSubmenu, target_menu_id: int
):
    _submenu = Submenu(title=title, description=description, menu=target_menu_id)
    db.add(_submenu)
    db.commit()
    db.refresh(_submenu)
    return _submenu
