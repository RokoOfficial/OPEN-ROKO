"""Registro centralizado de tools do HMP."""

from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from hmp.tools.base import BaseTool, ToolProvider
    from hmp.core.context import ExecutionContext


class ToolRegistry:
    """
    Registro centralizado de tools com suporte a plugins.
    
    Gerencia todas as tools disponiveis no HMP, incluindo
    tools nativas e tools externas registradas via plugins.
    """

    def __init__(self):
        self._tools: Dict[str, "BaseTool"] = {}
        self._legacy_tools: Dict[str, Callable] = {}
        self._call_counts: Dict[str, int] = {}
        self._providers: List["ToolProvider"] = []

    def register(self, tool: "BaseTool") -> None:
        """Registra uma tool no registry."""
        self._tools[tool.name] = tool

    def register_legacy(self, name: str, func: Callable) -> None:
        """Registra uma tool no formato legado (funcao)."""
        self._legacy_tools[name] = func

    def register_provider(self, provider: "ToolProvider") -> None:
        """Registra um provider e todas as suas tools."""
        self._providers.append(provider)
        for tool in provider.get_tools():
            self.register(tool)

    def unregister(self, name: str) -> bool:
        """Remove uma tool do registry."""
        if name in self._tools:
            del self._tools[name]
            return True
        if name in self._legacy_tools:
            del self._legacy_tools[name]
            return True
        return False

    def get(self, name: str) -> Optional["BaseTool"]:
        """Retorna uma tool pelo nome."""
        return self._tools.get(name)

    def exists(self, name: str) -> bool:
        """Verifica se uma tool existe."""
        return name in self._tools or name in self._legacy_tools

    def execute(
        self, 
        tool_name: str, 
        params: Dict[str, Any], 
        context: "ExecutionContext"
    ) -> Any:
        """
        Executa uma tool registrada.
        
        Args:
            tool_name: Nome da tool a executar
            params: Parametros para a tool
            context: Contexto de execucao
            
        Returns:
            Resultado da execucao
        """
        self._call_counts[tool_name] = self._call_counts.get(tool_name, 0) + 1

        if tool_name in self._tools:
            tool = self._tools[tool_name]
            error = tool.validate_params(params)
            if error:
                return {"error": error}
            try:
                return tool.invoke(params, context)
            except Exception as e:
                return {"error": f"{tool_name}: {str(e)}"}

        if tool_name in self._legacy_tools:
            try:
                return self._legacy_tools[tool_name](params, context.variables)
            except Exception as e:
                return {"error": f"{tool_name}: {str(e)}"}

        return {"error": f"Tool desconhecida: {tool_name}"}

    def list_tools(self) -> List[str]:
        """Lista todas as tools disponiveis."""
        all_tools = set(self._tools.keys()) | set(self._legacy_tools.keys())
        return sorted(all_tools)

    def list_by_category(self) -> Dict[str, List[str]]:
        """Lista tools agrupadas por categoria."""
        categories: Dict[str, List[str]] = {}
        for name in self.list_tools():
            parts = name.split('.')
            category = parts[0] if len(parts) > 1 else "general"
            if category not in categories:
                categories[category] = []
            categories[category].append(name)
        return categories

    def get_stats(self) -> Dict[str, int]:
        """Retorna estatisticas de uso das tools."""
        return self._call_counts.copy()

    def clear_stats(self) -> None:
        """Limpa estatisticas de uso."""
        self._call_counts.clear()

    def __len__(self) -> int:
        return len(self._tools) + len(self._legacy_tools)

    def __contains__(self, name: str) -> bool:
        return self.exists(name)
