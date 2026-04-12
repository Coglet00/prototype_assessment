from fastapi import FastAPI
from src.backend.router import router 


app = FastAPI()

app.include_router(router)