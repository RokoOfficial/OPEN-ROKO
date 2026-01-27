"""Tools de log do HMP."""

from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class LogPrint(BaseTool):
    @property
    def name(self) -> str:
        return "log.print"
    
    @property
    def description(self) -> str:
        return "Imprime mensagem no console"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        message = str(params.get('message', ''))
        
        for var, val in context.variables.items():
            if not var.startswith('_'):
                message = message.replace(f'${{{var}}}', str(val))
        
        print(f"[LOG] {message}")
        return message


class LogWrite(BaseTool):
    @property
    def name(self) -> str:
        return "log.write"
    
    @property
    def description(self) -> str:
        return "Escreve mensagem no log"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        message = str(params.get('message', ''))
        return f"[LOG WRITE] {message}"


class LogToolProvider(ToolProvider):
    """Provider de tools de log."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            LogPrint(),
            LogWrite(),
        ]
