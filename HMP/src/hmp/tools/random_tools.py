"""Tools de aleatoriedade do HMP."""

import random
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class RandomNumber(BaseTool):
    @property
    def name(self) -> str:
        return "random.number"
    
    @property
    def description(self) -> str:
        return "Gera numero aleatorio entre min e max"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> int:
        min_val = int(params.get('min', 0))
        max_val = int(params.get('max', 100))
        return random.randint(min_val, max_val)


class RandomChoice(BaseTool):
    @property
    def name(self) -> str:
        return "random.choice"
    
    @property
    def description(self) -> str:
        return "Escolhe um item aleatorio de uma lista"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        items = params.get('items', [])
        if isinstance(items, list) and len(items) > 0:
            return random.choice(items)
        return None


class RandomShuffle(BaseTool):
    @property
    def name(self) -> str:
        return "random.shuffle"
    
    @property
    def description(self) -> str:
        return "Embaralha uma lista"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('items', [])
        if isinstance(items, list):
            result = items.copy()
            random.shuffle(result)
            return result
        return []


class RandomToolProvider(ToolProvider):
    """Provider de tools de aleatoriedade."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            RandomNumber(),
            RandomChoice(),
            RandomShuffle(),
        ]
