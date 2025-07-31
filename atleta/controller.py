from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from models import Atleta  # modelo SQLAlchemy

router = APIRouter()

@router.get("/", summary= "Listar atletas", response_model=List[Atleta], status_code=status.HTTP_200_CREATED)
def get_atletas(
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Atleta)

    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)

    resultados = query.all()
    return resultados
