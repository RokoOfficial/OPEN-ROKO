"""Tools de lista do HMP."""

from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class ListPush(BaseTool):
    @property
    def name(self) -> str:
        return "list.push"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        value = params.get('value')
        if isinstance(items, list):
            result = items.copy()
            result.append(value)
            return result
        return [value]


class ListPop(BaseTool):
    @property
    def name(self) -> str:
        return "list.pop"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        items = params.get('list', [])
        if isinstance(items, list) and len(items) > 0:
            result = items.copy()
            return result.pop()
        return None


class ListLength(BaseTool):
    @property
    def name(self) -> str:
        return "list.length"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> int:
        items = params.get('list', [])
        return len(items) if isinstance(items, list) else 0


class ListGet(BaseTool):
    @property
    def name(self) -> str:
        return "list.get"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        items = params.get('list', [])
        index = int(params.get('index', 0))
        if isinstance(items, list) and 0 <= index < len(items):
            return items[index]
        return None


class ListSet(BaseTool):
    @property
    def name(self) -> str:
        return "list.set"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        index = int(params.get('index', 0))
        value = params.get('value')
        if isinstance(items, list) and 0 <= index < len(items):
            result = items.copy()
            result[index] = value
            return result
        return items if isinstance(items, list) else []


class ListReverse(BaseTool):
    @property
    def name(self) -> str:
        return "list.reverse"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        return list(reversed(items)) if isinstance(items, list) else []


class ListSort(BaseTool):
    @property
    def name(self) -> str:
        return "list.sort"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        reverse = params.get('reverse', False)
        if isinstance(items, list):
            try:
                return sorted(items, reverse=bool(reverse))
            except TypeError:
                return items
        return []


class ListContains(BaseTool):
    @property
    def name(self) -> str:
        return "list.contains"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> bool:
        items = params.get('list', [])
        value = params.get('value')
        return value in items if isinstance(items, list) else False


class ListIndex(BaseTool):
    @property
    def name(self) -> str:
        return "list.index"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> int:
        items = params.get('list', [])
        value = params.get('value')
        if isinstance(items, list) and value in items:
            return items.index(value)
        return -1


class ListSlice(BaseTool):
    @property
    def name(self) -> str:
        return "list.slice"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        start = int(params.get('start', 0))
        end = params.get('end', None)
        if isinstance(items, list):
            if end is not None:
                return items[start:int(end)]
            return items[start:]
        return []


class ListFilter(BaseTool):
    @property
    def name(self) -> str:
        return "list.filter"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        if isinstance(items, list):
            return [x for x in items if x]
        return []


class ListUnique(BaseTool):
    @property
    def name(self) -> str:
        return "list.unique"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        if isinstance(items, list):
            seen = []
            for item in items:
                if item not in seen:
                    seen.append(item)
            return seen
        return []


class ListFlatten(BaseTool):
    @property
    def name(self) -> str:
        return "list.flatten"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List:
        items = params.get('list', [])
        result = []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, list):
                    result.extend(item)
                else:
                    result.append(item)
        return result


class ListToolProvider(ToolProvider):
    """Provider de tools de lista."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            ListPush(),
            ListPop(),
            ListLength(),
            ListGet(),
            ListSet(),
            ListReverse(),
            ListSort(),
            ListContains(),
            ListIndex(),
            ListSlice(),
            ListFilter(),
            ListUnique(),
            ListFlatten(),
        ]
