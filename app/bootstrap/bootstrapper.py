from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.api.v1 import chat_router


def bootstrap() -> FastAPI:
    app: FastAPI = FastAPI()
    attach_cors(app)
    attach_app_default_handler(app)
    attach_app_routes(app)
    return app


def attach_cors(
        app: FastAPI
) -> None:
    origins: list[str] = ['*']  # TODO: Change this to the actual origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def attach_app_default_handler(
        app: FastAPI
) -> None:
    @app.get('/', include_in_schema=False)
    async def root():
        return {'message': 'KavakBot is running!'}


def attach_app_routes(
        app: FastAPI,
) -> None:
    app.include_router(chat_router.router, prefix='/api/v1/chat', tags=['chat'])
