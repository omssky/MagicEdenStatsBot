from aiogram import Router

def setup_routers() -> Router:
    from . import admin, user, callbacks, other

    router = Router()

    router.include_router(admin.router)
    router.include_router(user.router)
    router.include_router(callbacks.router)
    router.include_router(other.router)
    
    return router