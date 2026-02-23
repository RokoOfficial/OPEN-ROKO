"""Tools de sistema do HMP."""

import os
import time
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class SystemEnv(BaseTool):
    @property
    def name(self) -> str:
        return "system.env"
    
    @property
    def description(self) -> str:
        return "Obtem variavel de ambiente (lista segura apenas)"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        name = str(params.get('name', ''))
        
        if name not in context.config.safe_env_vars:
            return {"error": f"Variavel de ambiente nao permitida: {name}"}
        
        return os.environ.get(name, '')


class SystemSleep(BaseTool):
    @property
    def name(self) -> str:
        return "system.sleep"
    
    @property
    def description(self) -> str:
        return "Pausa a execucao por N segundos (maximo 5)"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        seconds = min(float(params.get('seconds', 0)), 5)
        time.sleep(seconds)
        return f"Pausado por {seconds} segundos"


class SystemToolProvider(ToolProvider):
    """Provider de tools de sistema."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            SystemEnv(),
            SystemSleep(),
        ]
