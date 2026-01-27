"""Tools de criptografia do HMP."""

import hashlib
import uuid
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class CryptoHash(BaseTool):
    @property
    def name(self) -> str:
        return "crypto.hash"
    
    @property
    def description(self) -> str:
        return "Gera hash de uma string"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        text = str(params.get('text', ''))
        algorithm = str(params.get('algorithm', 'sha256')).lower()
        
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
        }
        
        if algorithm not in algorithms:
            algorithm = 'sha256'
        
        return algorithms[algorithm](text.encode('utf-8')).hexdigest()


class CryptoUuid(BaseTool):
    @property
    def name(self) -> str:
        return "crypto.uuid"
    
    @property
    def description(self) -> str:
        return "Gera um UUID v4"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(uuid.uuid4())


class CryptoToolProvider(ToolProvider):
    """Provider de tools de criptografia."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            CryptoHash(),
            CryptoUuid(),
        ]
