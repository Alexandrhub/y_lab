import sys
from sqlalchemy.orm import Session
from .shemas import CreateMeny, UpdateMenu

sys.path = ["", ".."] + sys.path[1:]
from src.models import Menu, Submenu, Dishes


async def get_menu_list(db: Session):
    menu_list = db.query(Menu).offset(0).all()
    dop_param_menu = []

    _submenu = db.query(Submenu)
    _dishes = db.query(Dishes)

    for i in menu_list:
        submenus = _submenu.filter(Submenu.menu == i.id).all()
        dishes_count = 0

        for d in submenus:
            dishes_count += len(_dishes.filter(Dishes.submenu_id == d.id).all())

        dop_param_menu.append(
            {
                "title": i.title,
                "description": i.description,
                "id": i.id,
                "submenus_count": len(submenus),
                "dishes_count": dishes_count,
            }
        )
    return dop_param_menu


async def get_menu_by_id(db: Session, id: int):
    menu = db.query(Menu).filter(Menu.id == id).first()
    if menu != None:
        dop_param_menu = []
        _submenu = db.query(Submenu)
        _dishes = db.query(Dishes)
        submenus = _submenu.filter(Submenu.menu == menu.id).all()
        dishes_count = 0

        for d in submenus:
            dishes_count += len(_dishes.filter(Dishes.submenu_id == d.id).all())

        return {
            "data": {
                "title": menu.title,
                "description": menu.description,
                "id": menu.id,
            },
            "submenus_count": len(submenus),
            "dishes_count": dishes_count,
        }

    else:
        return "404"


async def delete_menu_by_id(db: Session, id: int):
    delete_data = db.query(Menu).filter(Menu.id == id).delete()
    db.commit()
    return delete_data


async def update_menu(
    target_menu_id: int, title: UpdateMenu, description: UpdateMenu, db: Session
):
    menu = db.query(Menu).filter(Menu.id == target_menu_id)
    update = menu.update({"title": title, "description": description})

    db.commit()

    return menu.first()


async def create_menu(db: Session, title: CreateMeny, description: CreateMeny):
    _menu = Menu(title=title, description=description)
    db.add(_menu)
    db.commit()
    db.refresh(_menu)
    return _menu
