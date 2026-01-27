"""Tools matematicas do HMP."""

import math as pymath
from typing import Any, Dict, List, TYPE_CHECKING

from hmp.tools.base import BaseTool, ToolParameter, ToolProvider

if TYPE_CHECKING:
    from hmp.core.context import ExecutionContext


class MathSum(BaseTool):
    @property
    def name(self) -> str:
        return "math.sum"
    
    @property
    def description(self) -> str:
        return "Soma dois numeros"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter("a", float, True, 0, "Primeiro numero"),
            ToolParameter("b", float, True, 0, "Segundo numero"),
        ]
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> float:
        return float(params.get('a', 0)) + float(params.get('b', 0))


class MathSubtract(BaseTool):
    @property
    def name(self) -> str:
        return "math.subtract"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> float:
        return float(params.get('a', 0)) - float(params.get('b', 0))


class MathMultiply(BaseTool):
    @property
    def name(self) -> str:
        return "math.multiply"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> float:
        return float(params.get('a', 0)) * float(params.get('b', 0))


class MathDivide(BaseTool):
    @property
    def name(self) -> str:
        return "math.divide"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        b = float(params.get('b', 1))
        if b == 0:
            return {"error": "Divisao por zero"}
        return float(params.get('a', 0)) / b


class MathPower(BaseTool):
    @property
    def name(self) -> str:
        return "math.power"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        base = float(params.get('base', 0))
        exp = float(params.get('exp', 1))
        if exp > 100:
            return {"error": "Expoente muito grande (max 100)"}
        return base ** exp


class MathMod(BaseTool):
    @property
    def name(self) -> str:
        return "math.mod"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        b = float(params.get('b', 1))
        if b == 0:
            return {"error": "Modulo por zero"}
        return float(params.get('a', 0)) % b


class MathAbs(BaseTool):
    @property
    def name(self) -> str:
        return "math.abs"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> float:
        return abs(float(params.get('value', 0)))


class MathRound(BaseTool):
    @property
    def name(self) -> str:
        return "math.round"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> float:
        return round(float(params.get('value', 0)), int(params.get('decimals', 0)))


class MathMin(BaseTool):
    @property
    def name(self) -> str:
        return "math.min"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        values = params.get('values', [])
        if isinstance(values, list) and len(values) > 0:
            return min(values)
        return None


class MathMax(BaseTool):
    @property
    def name(self) -> str:
        return "math.max"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        values = params.get('values', [])
        if isinstance(values, list) and len(values) > 0:
            return max(values)
        return None


class MathSqrt(BaseTool):
    @property
    def name(self) -> str:
        return "math.sqrt"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> Any:
        value = float(params.get('value', 0))
        if value < 0:
            return {"error": "Raiz quadrada de numero negativo"}
        return pymath.sqrt(value)


class MathFloor(BaseTool):
    @property
    def name(self) -> str:
        return "math.floor"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> int:
        return pymath.floor(float(params.get('value', 0)))


class MathCeil(BaseTool):
    @property
    def name(self) -> str:
        return "math.ceil"
    
    def invoke(self, params: Dict[str, Any], context: "ExecutionContext") -> int:
        return pymath.ceil(float(params.get('value', 0)))


class MathToolProvider(ToolProvider):
    """Provider de tools matematicas."""
    
    def get_tools(self) -> List[BaseTool]:
        return [
            MathSum(),
            MathSubtract(),
            MathMultiply(),
            MathDivide(),
            MathPower(),
            MathMod(),
            MathAbs(),
            MathRound(),
            MathMin(),
            MathMax(),
            MathSqrt(),
            MathFloor(),
            MathCeil(),
        ]
