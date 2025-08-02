from uuid import uuid4
from fastapi import APIRouter, Body,status, HTTPException
from pydantic import UUID4
from sqlalchemy import select


from centro_treinamento.models import CentroTreinamentoModel
from centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post("/", summary= "Criar um novo centro de treinamento", status_code=status.HTTP_201_CREATED, response_model=CentroTreinamentoOut)

async def post(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    # Lógica para criar um novo atleta
   centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
   cento_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
   db_session.add(cento_treinamento_model)
   await db_session.commit()
   return centro_treinamento_out
   # breakpoint()  
   # pass

@router.get("/", summary= "Consultar todos os Centro de Treinamento", status_code=status.HTTP_201_CREATED, response_model=list[CentroTreinamentoOut])

async def query(db_session: DatabaseDependency) -> CentroTreinamentoOut:  
   centro_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
   
   return centro_treinamento

@router.get("/{id}", summary= "Consultar centros de treinamento pelo ID", status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut)

async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:  
   centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
   
   if not centro_treinamento:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Centro de treinamento não encontrado no id: {id}')
   
   return centro_treinamento