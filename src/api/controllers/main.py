from src.api.controllers.users import router as user_router


def setup_controllers(app):
    app.include_router(user_router)
