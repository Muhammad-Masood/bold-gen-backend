from fastapi import FastAPI, Depends, HTTPException, Header
from contextlib import asynccontextmanager
from .database.connection import perform_migration
from .routers import landlord, buyer, contractor, tennat, auth
from .internal import admin
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

_:bool = load_dotenv()
origin_client_https = os.getenv("ORIGIN_CLIENT_HTTPS")

origins = [
    "http://localhost:3000",
    origin_client_https,
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    perform_migration()
    yield

app = FastAPI(title="Bold Generations", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def start():
#     """Launched with `poetry run start` at root level"""
#     uvicorn.run("bold_gen_backend.main:app", host="0.0.0.0", port=8000, reload=True)

# Dependencies
# def get_token_header(x_token: Annotated[str, Header()]):
#     print("x_token -> ", x_token)
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

# async def get_query_token(token: str):
#     if token != "jessica":
#         raise HTTPException(status_code=400, detail="No Jessica token provided")


app.include_router(landlord.router)
app.include_router(buyer.router)
app.include_router(contractor.router)
app.include_router(tennat.router)
app.include_router(auth.router)
app.include_router(admin.router)
                #    dependencies=[Depends(get_token_header)],
                #    responses={418: {"description": "I'm a teapot"}},)

@app.get("/")
async def root():
    return {"message": "Welcome to Bold Generations!"}