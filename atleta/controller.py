from datetime import datetime
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body,  Query,status, HTTPException
from pydantic import UUID4
from sqlalchemy import select
from fastapi_pagination import Page, paginate, add_pagination


from atleta.models import AtletaModel
from atleta.schemas import AtletaCustomizado, AtletaIn,  AtletaOut, AtletaUpdate
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post("/", summary= "Criar um novo atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)

async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)) :
 
   
   categoria_nome = atleta_in.categoria.nome
   centro_treinamento_nome= atleta_in.centro_treinamento.nome

   categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
   
   if not categoria:
      raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'A categoria {categoria_nome} não foi encontrada')
   
   centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first() 

   if not centro_treinamento:
      raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'O centro de treinamento {centro_treinamento_nome} não foi encontrada')
     
   try: 
        atleta_out = AtletaOut(id=uuid4(),created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

   except IntegrityError as e:
        await db_session.rollback()
        # Tente identificar se é erro de CPF duplicado pela mensagem original do erro
        if "cpf" in str(e.orig).lower():
            raise HTTPException(
                status_code=303,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        # Se for outro IntegrityError, pode lançar erro genérico
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade no banco de dados"
        )
   except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco"
        )

   return atleta_out


@router.get("/", summary= "Consultar todas os atletas", status_code=status.HTTP_200_OK, response_model=Page[AtletaOut])

async def query(db_session: DatabaseDependency) -> Page[AtletaOut]:  
   atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
   
   return paginate([AtletaOut.model_validate(atleta) for atleta in atletas])

@router.get("/{id}", summary= "Consultar atleta pelo ID", status_code=status.HTTP_200_OK, response_model=AtletaOut)

async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:  
   atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
   
   if not atleta:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Atleta não encontrado no id: {id}')
   
   return atleta

@router.patch("/{id}", summary= "Editar atleta pelo ID", status_code=status.HTTP_200_OK, response_model=AtletaOut)

async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:  
   atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
   
   if not atleta:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Atleta não encontrado no id: {id}')
   
   atleta_update = atleta_up.model_dump(exclude_unset=True)
   for key, value in atleta_update.items():
      setattr(atleta, key, value)
    
   await db_session.commit()
   await db_session.refresh(atleta)
      
   return atleta

@router.delete("/{id}", summary= "Deletar atleta pelo id", status_code=status.HTTP_204_NO_CONTENT)

async def get(id: UUID4, db_session: DatabaseDependency) -> None:  
   atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

   if not atleta:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Atleta não encontrado no id: {id}')
   
   await db_session.delete(atleta)
   await db_session.commit()


@router.get("/atleta/cpf", response_model=AtletaOut)
async def buscar_cliente_por_cpf(
    db_session: DatabaseDependency,
    cpf: str = Query(..., description="CPF do atleta")
) -> AtletaOut:
    result = await db_session.execute(
        select(AtletaModel).filter_by(cpf=cpf)
    )
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com CPF {cpf} não encontrado."
        )

    return atleta


@router.get("/atleta/nome", response_model=AtletaOut)
async def buscar_cliente_nome(
    db_session: DatabaseDependency,
    nome: str = Query(..., description="Nome do atleta")
) -> AtletaOut:
    result = await db_session.execute(
        select(AtletaModel).filter_by(nome=nome)
    )
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta  {nome} não encontrado."
        )

    return atleta

@router.get(
    "/atletas/customizados",
    summary="Consultar todos os atletas com campos customizados",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaCustomizado]
)
async def query(db_session: DatabaseDependency) -> list[AtletaCustomizado]:
    result = await db_session.execute(select(AtletaModel))
    atletas = result.scalars().all()
    return atletas  # FastAPI converte automaticamente para o modelo AtletaCustomizado
