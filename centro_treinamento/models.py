from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped,mapped_column, relationship
# from atleta.models import AtletaModel
from contrib.models import BaseModel


class CentroTreinamentoModel(BaseModel):
    __tablename__ =    'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False, unique= True)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(50), nullable=True)
    atleta: Mapped[list['AtletaModel']]= relationship(back_populates = 'centros_treinamento')