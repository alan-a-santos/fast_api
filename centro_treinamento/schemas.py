from typing import Annotated
from pydentic import Field
from contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description = 'Nome do Centro de Treinamento', exemple= 'Centro A', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do Centro de Treinamento', exemple="Rua de XYZ, 100", max_length=60)]
    proprietario: Annotated[str, Field(description= 'Nome do Proprietário', exemple= 'Fulano de Tal', max_length=30)]