from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.api.controllers.main import setup_controllers


def build_app():
    app = FastAPI(title='CRUD')

    setup_controllers(app=app)

    add_pagination(app)
    app.mount('/static', StaticFiles(directory='static'), name='static')

    return app
