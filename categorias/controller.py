from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def post():
    return {"message": "Post deu certo"}

@router.get("/")
async def get():
    return {"message": "a rota get deu certo"}