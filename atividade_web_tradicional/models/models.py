from sqlmodel import SQLModel, Field, Relationship
import ulid

# Classe Montadora
class Montadora(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    nome: str
    pais: str
    ano_fundacao: int
    modelos: list["Modelo"] = Relationship(back_populates="montadora")


# Classe Modelo
class Modelo(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    nome: str
    montadora_id: str = Field(foreign_key="montadora.id")
    valor_referencia: float
    ano_modelo: int
    motorizacao: float
    turbo: bool
    automatico: bool
    montadora: Montadora = Relationship(back_populates="modelos")
    veiculos: list["Veiculo"] = Relationship(back_populates="modelo")


# Classe Veiculo
class Veiculo(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    modelo_id: str = Field(foreign_key="modelo.id")
    cor: str
    ano_fabricacao: int
    valor: float
    placa: str
    vendido: bool
    modelo: Modelo = Relationship(back_populates="veiculos")
