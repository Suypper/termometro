"""
Modelos de dados usando Pydantic.

Pydantic valida automaticamente os tipos dos dados.
Se a API retornar algo inesperado, ele levanta um erro claro.
"""

from pydantic import BaseModel, Field


class DadosClimaticos(BaseModel):
    """
    Representa os dados climáticos processados de uma cidade.

    Attributes:
        cidade: Nome da cidade consultada
        temperatura: Temperatura atual em Celsius
        sensacao_termica: Sensação térmica em Celsius
        umidade: Umidade relativa do ar em porcentagem
        descricao: Descrição textual do clima (ex: "céu limpo")
        vento_velocidade: Velocidade do vento em m/s
    """

    cidade: str
    temperatura: float
    sensacao_termica: float = Field(alias="feels_like")  # Mapeia nome diferente
    umidade: int
    descricao: str
    vento_velocidade: float

    class Config:
        # Permite criar o modelo tanto com "sensacao_termica" quanto "feels_like"
        populate_by_name = True


class ErroAPI(BaseModel):
    """
    Representa um erro retornado pela API.
    """

    codigo: int
    mensagem: str