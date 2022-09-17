from dataclasses import dataclass
from sqlite3 import Cursor
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

#Creating a model for the post entity
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

#Create a connection to the database instance with psycopg
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastaspi',
            user='postgres',
            password='june41998',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


#This is the root path for the API being created
@app.get("/")
def root():
    return {"message": "Hello World"}

#This is the path for getting all the available posts
@app.get("/posts")
def get_posts():
    cursor.execute(
        """SELECT * FROM posts"""
    )
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

#This is the path for creating a post
#Note: changing the default status code for a particular path operation
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published) # The order matters
    )
    #Note that the above is done to prevent SQL injection into the connected database
    new_post = cursor.fetchone()

    #It is important to note that changes to the database has to be commited to be reflected in the database server
    conn.commit()
    return {"data": new_post}

#Creating an endpoint with a path parameter
#Make sure to be careful of path parameters and the ordering with other routed paths. Order matters!!
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s""",
        #It is important to convert the id back to a string
        (str(id))
    )
    post = cursor.fetchone()
    if not post:
        #There is a HTTPException funstion from fast API
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""",
        (str(id))
    )
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} deos not exist"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {"data": updated_post}