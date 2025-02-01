from fastapi import FastAPI, Depends, HTTPException, Header
from contextlib import asynccontextmanager
from database.connection import perform_migration 
from routers import landlord, buyer, contractor, tennat
from internal import admin
from typing import Annotated

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Creating tables..")
#     perform_migration()
#     yield

app = FastAPI(title="Bold Generations")

# Dependencies
def get_token_header(x_token: Annotated[str, Header()]):
    print("x_token -> ", x_token)
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

# Database



app.include_router(landlord.router)
app.include_router(buyer.router)
app.include_router(contractor.router)
app.include_router(tennat.router)
app.include_router(admin.router,
                   dependencies=[Depends(get_token_header)],
                   responses={418: {"description": "I'm a teapot"}},)

@app.get("/")
async def root():
    return {"message": "Welcome to Bold Generations!"}