from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#This is the root path for the API being created
@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)

app.include_router(user.router)

app.include_router(authentication.router)