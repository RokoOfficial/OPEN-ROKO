"""Tools de string do HMP."""

from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class StringConcat(BaseTool):
    @property
    def name(self) -> str:
        return "string.concat"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(params.get('a', '')) + str(params.get('b', ''))


class StringSplit(BaseTool):
    @property
    def name(self) -> str:
        return "string.split"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> List[str]:
        return str(params.get('text', '')).split(str(params.get('delimiter', ' ')))


class StringJoin(BaseTool):
    @property
    def name(self) -> str:
        return "string.join"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        items = params.get('items', [])
        delimiter = str(params.get('delimiter', ''))
        if isinstance(items, list):
            return delimiter.join(str(item) for item in items)
        return str(items)


class StringUpper(BaseTool):
    @property
    def name(self) -> str:
        return "string.upper"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(params.get('text', '')).upper()


class StringLower(BaseTool):
    @property
    def name(self) -> str:
        return "string.lower"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(params.get('text', '')).lower()


class StringTrim(BaseTool):
    @property
    def name(self) -> str:
        return "string.trim"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(params.get('text', '')).strip()


class StringReplace(BaseTool):
    @property
    def name(self) -> str:
        return "string.replace"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(params.get('text', '')).replace(
            str(params.get('old', '')), 
            str(params.get('new', ''))
        )


class StringContains(BaseTool):
    @property
    def name(self) -> str:
        return "string.contains"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> bool:
        return str(params.get('search', '')) in str(params.get('text', ''))


class StringLength(BaseTool):
    @property
    def name(self) -> str:
        return "string.length"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> int:
        return len(str(params.get('text', '')))


class StringSubstring(BaseTool):
    @property
    def name(self) -> str:
        return "string.substring"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        text = str(params.get('text', ''))
        start = int(params.get('start', 0))
        end = params.get('end', None)
        if end is not None:
            return text[start:int(end)]
        return text[start:]


class StringStartsWith(BaseTool):
    @property
    def name(self) -> str:
        return "string.startswith"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> bool:
        return str(params.get('text', '')).startswith(str(params.get('prefix', '')))


class StringEndsWith(BaseTool):
    @property
    def name(self) -> str:
        return "string.endswith"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> bool:
        return str(params.get('text', '')).endswith(str(params.get('suffix', '')))


class StringRepeat(BaseTool):
    @property
    def name(self) -> str:
        return "string.repeat"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        text = str(params.get('text', ''))
        times = min(int(params.get('times', 1)), 1000)
        return text * times


class StringReverse(BaseTool):
    @property
    def name(self) -> str:
        return "string.reverse"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        return str(params.get('text', ''))[::-1]


class StringPadLeft(BaseTool):
    @property
    def name(self) -> str:
        return "string.pad_left"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        text = str(params.get('text', ''))
        length = min(int(params.get('length', 0)), 1000)
        char = str(params.get('char', ' '))[:1] or ' '
        return text.rjust(length, char)


class StringPadRight(BaseTool):
    @property
    def name(self) -> str:
        return "string.pad_right"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        text = str(params.get('text', ''))
        length = min(int(params.get('length', 0)), 1000)
        char = str(params.get('char', ' '))[:1] or ' '
        return text.ljust(length, char)


class StringToolProvider(ToolProvider):
    """Provider de tools de string."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            StringConcat(),
            StringSplit(),
            StringJoin(),
            StringUpper(),
            StringLower(),
            StringTrim(),
            StringReplace(),
            StringContains(),
            StringLength(),
            StringSubstring(),
            StringStartsWith(),
            StringEndsWith(),
            StringRepeat(),
            StringReverse(),
            StringPadLeft(),
            StringPadRight(),
        ]
