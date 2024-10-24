from pydantic import BaseModel

class InputMontadora(BaseModel):
    nome: str
    pais: str
    ano_fundacao: int


class InputModelo(BaseModel):
    nome: str
    montadora_id: str
    valor_referencia: float
    ano_modelo: int
    motorizacao: float
    turbo: bool
    automatico: bool


class InputVeiculo(BaseModel):
    modelo_id: str
    cor: str
    ano_fabricacao: int
    valor: float
    placa: str
    vendido: bool
