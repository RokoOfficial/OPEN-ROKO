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
    line_number: int = 0


@dataclass 
class HMPConfig:
    """Configuracoes do motor HMP."""
    max_iterations: int = 100000
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
    
    Mantem o estado durante a execucao de um script HMP,
    incluindo variaveis, pilha de chamadas e configuracoes.
    """

    def __init__(
        self,
        registry: Optional["ToolRegistry"] = None,
        cache: Optional["ExpressionCache"] = None,
        config: Optional[HMPConfig] = None,
        initial_vars: Optional[Dict[str, Any]] = None
    ):
        self.variables: Dict[str, Any] = initial_vars.copy() if initial_vars else {}
        self.last_result: Dict[str, Any] = {}
        self.call_stack: List[ExecutionFrame] = []
        self.functions: Dict[str, Dict] = {}
        self.config = config or HMPConfig()
        
        self._registry = registry
        self._cache = cache
        self._iteration_count = 0
        self._nested_depth = 0

    @property
    def registry(self) -> "ToolRegistry":
        """Retorna o registry de tools."""
        if self._registry is None:
            from hmp.tools.registry import ToolRegistry
            self._registry = ToolRegistry()
        return self._registry

    @property
    def cache(self) -> "ExpressionCache":
        """Retorna o cache de expressoes."""
        if self._cache is None:
            from hmp.expr.cache import ExpressionCache
            self._cache = ExpressionCache()
        return self._cache

    def get_variable(self, name: str, default: Any = None) -> Any:
        """Obtem valor de uma variavel."""
        return self.variables.get(name, default)

    def set_variable(self, name: str, value: Any) -> None:
        """Define valor de uma variavel."""
        self.variables[name] = value

    def push_frame(self, name: str, local_vars: Dict[str, Any] = None) -> None:
        """Empilha um novo frame de execucao."""
        frame = ExecutionFrame(
            name=name,
            variables=local_vars.copy() if local_vars else {}
        )
        self.call_stack.append(frame)
        self._nested_depth += 1

    def pop_frame(self) -> Optional[ExecutionFrame]:
        """Desempilha o frame atual."""
        if self.call_stack:
            self._nested_depth -= 1
            return self.call_stack.pop()
        return None

    def increment_iteration(self) -> None:
        """Incrementa contador de iteracoes."""
        self._iteration_count += 1

    def check_limits(self) -> None:
        """Verifica se os limites foram excedidos."""
        if self._iteration_count > self.config.max_iterations:
            raise RuntimeError(
                f"Limite de {self.config.max_iterations} iteracoes excedido"
            )
        if self._nested_depth > self.config.max_nested_depth:
            raise RuntimeError(
                f"Limite de {self.config.max_nested_depth} niveis de aninhamento excedido"
            )

    def reset(self) -> None:
        """Reseta o contexto para um novo script."""
        self.variables.clear()
        self.last_result.clear()
        self.call_stack.clear()
        self._iteration_count = 0
        self._nested_depth = 0
