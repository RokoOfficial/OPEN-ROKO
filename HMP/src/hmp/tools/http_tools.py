"""Tools HTTP do HMP."""

import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class HttpGet(BaseTool):
    @property
    def name(self) -> str:
        return "http.get"
    
    @property
    def description(self) -> str:
        return "Faz requisicao HTTP GET"
    
    def _is_host_allowed(self, host: str, context: "ExecutionContext") -> bool:
        """Verifica se o host e permitido."""
        host = host.lower().split(':')[0]
        allowed = context.config.allowed_http_hosts
        
        if host in allowed:
            return True
        
        for allowed_host in allowed:
            if host.endswith('.' + allowed_host):
                return True
        
        return False
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        url = str(params.get('url', ''))
        
        if not url:
            return {"error": "URL nao fornecida"}
        
        parsed = urlparse(url)
        if not self._is_host_allowed(parsed.netloc, context):
            return {"error": f"Host nao permitido: {parsed.netloc}"}
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'HMP/3.0'})
            with urllib.request.urlopen(req, timeout=context.config.http_timeout) as response:
                data = response.read(context.config.http_max_response_size)
                content_type = response.headers.get('Content-Type', '')
                
                if 'application/json' in content_type:
                    return json.loads(data.decode('utf-8'))
                return data.decode('utf-8')
        except urllib.error.URLError as e:
            return {"error": f"Erro de conexao: {str(e)}"}
        except Exception as e:
            return {"error": f"Erro HTTP: {str(e)}"}


class HttpPost(BaseTool):
    @property
    def name(self) -> str:
        return "http.post"
    
    @property
    def description(self) -> str:
        return "Faz requisicao HTTP POST"
    
    def _is_host_allowed(self, host: str, context: "ExecutionContext") -> bool:
        """Verifica se o host e permitido."""
        host = host.lower().split(':')[0]
        allowed = context.config.allowed_http_hosts
        
        if host in allowed:
            return True
        
        for allowed_host in allowed:
            if host.endswith('.' + allowed_host):
                return True
        
        return False
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        url = str(params.get('url', ''))
        body = params.get('body', {})
        
        if not url:
            return {"error": "URL nao fornecida"}
        
        parsed = urlparse(url)
        if not self._is_host_allowed(parsed.netloc, context):
            return {"error": f"Host nao permitido: {parsed.netloc}"}
        
        try:
            data = json.dumps(body).encode('utf-8')
            req = urllib.request.Request(
                url, 
                data=data,
                headers={
                    'User-Agent': 'HMP/3.0',
                    'Content-Type': 'application/json'
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=context.config.http_timeout) as response:
                resp_data = response.read(context.config.http_max_response_size)
                content_type = response.headers.get('Content-Type', '')
                
                if 'application/json' in content_type:
                    return json.loads(resp_data.decode('utf-8'))
                return resp_data.decode('utf-8')
        except urllib.error.URLError as e:
            return {"error": f"Erro de conexao: {str(e)}"}
        except Exception as e:
            return {"error": f"Erro HTTP: {str(e)}"}


class HttpToolProvider(ToolProvider):
    """Provider de tools HTTP."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            HttpGet(),
            HttpPost(),
        ]
