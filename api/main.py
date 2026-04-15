from fastapi import FastAPI
from src.backend.router import router 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://prototypeassessment-8arxkijkpvo8kkrtc4vojh.streamlit.app/"], # In production, replace "*" with your Streamlit URL
    allow_methods=["*"],
    allow_headers=["*"],
)