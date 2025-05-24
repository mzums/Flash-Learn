from fastapi import FastAPI
from web.api import users, sets

app = FastAPI()


app.include_router(users.router, prefix="/api/users")
app.include_router(sets.router, prefix="/api/v1/sets")