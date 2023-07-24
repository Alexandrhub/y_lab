from fastapi import FastAPI
import menu.menu
import submenu.submenu
import dishes.dishes

app = FastAPI()


@app.get("/")
async def home():
    return "Welcome"


app.include_router(menu.menu.router, prefix="/api/v1/menus", tags=["menu"])
app.include_router(submenu.submenu.router, prefix="/api/v1/menus", tags=["submenu"])
app.include_router(dishes.dishes.router, prefix="/api/v1/menus", tags=["dishes"])
