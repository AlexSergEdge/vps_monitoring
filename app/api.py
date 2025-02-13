from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.config import settings
from monitoring.main import get_name

from database.session import engine
from database.base import Base


# NOTE: unused - alembic used to migrate instead
def autocreate_tables():
    Base.metadata.create_all(bind=engine)


def start_app():
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    # autocreate_tables()
    return app

app = start_app()


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    name = get_name()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"name": name}
    )
