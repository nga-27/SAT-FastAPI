import json

from fastapi import APIRouter, Response, HTTPException

from app.libs.utils.classes import User
from app.libs.utils.user_utils import serialize_users, add_user, remove_user

router = APIRouter(
    prefix="/users"
)


@router.get("/", tags=["Users"])
def get_users():
    return serialize_users()[0]


@router.post("/", tags=["Users"], status_code=201)
def post_user(user: User):
    res, code = add_user(user)
    if code != 201:
        raise HTTPException(status_code=code, detail=res['value'])
    return res


@router.delete("/{username}", tags=["Users"], status_code=200)
def delete_user(username: str, response: Response):
    res, code = remove_user(username)
    if code != 200:
        raise HTTPException(status_code=code, detail=res['value'])
    return res
