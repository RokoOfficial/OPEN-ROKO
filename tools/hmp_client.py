#!/usr/bin/env python3
"""
Cliente para executar codigos HMP via API REST
"""

import requests
import json
import sys
from typing import Dict, Any, Optional, List


class HMPClient:
    def __init__(self, base_url: str = "https://e36c8d65-9709-4fae-b674-e8758ca7e7b4-00-ip365yuhjk9.spock.replit.dev/"):
        """Inicializa o cliente HMP com a URL base da API."""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HMP-Client/1.0'
        })
    
    def run_file(self, filename: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executa um arquivo .hmp via API.
        
        Args:
            filename: Nome do arquivo HMP (com ou sem extensao .hmp)
            variables: Variaveis iniciais para o script (opcional)
        
        Returns:
            Resultado da execucao
        """
        if not filename.endswith('.hmp'):
            filename += '.hmp'
        
        url = f"{self.base_url}/run/file/{filename}"
        
        payload = {}
        if variables:
            payload['variables'] = variables
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def run_script(self, script: str) -> Dict[str, Any]:
        """
        Executa um script HMP inline.
        
        Args:
            script: Codigo HMP como string
        
        Returns:
            Resultado da execucao
        """
        url = f"{self.base_url}/run"
        payload = {'script': script}
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def call_tool(self, tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executa uma tool diretamente.
        
        Args:
            tool_name: Nome da tool (ex: math.sum, string.upper)
            params: Parametros da tool
        
        Returns:
            Resultado da tool
        """
        url = f"{self.base_url}/tool/{tool_name}"
        
        try:
            response = self.session.post(url, json=params or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def list_files(self) -> Dict[str, Any]:
        """Lista todos os arquivos .hmp disponiveis."""
        url = f"{self.base_url}/files"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def get_file_content(self, filename: str) -> Dict[str, Any]:
        """Obtem o conteudo de um arquivo .hmp."""
        if not filename.endswith('.hmp'):
            filename += '.hmp'
        
        url = f"{self.base_url}/files/{filename}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def list_tools(self) -> Dict[str, Any]:
        """Lista todas as tools disponiveis."""
        url = f"{self.base_url}/tools"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def list_tools_by_category(self, category: str) -> Dict[str, Any]:
        """Lista tools de uma categoria especifica."""
        url = f"{self.base_url}/tools/{category}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Erro de requisicao: {str(e)}'}
    
    def math_sum(self, a: float, b: float) -> float:
        """Soma dois numeros."""
        result = self.call_tool('math.sum', {'a': a, 'b': b})
        return result.get('result')
    
    def math_multiply(self, a: float, b: float) -> float:
        """Multiplica dois numeros."""
        result = self.call_tool('math.multiply', {'a': a, 'b': b})
        return result.get('result')
    
    def string_upper(self, text: str) -> str:
        """Converte texto para maiusculas."""
        result = self.call_tool('string.upper', {'text': text})
        return result.get('result')
    
    def string_lower(self, text: str) -> str:
        """Converte texto para minusculas."""
        result = self.call_tool('string.lower', {'text': text})
        return result.get('result')
    
    def date_now(self) -> str:
        """Retorna data/hora atual."""
        result = self.call_tool('date.now', {})
        return result.get('result')
    
    def random_number(self, min_val: float = 0, max_val: float = 100) -> float:
        """Gera numero aleatorio."""
        result = self.call_tool('random.number', {'min': min_val, 'max': max_val})
        return result.get('result')
    
    def crypto_hash(self, text: str, algorithm: str = 'sha256') -> str:
        """Gera hash de texto."""
        result = self.call_tool('crypto.hash', {'text': text, 'algorithm': algorithm})
        return result.get('result')
    
    def crypto_uuid(self) -> str:
        """Gera UUID."""
        result = self.call_tool('crypto.uuid', {})
        return result.get('result')


def print_result(result: Dict[str, Any]):
    """Imprime o resultado de forma formatada."""
    if result.get('success'):
        print("Execucao bem-sucedida!")
        
        if 'filename' in result:
            print(f"Arquivo: {result['filename']}")
        
        if result.get('output'):
            print("\nSaida:")
            for line in result['output']:
                print(f"  {line}")
        
        if result.get('variables'):
            print("\nVariaveis:")
            for name, value in result['variables'].items():
                print(f"  {name} = {value}")
        
        if result.get('return_value') is not None:
            print(f"\nRetorno: {result['return_value']}")
    else:
        print("Erro na execucao:")
        print(f"  {result.get('error', 'Erro desconhecido')}")


def main():
    """Funcao principal para demonstrar o uso do cliente."""
    client = HMPClient("http://localhost:5000")
    
    print("=== HMP Client - Demonstracao ===\n")
    
    print("1. Listando arquivos disponiveis:")
    files = client.list_files()
    if files.get('files'):
        for f in files['files']:
            print(f"   - {f['name']}")
    print()
    
    print("2. Executando hello_world.hmp:")
    result = client.run_file('hello_world')
    print_result(result)
    print()
    
    print("3. Chamando tools diretamente:")
    print(f"   math.sum(10, 5) = {client.math_sum(10, 5)}")
    print(f"   string.upper('hello') = {client.string_upper('hello')}")
    print(f"   date.now() = {client.date_now()}")
    print(f"   crypto.uuid() = {client.crypto_uuid()}")
    print()
    
    print("4. Executando script inline:")
    script = '''
SET x TO 10
SET y TO 20
CALL math.sum WITH a=${x}, b=${y}
SET resultado TO ${last_result["default"]}
CALL log.print WITH message="Soma: ${x} + ${y} = ${resultado}"
RETURN ${resultado}
'''
    result = client.run_script(script)
    print_result(result)


if __name__ == "__main__":
    main()
