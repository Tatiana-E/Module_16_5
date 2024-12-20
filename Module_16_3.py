from fastapi import FastAPI, status, Body, HTTPException, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: Annotated[int, Path(gt=0, le=100, description= "User ID from 1 to 100")]
    username: Annotated[str, Path(min_length=3, max_length=25, pattern='[a-zA-Z0-9_-]+$')]
    age: Annotated[int, Path(gt=18, le=100, description= "Enter your age")]


@app.get('/')
async def get_(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "user": users[user_id-1]})


@app.post('/user/{username}/{age}')
async def create_user(user: User):
    if not users:
        user.id = 1
    else:
        user.id = users[-1].id + 1
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(gt=0, le=100, description= "User ID from 1 to 100")],
                      username: Annotated[str, Path(min_length=3, max_length=25, pattern='[a-zA-Z0-9_-]+$')],
                      age: Annotated[int, Path(gt=18, le=100, description= "Enter your age")]):
    try:
        edit_user = users[user_id-1]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(gt=0, le=100, description= "User ID from 1 to 100")]):
    try:
        user_out = users.pop(user_id-1)
        return user_out
    except:
        raise HTTPException(status_code=404, detail='Users not found')

