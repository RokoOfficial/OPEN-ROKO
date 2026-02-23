"""Contexto de execucao do HMP."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from hmp.tools.registry import ToolRegistry
    from hmp.expr.cache import ExpressionCache


@dataclass
class ExecutionFrame:
    """Frame de execucao para pilha de chamadas."""
    name: str
    variables: Dict[str, Any] = field(default_factory=dict)
    is_function: bool = False


@dataclass 
class HMPConfig:
    """Configuracoes do motor HMP."""
    max_iterations: int = 1000000
    max_loop_iterations: int = 10000
    max_while_iterations: int = 1000
    max_nested_depth: int = 50
    http_timeout: int = 5
    http_max_response_size: int = 1024 * 1024
    allowed_http_hosts: frozenset = field(default_factory=lambda: frozenset([
        'api.github.com',
        'jsonplaceholder.typicode.com',
        'httpbin.org',
        'api.openai.com',
        'api.anthropic.com',
        'reqres.in',
        'dummyjson.com',
        'fakestoreapi.com',
    ]))
    safe_env_vars: frozenset = field(default_factory=lambda: frozenset([
        'PATH', 'HOME', 'USER', 'LANG', 'SHELL', 'TERM', 'TZ'
    ]))


class ExecutionContext:
    """
    Contexto de execucao do HMP.
    """

    def __init__(
        self,
        registry: Optional["ToolRegistry"] = None,
        cache: Optional["ExpressionCache"] = None,
        config: Optional[HMPConfig] = None,
        initial_vars: Optional[Dict[str, Any]] = None
    ):
        self.variables: Dict[str, Any] = initial_vars.copy() if initial_vars else {}
        self.call_stack: List[ExecutionFrame] = []
        self.functions: Dict[str, Dict] = {}
        self.config = config or HMPConfig()
        
        self._registry = registry
        self._cache = cache
        self._iteration_count = 0
        self._nested_depth = 0

    @property
    def registry(self) -> "ToolRegistry":
        if self._registry is None:
            from hmp.tools.registry import ToolRegistry
            self._registry = ToolRegistry()
        return self._registry

    @property
    def cache(self) -> "ExpressionCache":
        if self._cache is None:
            from hmp.expr.cache import ExpressionCache
            self._cache = ExpressionCache()
        return self._cache

    def get_variable(self, name: str, default: Any = None) -> Any:
        # Procura na pilha de frames (do topo para a base)
        for frame in reversed(self.call_stack):
            if name in frame.variables:
                return frame.variables[name]
            if frame.is_function:
                break
        
        return self.variables.get(name, default)

    def set_variable(self, name: str, value: Any) -> None:
        # Se houver frames de funcao, define no frame da funcao atual
        # Mas se for uma atribuicao global (fora de funcao), define no global
        if not any(f.is_function for f in self.call_stack):
            self.variables[name] = value
            return

        # Se estiver dentro de uma funcao, define no frame da funcao atual
        for frame in reversed(self.call_stack):
            if frame.is_function:
                frame.variables[name] = value
                return
        
        # Fallback
        self.variables[name] = value

    def push_frame(self, name: str, local_vars: Dict[str, Any] = None, is_function: bool = False) -> None:
        frame = ExecutionFrame(
            name=name,
            variables=local_vars.copy() if local_vars else {},
            is_function=is_function
        )
        self.call_stack.append(frame)
        self._nested_depth += 1

    def pop_frame(self) -> Optional[ExecutionFrame]:
        if self.call_stack:
            self._nested_depth -= 1
            return self.call_stack.pop()
        return None

    def increment_iteration(self) -> None:
        self._iteration_count += 1

    def check_limits(self) -> None:
        if self._iteration_count > self.config.max_iterations:
            raise RuntimeError(f"Limite de {self.config.max_iterations} iteracoes excedido")
        if self._nested_depth > self.config.max_nested_depth:
            raise RuntimeError(f"Limite de {self.config.max_nested_depth} niveis de aninhamento excedido")

    def reset(self) -> None:
        self.variables.clear()
        self.call_stack.clear()
        self._iteration_count = 0
        self._nested_depth = 0
