from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from config import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    title = Column(String)
    description = Column(String)


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    title = Column(String)
    description = Column(String)
    menu = Column(Integer, ForeignKey("menu.id", ondelete="CASCADE"))


class Dishes(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    title = Column(String)
    description = Column(String)
    pries = Column(Float)
    submenu_id = Column(Integer, ForeignKey("submenu.id", ondelete="CASCADE"))
    submenus = relationship(Submenu)


menu = Menu.__table__
submenu = Submenu.__table__
