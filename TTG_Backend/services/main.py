# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import describe_router
from api import app


app = FastAPI()

# CORS برای دسترسی از فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # آدرس فرانت‌اند React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to NVIDIA VILA Vision API"}

app.include_router(describe_router)
