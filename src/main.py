"""
Ponto de entrada da aplicação O Termômetro.

Este módulo orquestra o fluxo principal:
1. Recebe input do usuário
2. Busca dados na API
3. Exibe resultado formatado
"""



import json
import sys
import os
from datetime import datetime
from typing import Self

# Forçar UTF-8 no Windows para suportar emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from src.cliente import (
    ClienteClima,
    CidadeNaoEncontradaError,
    ErroDeConexaoError,
    ClienteClimaException
)
from src.modelos import DadosClimaticos


def formatar_resultado(dados: DadosClimaticos) -> str:
    """
    Formata os dados climáticos para exibição.

    Args:
        dados: Dados climáticos validados

    Returns:
        String formatada para impressão
    """
    linha = "=" * 40

    return f"""
{linha}
🌡️  CLIMA EM {dados.cidade.upper()}
{linha}

🌡️  Temperatura:     {dados.temperatura:.1f}°C
🤒 Sensação térmica: {dados.sensacao_termica:.1f}°C
💧 Umidade:          {dados.umidade}%
💨 Vento:            {dados.vento_velocidade:.1f} m/s
☁️  Condição:         {dados.descricao.capitalize()}

{linha}
"""

def exportar_json(dados: DadosClimaticos, caminho: str = None) -> str:
    """
    Exporta os dados climáticos para um arquivo JSON.

    Args:
        dados: Dados climáticos a serem exportados
        caminho: Caminho do arquivo (opcional)

    Returns:
        Caminho do arquivo salvo
    """
    # Definir pasta de exportação e garantir que existe
    pasta_exports = "exports"
    if not os.path.exists(pasta_exports):
        os.makedirs(pasta_exports)

    # Se não passou caminho, gerar automático com timestamp na pasta correta
    if caminho is None:
        nome_arquivo = f"clima_{dados.cidade}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        caminho = os.path.join(pasta_exports, nome_arquivo)
    
    # Usar dados.model_dump() do Pydantic para converter em dict
    dados_dict = dados.model_dump()
    
    # Salvar com json.dump()
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados_dict, f, ensure_ascii=False, indent=2)
    
    return caminho


def executar() -> None:
    """
    Função principal que executa o programa.

    Fluxo:
    1. Solicita cidade ao usuário
    2. Busca dados na API
    3. Exibe resultado ou mensagem de erro
    """
    print("\n🌡️  O TERMÔMETRO - Consulta de Clima\n")

    # Criar instância do cliente
    cliente = ClienteClima()

    while True:
        # Solicitar entrada do usuário
        entrada = input("Digite o nome da cidade (ou 'sair' para encerrar): ").strip()

        # Verificar comando de sair
        if entrada.lower() == "sair":
            print("\n👋 Até logo!\n")
            break

        # Validar entrada vazia
        if not entrada:
            print("⚠️  Por favor, digite o nome de uma cidade.\n")
            continue

        # Separar cidades por vírgula e limpar espaços
        cidades = [cidade.strip() for cidade in entrada.split(",")]

        # Buscar dados para cada cidade
        for cidade in cidades:
            if not cidade:  # Ignorar strings vazias (ex: "London,,Tokyo")
                continue

            try:
                dados = cliente.buscar_clima(cidade)
                print(formatar_resultado(dados))

                # Exportar para JSON
                arquivo = exportar_json(dados)
                print(f"💾 Dados salvos em: {arquivo}\n")

            except CidadeNaoEncontradaError:
                print(f"\n❌ Cidade '{cidade}' não encontrada.")
                print("💡 Dica: Tente usar o nome em inglês (ex: 'Sao Paulo')\n")

            except ErroDeConexaoError as erro:
                print(f"\n🌐 Problema de conexão: {erro}")
                print("💡 Verifique sua internet e tente novamente.\n")

            except ClienteClimaException as erro:
                print(f"\n⚠️  Erro inesperado: {erro}\n")


# Este bloco só executa se rodar este arquivo diretamente
# Não executa se importar como módulo
if __name__ == "__main__":
    executar()