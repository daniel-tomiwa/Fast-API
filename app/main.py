from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#Creating a model for the post entity
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Title of the first post", "content": "content of the first post", "id": 1}, {"title": "favorite foods", 
"content": "I like Pizza", "id": 2}]

#Function to find a particular post
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#This is the root path for the API being created
@app.get("/")
def root():
    return {"message": "Hello World"}

#This is the path for getting all the available posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#This is the path for creating a post
#Note: changing the default status code for a particular path operation
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

#Creating an endpoint with a path parameter
#Make sure to be careful of path parameters and the ordering with other routed paths. Order matters!!
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
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
    index = find_index_post(id)

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}