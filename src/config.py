"""
Configurações da aplicação.

Carrega variáveis de ambiente de forma segura.
"""

import os
from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env
load_dotenv()


class Configuracao:
    """
    Centraliza todas as configurações da aplicação.

    Usar uma classe permite:
    1. Validar se as variáveis existem
    2. Ter autocomplete no editor
    3. Facilitar testes (podemos criar configurações fake)
    """

    def __init__(self) -> None:
        self.api_key: str = self._carregar_variavel("OPENWEATHER_API_KEY")
        self.base_url: str = "https://api.openweathermap.org/data/2.5/weather"
        self.unidades: str = "metric"  # Celsius
        self.idioma: str = "pt_br"

    def _carregar_variavel(self, nome: str) -> str:
        """
        Carrega uma variável de ambiente.

        Args:
            nome: Nome da variável

        Returns:
            Valor da variável

        Raises:
            ValueError: Se a variável não estiver definida
        """
        valor = os.getenv(nome)

        if valor is None:
            raise ValueError(
                f"Variável de ambiente '{nome}' não encontrada. "
                f"Verifique seu arquivo .env"
            )

        return valor


# Instância global (Singleton simples)
config = Configuracao()