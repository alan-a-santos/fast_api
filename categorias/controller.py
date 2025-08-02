from uuid import uuid4
from fastapi import APIRouter, Body,status, HTTPException
from pydantic import UUID4
from sqlalchemy import select


from categorias.models import CategoriaModel
from categorias.schemas import CategoriaIn, CategoriaOut
from contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post("/", summary= "Criar nova categoria", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)

async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    # Lógica para criar um novo atleta
   categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
   categoria_model = CategoriaModel(**categoria_out.model_dump())
   db_session.add(categoria_model)
   await db_session.commit()
   return categoria_out
   # breakpoint()  
   # pass

@router.get("/", summary= "Consultar todas as categorias", status_code=status.HTTP_200_OK, response_model=list[CategoriaOut])

async def query(db_session: DatabaseDependency) -> CategoriaOut:  
   categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
   
   return categorias

@router.get("/{id}", summary= "Consultar categorias pelo ID", status_code=status.HTTP_200_OK, response_model=CategoriaOut)

async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:  
   categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
   
   if not categoria:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Categoria não encontrada no id: {id}')
   
   return categoria