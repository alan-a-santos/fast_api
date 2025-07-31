from typing import Annotated
from pydantic import  Field, PositiveFloat
from contrib.schemas import BaseSchema

class Atleta(BaseSchema):
    nome: Annotated[str, Field(..., description="Nome do Atleta", example="Usain Bolt", max_length=50)]
    cpf: Annotated[str, Field(..., description="CPF do Atleta", example="123.456.789-00", max_length=11)]
    idade: Annotated[int, Field(..., description="Idade do Atleta", example=30)]
    peso: Annotated[PositiveFloat, Field(..., description="Peso do Atleta em kg", example=80.5)] 
    altura: Annotated[PositiveFloat, Field(..., description="Altura do Atleta em metros", example=1.85)]
    sexo: Annotated[str, Field(..., description="Sexo do Atleta", example="M", max_length=1)]