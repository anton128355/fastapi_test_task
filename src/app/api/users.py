from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import UserDB, UserSchema

router = APIRouter()


@router.post("/user", response_model=UserDB, status_code=201)
async def post_user(payload: UserSchema):
    user_id = await crud.post(payload)

    response_object = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "password": payload.password
    }
    return response_object


@router.get("/user/{user_id}", response_model=UserDB)
async def get_user(user_id: int = Path(..., gt=0),):
    user = await crud.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Note not found")
    return user


@router.put("/user/{user_id}", response_model=UserDB)
async def put_user(payload: UserSchema, user_id: int = Path(..., gt=0),):
    user = await crud.get(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        user_id = await crud.put(user_id, payload)

    response_object = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "password": payload.password
    }
    return response_object


@router.patch("/user/{user_id}", response_model=UserDB)
async def patch_user(payload: UserSchema, user_id: int = Path(..., gt=0),):
    user = await crud.get(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        user_id = await crud.patch(user_id, payload)

        response_object = {
            "id": user_id,
            "username": payload.username,
            "email": payload.email,
            "password": payload.password
        }
        return response_object


@router.delete("/user/{user_id}", response_model=UserDB)
async def delete_user(user_id: int = Path(..., gt=0)):
    user = await crud.get(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        await crud.delete(user_id)
        return user


@router.get("/user-list", response_model=List[UserDB])
async def get_all_users():
    return await crud.get_all()
