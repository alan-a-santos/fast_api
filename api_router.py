from fastapi import APIRouter
from atleta.controller import router as atleta
from centro_treinamento.controller import router as centro_treinamento
from categorias.controller import router as categorias

api_router = APIRouter()
api_router.include_router(atleta, prefix="/atleta", tags=["atleta"])
api_router.include_router(centro_treinamento, prefix="/centro_treinamento", tags=["centro_treinamento"])
api_router.include_router(categorias, prefix="/categorias", tags=["categorias"])

