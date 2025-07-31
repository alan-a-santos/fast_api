
from typing import Annotated
from pydantic import Field
from contrib.schemas import BaseSchema


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description= "Categoria do atleta", exemple="Atletismo", max_length=10)]