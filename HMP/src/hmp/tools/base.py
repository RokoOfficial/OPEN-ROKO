"""Classe base abstrata para tools do HMP."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


@dataclass
class ToolParameter:
    """Define um parametro de uma tool."""
    name: str
    type: type
    required: bool = True
    default: Any = None
    description: str = ""


class BaseTool(ABC):
    """
    Classe base abstrata para todas as tools do HMP.
    
    Para criar uma nova tool, herde desta classe e implemente
    os metodos abstratos `name` e `invoke`.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome unico da tool no formato 'categoria.acao'.
        Exemplo: 'math.sum', 'string.upper'
        """
        pass

    @property
    def description(self) -> str:
        """Descricao da tool para documentacao."""
        return ""

    @property
    def parameters(self) -> List[ToolParameter]:
        """Lista de parametros aceitos pela tool."""
        return []

    @property
    def category(self) -> str:
        """Categoria da tool (extraida do nome)."""
        parts = self.name.split('.')
        return parts[0] if len(parts) > 1 else "general"

    @abstractmethod
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        """
        Executa a tool com os parametros fornecidos.
        
        Args:
            params: Dicionario com os parametros da tool
            context: Contexto de execucao atual
            
        Returns:
            Resultado da execucao da tool
        """
        pass

    def validate_params(self, params: Dict[str, Any]) -> Optional[str]:
        """
        Valida os parametros fornecidos.
        
        Returns:
            None se valido, mensagem de erro se invalido
        """
        for param in self.parameters:
            if param.required and param.name not in params:
                return f"Parametro obrigatorio ausente: {param.name}"
        return None

    def __repr__(self) -> str:
        return f"<Tool: {self.name}>"


class ToolProvider(ABC):
    """
    Provedor de tools para registrar multiplas tools de uma vez.
    Util para plugins e extensoes.
    """

    @abstractmethod
    def get_tools(self) -> List[BaseTool]:
        """Retorna lista de tools fornecidas por este provider."""
        pass

    @property
    def name(self) -> str:
        """Nome do provider."""
        return self.__class__.__name__
