from fastapi import FastAPI
from src.onlineshop.resources import router

def get_app():
    app = FastAPI()

    app.include_router(router) # <- вот тут мы зарегистрировали роутер

    return app


app = get_app()
# запуск через uvicorn src.onlineshop.main:app --reload