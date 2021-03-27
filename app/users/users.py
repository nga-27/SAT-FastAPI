import json
import secrets

from fastapi import APIRouter, Response, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.libs.utils.classes import User
from app.libs.utils.user_utils import serialize_user, add_user, remove_user, check_user

router = APIRouter(
    prefix="/users"
)

security = HTTPBasic()


@router.get("/", tags=["Users"])
def get_user(credentials: HTTPBasicCredentials = Depends(security)):
    if check_user(credentials.username):
        return serialize_user(credentials.username)
    raise HTTPException(
        status_code=401, detail=f"Username {credentials.username} is not found.")


@router.post("/", tags=["Users"], status_code=201)
def post_user(user: User):
    res, code = add_user(user)
    if code != 201:
        raise HTTPException(status_code=code, detail=res['value'])
    return res


@router.delete("/", tags=["Users"], status_code=200)
def delete_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if check_user(credentials.username):
        res, code = remove_user(credentials.username, credentials.password)
        if code != 200:
            raise HTTPException(status_code=code, detail=res['value'])
        return res
    raise HTTPException(
        status_code=401, detail=f"Username {credentials.username} is not found.")
