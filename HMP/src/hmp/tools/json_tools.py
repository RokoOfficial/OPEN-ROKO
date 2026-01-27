"""Tools de JSON do HMP."""

import json
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class JsonParse(BaseTool):
    @property
    def name(self) -> str:
        return "json.parse"
    
    @property
    def description(self) -> str:
        return "Converte string JSON para objeto"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        text = str(params.get('text', '{}'))
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": "JSON invalido"}


class JsonStringify(BaseTool):
    @property
    def name(self) -> str:
        return "json.stringify"
    
    @property
    def description(self) -> str:
        return "Converte objeto para string JSON"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        value = params.get('value', {})
        pretty = params.get('pretty', False)
        try:
            if pretty:
                return json.dumps(value, indent=2, ensure_ascii=False)
            return json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(value)


class JsonToolProvider(ToolProvider):
    """Provider de tools de JSON."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            JsonParse(),
            JsonStringify(),
        ]
