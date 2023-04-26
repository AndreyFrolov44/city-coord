from fastapi import FastAPI

from app.cities.routers import router

app = FastAPI()

app.include_router(router, prefix='/api')



