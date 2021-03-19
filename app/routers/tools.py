from fastapi import APIRouter

router = APIRouter(
    prefix="/tools"
)


@router.get("/", tags=["tools"])
def echo_tools():
    return {"tools": "hello there"}
