"""
HMP - Human Machine Protocol / Hybrid Macro Programming
Framework profissional para automacao e orquestracao de fluxos logicos.

Versao: 3.0.0
"""

__version__ = "3.0.0"
__author__ = "HMP Team"

from hmp.core.engine import HMPEngine
from hmp.core.context import ExecutionContext
from hmp.tools.registry import ToolRegistry
from hmp.expr.cache import ExpressionCache
from hmp.expr.evaluator import safe_eval_expr

__all__ = [
    "HMPEngine",
    "ExecutionContext", 
    "ToolRegistry",
    "ExpressionCache",
    "safe_eval_expr",
    "run_script",
    "list_tools",
]

_default_engine = None

def _get_engine() -> "HMPEngine":
    global _default_engine
    if _default_engine is None:
        _default_engine = HMPEngine()
    return _default_engine

def run_script(script: str, context: dict = None) -> dict:
    """Executa um script HMP e retorna o resultado."""
    return _get_engine().execute(script, context)

def list_tools() -> list:
    """Lista todas as tools disponiveis."""
    return _get_engine().registry.list_tools()
