"""
Cliente para comunicação com a API OpenWeatherMap.

Este módulo encapsula toda a lógica de comunicação HTTP.
"""

import requests
from datetime import datetime
from typing import Optional, Tuple

from src.config import config
from src.modelos import DadosClimaticos, ErroAPI


class ClienteClimaException(Exception):
    """Exceção base para erros do cliente de clima."""
    pass


class CidadeNaoEncontradaError(ClienteClimaException):
    """Levantada quando a cidade não existe na API."""
    pass


class ErroDeConexaoError(ClienteClimaException):
    """Levantada quando há problemas de rede."""
    pass


class ClienteClima:
    """
    Cliente para buscar dados climáticos.

    Esta classe encapsula a comunicação com a API OpenWeatherMap,
    tratando erros e convertendo a resposta para nossos modelos.

    Exemplo de uso:
        cliente = ClienteClima()
        dados = cliente.buscar_clima("São Paulo")
        print(f"Temperatura: {dados.temperatura}°C")
    """

    def __init__(self, tempo_cache: int = 300) -> None:
        """Inicializa o cliente com as configurações.
        
        Args:
            tempo_cache: Tempo em segundos para manter cache (padrão: 300 = 5 min)
        """
        self._api_key = config.api_key
        self._base_url = config.base_url
        self._unidades = config.unidades
        self._idioma = config.idioma
        self._cache: dict[str, Tuple[DadosClimaticos, datetime]] = {}
        self._tempo_cache = tempo_cache

    def buscar_clima(self, cidade: str) -> DadosClimaticos:
        """
        Busca os dados climáticos de uma cidade.

        Args:
            cidade: Nome da cidade (ex: "São Paulo", "London")

        Returns:
            DadosClimaticos com as informações do clima

        Raises:
            CidadeNaoEncontradaError: Se a cidade não existir
            ErroDeConexaoError: Se houver problema de rede
            ClienteClimaException: Para outros erros da API
        """
        cidade_lower = cidade.lower()
        
        # 1. Verificar se há dados em cache válidos
        if cidade_lower in self._cache:
            dados_cache, timestamp = self._cache[cidade_lower]
            idade = (datetime.now() - timestamp).total_seconds()
            if idade < self._tempo_cache:
                print(f"📦 Usando cache ({int(self._tempo_cache - idade)}s restantes)")
                return dados_cache
        
        # 2. Montar os parâmetros da requisição
        parametros = self._montar_parametros(cidade)

        # 3. Fazer a requisição HTTP
        resposta_json = self._fazer_requisicao(parametros)

        # 4. Converter para nosso modelo
        dados = self._processar_resposta(resposta_json, cidade)
        
        # 5. Salvar no cache
        self._cache[cidade_lower] = (dados, datetime.now())

        return dados

    def _montar_parametros(self, cidade: str) -> dict:
        """
        Monta o dicionário de parâmetros para a requisição.

        Args:
            cidade: Nome da cidade

        Returns:
            Dicionário com os parâmetros da URL
        """
        return {
            "q": cidade,
            "appid": self._api_key,
            "units": self._unidades,
            "lang": self._idioma
        }

    def _fazer_requisicao(self, parametros: dict) -> dict:
        """
        Executa a requisição HTTP para a API.

        Args:
            parametros: Parâmetros da query string

        Returns:
            JSON da resposta como dicionário

        Raises:
            ErroDeConexaoError: Se não conseguir conectar
            CidadeNaoEncontradaError: Se cidade não existir (404)
            ClienteClimaException: Para outros erros HTTP
        """
        try:
            resposta = requests.get(
                self._base_url,
                params=parametros,
                timeout=10  # Nunca deixe sem timeout!
            )

            # Verificar código de status HTTP
            if resposta.status_code == 404:
                raise CidadeNaoEncontradaError(
                    f"Cidade não encontrada: {parametros['q']}"
                )

            if resposta.status_code == 401:
                raise ClienteClimaException(
                    "API Key inválida. Verifique seu arquivo .env"
                )

            if resposta.status_code != 200:
                raise ClienteClimaException(
                    f"Erro na API: código {resposta.status_code}"
                )

            return resposta.json()

        except requests.exceptions.ConnectionError:
            raise ErroDeConexaoError(
                "Não foi possível conectar à API. Verifique sua internet."
            )
        except requests.exceptions.Timeout:
            raise ErroDeConexaoError(
                "A API demorou muito para responder. Tente novamente."
            )

    def _processar_resposta(self, json_resposta: dict, cidade: str) -> DadosClimaticos:
        """
        Converte o JSON da API para nosso modelo Pydantic.

        Este método navega pelo JSON aninhado e extrai os campos necessários.

        Args:
            json_resposta: Resposta bruta da API
            cidade: Nome da cidade buscada (fallback)

        Returns:
            DadosClimaticos validado
        """
        # Extrair dados do JSON aninhado
        # Observe como navegamos: json["chave1"]["chave2"]

        dados_main = json_resposta["main"]
        dados_weather = json_resposta["weather"][0]  # É uma lista!
        dados_wind = json_resposta["wind"]

        # Criar o modelo Pydantic
        # Ele vai validar automaticamente os tipos
        return DadosClimaticos(
            cidade=json_resposta.get("name", cidade),
            temperatura=dados_main["temp"],
            sensacao_termica=dados_main["feels_like"],
            umidade=dados_main["humidity"],
            descricao=dados_weather["description"],
            vento_velocidade=dados_wind["speed"]
        )