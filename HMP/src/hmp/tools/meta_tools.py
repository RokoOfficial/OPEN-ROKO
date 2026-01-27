"""Tools de meta-informacao do HMP."""

from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class MetaVersion(BaseTool):
    @property
    def name(self) -> str:
        return "meta.version"
    
    @property
    def description(self) -> str:
        return "Retorna versao do HMP"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Dict:
        return {
            "version": "3.0.0",
            "name": "HMP - Human Machine Protocol",
            "engine": "HMP Engine"
        }


class MetaTools(BaseTool):
    @property
    def name(self) -> str:
        return "meta.tools"
    
    @property
    def description(self) -> str:
        return "Lista todas as tools disponiveis"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List[str]:
        return context.registry.list_tools()


class MetaMetrics(BaseTool):
    @property
    def name(self) -> str:
        return "meta.metrics"
    
    @property
    def description(self) -> str:
        return "Retorna metricas de execucao"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Dict:
        return {
            "variables_count": len(context.variables),
            "functions_count": len(context.functions),
            "tool_calls": context.registry.get_stats(),
        }


class MetaCacheStats(BaseTool):
    @property
    def name(self) -> str:
        return "meta.cache_stats"
    
    @property
    def description(self) -> str:
        return "Retorna estatisticas do cache de expressoes"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Dict:
        return context.cache.stats()


class MetaToolProvider(ToolProvider):
    """Provider de tools de meta-informacao."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            MetaVersion(),
            MetaTools(),
            MetaMetrics(),
            MetaCacheStats(),
        ]
