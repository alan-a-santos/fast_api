
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped,mapped_column, relationship
from contrib.models import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atleta.models import AtletaModel


class CategoriaModel(BaseModel):
    __tablename__ =    'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50),  nullable=False, unique=True)

    atleta: Mapped[list['AtletaModel']] = relationship('AtletaModel', back_populates='categoria')
