from fastapi import FastAPI

from src.api.controllers.main import setup_controllers


def build_app():
    app = FastAPI(title='CRUD')

    setup_controllers(app=app)

    return app
