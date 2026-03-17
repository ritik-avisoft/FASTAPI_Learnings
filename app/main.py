from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response, status, HTTPException

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

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
    return {"data": my_posts}

@app.post("/posts")
def create_post(new_post : Post, response:Response):
    post_dict=new_post.model_dump()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    response.status_code=status.HTTP_201_CREATED
    return {"data": new_post.model_dump()}

@app.get("/posts/{id}")
def get_post(id:int, response :Response):

    # return {"post_detail": f"Content: {my_posts[id].get('content')}, Title: {my_posts[id].get('title')}"}

    post = find_post(int(id))
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
    index=find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post):
    index=find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    
    post_dict=updated_post.model_dump()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":post_dict}

