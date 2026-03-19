from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv

from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

# load_dotenv()

app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Post(BaseModel):
    title: str
    content: str

while True:

    try:
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except psycopg2.Error as err:
        print("Error: Could not make connection to the Postgres database")
        print(err)
        time.sleep(2)
        break

#creating an arr to store the posts information.
my_posts=[
   {
      "title":"post 1",
      "content":"content of post 1",
      "id":1
   },
   {
      "title":"post 2",
      "content":"content of post 2",
      "id":2
   },
   {
      "title":"post 3",
      "content":"content of post 3",
      "id":3
   }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"Welcome on Online Social Media plateform login to get access"}

@app.post("/login")
def enter_username(payload: dict = Body(...)):
    print(payload)
    return {f"{payload['name'] } logged In Sucsessfully"}

# @app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    
    return {f"new post with '{payload['title']}' has beem added successfully"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post : Post, response:Response):
    # post_dict=new_post.model_dump()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # response.status_code=status.HTTP_201_CREATED
    # return {"data": new_post.model_dump()}

    cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,(new_post.title, new_post.content))
    new_post= cursor.fetchone()
    conn.commit()
    return {"data": new_post}
    

@app.get("/posts/{id}")
def get_post(id:int, response :Response):

    # return {"post_detail": f"Content: {my_posts[id].get('content')}, Title: {my_posts[id].get('title')}"}
    # post = find_post(int(id))

    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post=cursor.fetchone()
    if not post:
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": "post not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    else:
        return{
        "post_detail": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # index=find_index_post(id)
    # if index is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id: {id} does not exist"
    #     )
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    cursor.execute("""DELETE from posts where id = %s RETURNING *""",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post):
    # index=find_index_post(id)
    # if index is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id: {id} does not exist"
    #     )
    
    # post_dict=updated_post.model_dump()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    # return {"data":post_dict}

    cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (updated_post.title, updated_post.content, str(id)))
    post=cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")

    return {"data": post}
