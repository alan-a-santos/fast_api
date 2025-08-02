from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped,mapped_column, relationship
from contrib.models import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atleta.models import AtletaModel

class CentroTreinamentoModel(BaseModel):
    __tablename__ =    'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False, unique= True)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(50), nullable=True)
    
    atleta: Mapped[list['AtletaModel']]= relationship('AtletaModel',back_populates = 'centro_treinamento')