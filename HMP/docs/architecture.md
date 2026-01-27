# HMP - Arquitetura do Framework

Documentacao tecnica da arquitetura interna do HMP.

## Visao Geral

O HMP e composto por camadas bem definidas que se comunicam de forma unidirecional:

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI                                  │
│                     (cli/main.py)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      HMPEngine                               │
│                   (core/engine.py)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Parser    │  │  Executor   │  │   Tools     │         │
│  │             │  │             │  │  Registry   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ ExecutionCtx  │  │  Evaluator    │  │  ToolProviders│
│ (context.py)  │  │ (evaluator.py)│  │  (*_tools.py) │
└───────────────┘  └───────────────┘  └───────────────┘
```

## Modulos

### Core (`src/hmp/core/`)

#### engine.py - Motor de Execucao

O `HMPEngine` e o orquestrador principal que:

1. **Parseia** o script HMP em linhas
2. **Pre-processa** definicoes de funcoes
3. **Executa** linha por linha
4. **Delega** comandos para handlers especificos

```python
class HMPEngine:
    def __init__(self, config: EngineConfig = None):
        self.config = config or EngineConfig()
        self.registry = ToolRegistry()
        self._register_native_tools()
    
    def execute(self, script: str, initial_vars: dict = None) -> dict:
        context = ExecutionContext(initial_vars)
        result = {"output": [], "variables": {}, "return_value": None}
        # ... execucao
        return result
```

Handlers de comandos:
- `_handle_set()` - Processa SET
- `_handle_call()` - Processa CALL
- `_handle_if()` - Processa IF/ELSE/ENDIF
- `_handle_loop()` - Processa LOOP TIMES
- `_handle_while()` - Processa WHILE
- `_handle_for_each()` - Processa FOR EACH
- `_handle_try()` - Processa TRY/CATCH
- `_handle_parallel()` - Processa PARALLEL

#### context.py - Contexto de Execucao

`ExecutionContext` gerencia o estado durante a execucao:

```python
class ExecutionContext:
    def __init__(self, initial_vars: dict = None):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, dict] = {}
        self.call_stack: List[ExecutionFrame] = []
        self._iteration_count: int = 0
        self._nested_depth: int = 0
    
    def set_variable(self, name: str, value: Any) -> None
    def get_variable(self, name: str) -> Any
    def push_frame(self, name: str, local_vars: dict = None) -> None
    def pop_frame(self) -> None
    def check_limits(self) -> None  # Verifica limites de seguranca
```

### Expressions (`src/hmp/expr/`)

#### evaluator.py - Avaliador de Expressoes

Avalia expressoes de forma segura usando AST (sem `eval()`):

```python
def safe_eval_expr(expr: str, variables: dict) -> Any:
    """Avalia expressao de forma segura via AST."""
    tree = ast.parse(expr, mode='eval')
    return _eval_node(tree.body, variables)
```

Operadores suportados:
- Aritmeticos: `+`, `-`, `*`, `/`, `%`, `**`
- Comparacao: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logicos: `and`, `or`, `not`
- Acesso: `[]` (subscript)

#### cache.py - Cache de AST

Cache LRU para ASTs pre-compiladas:

```python
class ASTCache:
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, ast.AST] = {}
        self._order: List[str] = []
        self._max_size = max_size
    
    def get_or_compile(self, expr: str) -> ast.AST:
        if expr in self._cache:
            return self._cache[expr]
        tree = ast.parse(expr, mode='eval')
        self._store(expr, tree)
        return tree
```

### Tools (`src/hmp/tools/`)

#### base.py - Classes Base

```python
from abc import ABC, abstractmethod

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome da tool (ex: 'math.sum')"""
        pass
    
    @property
    def description(self) -> str:
        """Descricao da tool"""
        return ""
    
    @abstractmethod
    def invoke(self, params: dict, context: Any) -> Any:
        """Executa a tool com os parametros dados"""
        pass

class ToolProvider(ABC):
    @abstractmethod
    def get_tools(self) -> List[BaseTool]:
        """Retorna lista de tools fornecidas"""
        pass
```

#### registry.py - Registro de Tools

```python
class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._legacy_tools: Dict[str, Callable] = {}
    
    def register_tool(self, tool: BaseTool) -> None
    def register_function(self, name: str, func: Callable) -> None
    def register_provider(self, provider: ToolProvider) -> None
    def invoke(self, name: str, params: dict, context) -> Any
    def list_tools(self) -> List[str]
    def get_tool_info(self, name: str) -> Optional[dict]
```

#### Providers de Tools

Cada categoria de tools tem seu proprio provider:

| Arquivo | Provider | Tools |
|---------|----------|-------|
| `math_tools.py` | `MathToolProvider` | 13 tools |
| `string_tools.py` | `StringToolProvider` | 16 tools |
| `list_tools.py` | `ListToolProvider` | 13 tools |
| `json_tools.py` | `JsonToolProvider` | 2 tools |
| `date_tools.py` | `DateToolProvider` | 5 tools |
| `http_tools.py` | `HttpToolProvider` | 2 tools |
| `crypto_tools.py` | `CryptoToolProvider` | 2 tools |
| `random_tools.py` | `RandomToolProvider` | 3 tools |
| `log_tools.py` | `LogToolProvider` | 2 tools |
| `system_tools.py` | `SystemToolProvider` | 2 tools |
| `meta_tools.py` | `MetaToolProvider` | 4 tools |

### CLI (`src/hmp/cli/`)

#### main.py - Interface de Linha de Comando

```python
def main():
    parser = argparse.ArgumentParser(prog='hmp')
    subparsers = parser.add_subparsers()
    
    # Comandos
    run_parser = subparsers.add_parser('run')
    tools_parser = subparsers.add_parser('tools')
    validate_parser = subparsers.add_parser('validate')
    repl_parser = subparsers.add_parser('repl')
```

Comandos:
- `hmp run <arquivo>` - Executa script
- `hmp tools` - Lista tools disponiveis
- `hmp validate <arquivo>` - Valida sintaxe
- `hmp repl` - Modo interativo

### Runtime (`src/hmp/runtime/`)

#### errors.py - Excecoes Customizadas

```python
class HMPError(Exception):
    """Erro base do HMP"""
    pass

class HMPSyntaxError(HMPError):
    """Erro de sintaxe"""
    pass

class HMPRuntimeError(HMPError):
    """Erro de runtime"""
    pass

class HMPLimitError(HMPError):
    """Limite de seguranca excedido"""
    pass

class HMPToolError(HMPError):
    """Erro em tool"""
    pass
```

## Fluxo de Execucao

```
1. Script HMP recebido
        │
        ▼
2. Linhas separadas e limpas
        │
        ▼
3. Pre-processamento de FUNCTIONs
        │
        ▼
4. Execucao linha por linha
        │
        ├──► SET → _handle_set() → _parse_value() → context.set_variable()
        │
        ├──► CALL → _handle_call() → registry.invoke() → tool.invoke()
        │
        ├──► IF → _handle_if() → _evaluate_expression() → executa bloco
        │
        ├──► LOOP → _handle_loop() → executa N vezes
        │
        ├──► FOR EACH → _handle_for_each() → itera lista
        │
        └──► TRY → _handle_try() → executa com captura de erro
        
        ▼
5. Retorna resultado com output, variables, return_value
```

## Seguranca

### Limites de Protecao

```python
@dataclass
class EngineConfig:
    max_iterations: int = 10000
    max_loop_iterations: int = 1000
    max_recursion_depth: int = 100
    http_timeout: int = 30
    max_sleep: int = 5
```

### Avaliacao Segura

- **Sem `eval()`** - Todas expressoes via AST
- **Whitelist de operadores** - Apenas operadores permitidos
- **Isolamento de contexto** - Variaveis isoladas por frame
- **Timeout HTTP** - Limite de tempo para requisicoes
- **Limite de loops** - Previne loops infinitos

## Extensibilidade

### Criar Tool Customizada

```python
from hmp.tools.base import BaseTool

class MinhaToolCustomizada(BaseTool):
    @property
    def name(self) -> str:
        return "custom.minha_tool"
    
    @property
    def description(self) -> str:
        return "Faz algo customizado"
    
    def invoke(self, params: dict, context) -> Any:
        valor = params.get('valor', 0)
        return valor * 2
```

### Criar Provider

```python
from hmp.tools.base import ToolProvider

class MeuProvider(ToolProvider):
    def get_tools(self):
        return [
            MinhaToolCustomizada(),
            OutraToolCustomizada(),
        ]
```

### Registrar

```python
from hmp.core.engine import HMPEngine

engine = HMPEngine()
engine.registry.register_provider(MeuProvider())

# Ou registrar funcao diretamente
engine.registry.register_function(
    "custom.simples",
    lambda params, ctx: params.get('x', 0) + 1
)
```

## Testes

```bash
# Rodar todos os testes
python -m pytest tests/

# Apenas unitarios
python -m pytest tests/unit/

# Com cobertura
python -m pytest --cov=src/hmp tests/
```

---

Voltar para [README](../README.md) | Ver [Sintaxe](syntax.md) | Ver [Tools](tools-reference.md)
