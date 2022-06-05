from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_query_token
from .internal import admin
from .routers import items, users

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(dependencies=[])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)

cors_origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
