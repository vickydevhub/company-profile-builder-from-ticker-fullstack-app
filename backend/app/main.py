from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.build import router as build_router
from app.api.profile import router as profile_router
from app.database.database import init_db

app = FastAPI(
    title="Profile Builder API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(
    build_router,
    prefix="/api"
)

app.include_router(
    profile_router,
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "message": "Backend Running"
    }