from src.api.controllers.users import router as user_router
from src.api.controllers.room import router as room_router
from src.api.controllers.comment import router as comment_router


def setup_controllers(app):
    app.include_router(user_router)
    app.include_router(room_router)
    app.include_router(comment_router)
