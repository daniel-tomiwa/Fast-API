from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, authentication, vote
from fastapi.middleware.cors import CORSMiddleware


#The command below is used to create the tables without the help of alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#This is the root path for the API being created
@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)