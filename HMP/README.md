# HMP - Human Machine Protocol

<p align="center">
  <strong>Framework profissional para automacao e orquestracao de fluxos logicos</strong>
</p>

<p align="center">
  <a href="#instalacao">Instalacao</a> |
  <a href="#uso-rapido">Uso Rapido</a> |
  <a href="#sintaxe">Sintaxe</a> |
  <a href="#tools">Tools</a> |
  <a href="#exemplos">Exemplos</a> |
  <a href="#documentacao">Documentacao</a>
</p>

---

## Sobre

O HMP (Human Machine Protocol) e uma linguagem de programacao declarativa projetada para:

- **Automacao** - Orquestracao de fluxos logicos complexos
- **Integracao IA** - Ponte entre LLMs e execucao deterministica
- **Seguranca** - Execucao isolada com limites de protecao
- **Extensibilidade** - Sistema de plugins para tools customizadas

### Caracteristicas

- 64+ tools nativas (math, string, list, http, crypto, etc.)
- Sintaxe declarativa em ingles natural
- Avaliacao segura de expressoes via AST
- Suporte a loops, condicionais, funcoes e paralelismo
- CLI profissional para execucao e depuracao

## Instalacao

```bash
# Clonar o repositorio
git clone <repo-url>
cd HMP

# Instalar em modo de desenvolvimento
pip install -e .

# Ou com dependencias de desenvolvimento
pip install -e ".[dev]"
```

## Uso Rapido

### Via CLI

```bash
# Executar um script
hmp run examples/hello_world.hmp

# Listar todas as tools disponiveis
hmp tools

# Modo interativo (REPL)
hmp repl

# Validar script sem executar
hmp validate script.hmp
```

### Via Python

```python
from hmp import run_script, list_tools

# Executar script HMP
result = run_script('''
SET nome TO "Mundo"
CALL log.print WITH message="Ola, ${nome}!"
RETURN "Concluido"
''')

print(result['return_value'])  # "Concluido"
print(result['output'])        # Lista de saidas

# Listar tools disponiveis
tools = list_tools()
print(f"Total: {len(tools)} tools")
```

## Sintaxe

### Variaveis

```hmp
SET nome TO "Maria"
SET idade TO 25
SET lista TO [1, 2, 3, 4, 5]
SET dobro TO ${idade * 2}
```

### Condicionais

```hmp
IF ${idade} >= 18 THEN
    CALL log.print WITH message="Maior de idade"
ELSE
    CALL log.print WITH message="Menor de idade"
ENDIF
```

### Loops

```hmp
# Loop fixo
LOOP 5 TIMES
    CALL log.print WITH message="Iteracao ${loop_index}"
ENDLOOP

# Loop condicional
SET i TO 0
WHILE ${i} < 10
    SET i TO ${i + 1}
ENDWHILE

# Iteracao de lista
SET frutas TO ["maca", "banana", "laranja"]
FOR EACH fruta IN ${frutas}
    CALL log.print WITH message="Fruta: ${fruta}"
ENDFOR
```

### Funcoes

```hmp
FUNCTION calcular_dobro(valor)
    SET resultado TO ${valor * 2}
    RETURN ${resultado}
ENDFUNCTION

CALL calcular_dobro WITH valor=21
CALL log.print WITH message="Resultado: ${last_result}"
```

### Tratamento de Erros

```hmp
TRY
    CALL http.get WITH url="https://api.exemplo.com/dados"
CATCH
    CALL log.print WITH message="Erro: ${error}"
ENDTRY
```

## Tools

O HMP inclui 64 tools nativas organizadas em 11 categorias:

| Categoria | Tools | Descricao |
|-----------|-------|-----------|
| `math.*` | 13 | Operacoes matematicas |
| `string.*` | 16 | Manipulacao de strings |
| `list.*` | 13 | Operacoes com listas |
| `json.*` | 2 | Parse e stringify JSON |
| `date.*` | 5 | Data e hora |
| `http.*` | 2 | Requisicoes HTTP |
| `crypto.*` | 2 | Hash e UUID |
| `random.*` | 3 | Numeros aleatorios |
| `log.*` | 2 | Logging e debug |
| `system.*` | 2 | Sistema operacional |
| `meta.*` | 4 | Metadados e tipos |

Veja a [referencia completa de tools](docs/tools-reference.md) para detalhes.

## Exemplos

### Hello World

```hmp
SET nome TO "Mundo"
CALL log.print WITH message="Ola, ${nome}!"
```

### Calculadora

```hmp
FUNCTION somar(a, b)
    CALL math.sum WITH a=${a}, b=${b}
    RETURN ${last_result}
ENDFUNCTION

CALL somar WITH a=10, b=5
CALL log.print WITH message="10 + 5 = ${last_result}"
```

### Soma de Lista

```hmp
SET numeros TO [1, 2, 3, 4, 5]
SET soma TO 0

FOR EACH n IN ${numeros}
    SET soma TO ${soma + n}
ENDFOR

CALL log.print WITH message="Soma: ${soma}"
```

Mais exemplos em [`examples/`](examples/).

## Extensibilidade

Crie suas proprias tools:

```python
from hmp.tools.base import BaseTool, ToolProvider

class MinhaTool(BaseTool):
    @property
    def name(self) -> str:
        return "custom.minha_tool"
    
    @property
    def description(self) -> str:
        return "Descricao da minha tool"
    
    def invoke(self, params: dict, context) -> any:
        return f"Resultado: {params.get('valor')}"

class MeuProvider(ToolProvider):
    def get_tools(self):
        return [MinhaTool()]

# Registrar no engine
from hmp.core.engine import HMPEngine
engine = HMPEngine()
engine.registry.register_provider(MeuProvider())
```

## Documentacao

- [Guia de Sintaxe](docs/syntax.md) - Referencia completa da linguagem
- [Referencia de Tools](docs/tools-reference.md) - Todas as 64 tools documentadas
- [Arquitetura](docs/architecture.md) - Estrutura interna do framework
- [Protocolo HMP](HMP_PROTOCOL.txt) - Filosofia e objetivos do protocolo

## Estrutura do Projeto

```
HMP/
├── src/hmp/
│   ├── core/           # Motor de execucao
│   │   ├── engine.py   # Orquestrador principal
│   │   └── context.py  # Contexto de execucao
│   ├── expr/           # Avaliacao de expressoes
│   │   ├── cache.py    # Cache LRU de AST
│   │   └── evaluator.py# Avaliador seguro
│   ├── tools/          # Tools nativas (64)
│   │   ├── base.py     # Classes base
│   │   ├── registry.py # Registro de tools
│   │   └── *_tools.py  # Implementacoes
│   ├── runtime/        # Runtime e erros
│   ├── parser/         # Tokenizador
│   ├── contrib/        # Extensoes
│   └── cli/            # Interface CLI
├── tests/              # Testes unitarios e integracao
├── examples/           # Scripts de exemplo
├── docs/               # Documentacao
└── pyproject.toml      # Configuracao do projeto
```

## Desenvolvimento

```bash
# Instalar dependencias de dev
pip install -e ".[dev]"

# Rodar testes
python -m pytest tests/

# Verificar tipos
mypy src/hmp/

# Rodar demo
python run_demo.py
```

## Licenca

MIT

---

<p align="center">
  <strong>HMP - Human Machine Protocol</strong><br>
  A linguagem do pensamento estruturado.
</p>
