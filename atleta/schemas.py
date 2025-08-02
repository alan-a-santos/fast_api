from typing import Annotated, Optional
from pydantic import  Field, PositiveFloat
from categorias.schemas import CategoriaIn
from centro_treinamento.schemas import CentroTreinamentoAtleta
from contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(..., description="Nome do Atleta", example="Usain Bolt 5", max_length=50)]
    cpf: Annotated[str, Field(..., description="CPF do Atleta", example="123.456.789-00", max_length=14)]
    idade: Annotated[int, Field(..., description="Idade do Atleta", example=30)]
    peso: Annotated[PositiveFloat, Field(..., description="Peso do Atleta em kg", example=80.5)] 
    altura: Annotated[PositiveFloat, Field(..., description="Altura do Atleta em metros", example=1.85)]
    sexo: Annotated[str, Field(..., description="Sexo do Atleta", example="M", max_length=1)]
    categoria: Annotated[(CategoriaIn, Field(description="Categoria do atleta"))]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de Treinamento  do atleta")]


class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[ Optional [str], Field(..., description="Nome do Atleta", example="Usain Bolt 5", max_length=50)]
    idade: Annotated[Optional [int], Field(..., description="Idade do Atleta", example=30)]

class AtletaCustomizado(BaseSchema):
    nome: Annotated[str, Field(..., description="Nome do Atleta", example="Usain Bolt 5", max_length=50)]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de Treinamento  do atleta")]
    categoria: Annotated[(CategoriaIn, Field(description="Categoria do atleta"))]