"""Tools de data e hora do HMP."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class DateNow(BaseTool):
    @property
    def name(self) -> str:
        return "date.now"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        format_str = params.get('format', 'iso')
        now = datetime.now()
        if format_str == 'iso':
            return now.isoformat()
        elif format_str == 'date':
            return now.strftime('%Y-%m-%d')
        elif format_str == 'time':
            return now.strftime('%H:%M:%S')
        elif format_str == 'timestamp':
            return int(now.timestamp())
        else:
            try:
                return now.strftime(format_str)
            except ValueError:
                return now.isoformat()


class DateFormat(BaseTool):
    @property
    def name(self) -> str:
        return "date.format"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        timestamp = params.get('timestamp', None)
        format_str = params.get('format', '%Y-%m-%d %H:%M:%S')
        
        if timestamp is None:
            dt = datetime.now()
        elif isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp)
        else:
            try:
                dt = datetime.fromisoformat(str(timestamp))
            except ValueError:
                return str(timestamp)
        
        try:
            return dt.strftime(format_str)
        except ValueError:
            return dt.isoformat()


class DateParse(BaseTool):
    @property
    def name(self) -> str:
        return "date.parse"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        text = str(params.get('text', ''))
        format_str = params.get('format', None)
        
        try:
            if format_str:
                dt = datetime.strptime(text, format_str)
            else:
                dt = datetime.fromisoformat(text)
            return dt.isoformat()
        except ValueError:
            return {"error": f"Formato de data invalido: {text}"}


class DateAdd(BaseTool):
    @property
    def name(self) -> str:
        return "date.add"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> str:
        date_str = params.get('date', datetime.now().isoformat())
        days = int(params.get('days', 0))
        hours = int(params.get('hours', 0))
        minutes = int(params.get('minutes', 0))
        seconds = int(params.get('seconds', 0))
        
        try:
            dt = datetime.fromisoformat(str(date_str))
        except ValueError:
            dt = datetime.now()
        
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        result = dt + delta
        return result.isoformat()


class DateDiff(BaseTool):
    @property
    def name(self) -> str:
        return "date.diff"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        date1_str = params.get('date1', '')
        date2_str = params.get('date2', '')
        unit = params.get('unit', 'days')
        
        try:
            dt1 = datetime.fromisoformat(str(date1_str))
            dt2 = datetime.fromisoformat(str(date2_str))
        except ValueError:
            return {"error": "Formato de data invalido"}
        
        diff = dt2 - dt1
        
        if unit == 'days':
            return diff.days
        elif unit == 'hours':
            return diff.total_seconds() / 3600
        elif unit == 'minutes':
            return diff.total_seconds() / 60
        elif unit == 'seconds':
            return diff.total_seconds()
        else:
            return diff.days


class DateToolProvider(ToolProvider):
    """Provider de tools de data."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            DateNow(),
            DateFormat(),
            DateParse(),
            DateAdd(),
            DateDiff(),
        ]
