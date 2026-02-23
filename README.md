# OPEN-ROKO — Cognitive Operating System

**OPEN-ROKO** é um **Cognitive Operating System** para automação de fluxos complexos com foco em **determinismo, rastreabilidade e segurança**. Ele combina uma linguagem declarativa própria (HMP), um motor de execução confiável e uma API para integrações em escala.

> Missão: tornar automações críticas auditáveis, previsíveis e fáceis de manter.

---

## ✨ Destaques

- **Linguagem declarativa (HMP)** com controle de fluxo completo, funções e módulos.
- **Ferramentas nativas** para operações matemáticas, strings, listas, JSON, HTTP e mais.
- **API REST** para execução de scripts e chamadas de tools.
- **Pronto para produção** com execução determinística e logs consistentes.

---

## 🧠 HMP Engine (High-level Modular Protocol)

OPEN-ROKO é um motor de script flexível e extensível, projetado para automatizar tarefas e orquestrar fluxos de trabalho usando uma linguagem de script simples e intuitiva. Ele permite a definição de variáveis, chamadas de ferramentas, estruturas de controle (condicionais, loops) e funções, tornando-o ideal para prototipagem rápida e automação de processos.

### Recursos principais

| Recurso | Descrição |
| :--- | :--- |
| **Linguagem de Script Simples** | Sintaxe clara e fácil de aprender para definir lógica de automação. |
| **Variáveis e Expressões** | Suporte a variáveis, tipos de dados básicos (strings, números, booleanos, listas) e expressões matemáticas/lógicas. |
| **Interpolação de Strings** | Permite a inclusão dinâmica de valores de variáveis em strings (ex: `"Olá, ${nome}!"`). |
| **Ferramentas Extensíveis** | Capacidade de integrar e chamar ferramentas externas para estender a funcionalidade do motor. |
| **Estruturas de controle** | `IF/THEN/ELSE`, `LOOP/TIMES`, `WHILE`, `FOR EACH/IN` para controle de fluxo. |
| **Funções** | Definição e execução de funções com parâmetros. |
| **Tratamento de erros** | Blocos `TRY/CATCH` para gerenciar exceções durante a execução. |
| **Paralelismo** | Blocos `PARALLEL` para execução concorrente de tarefas. |
| **Modularidade** | `IMPORT` com namespaces para organização do código em módulos separados. |

### Toolset nativo

O HMP oferece um conjunto robusto de tools por categoria:

| Categoria | Exemplos |
| :--- | :--- |
| **math** | `sum`, `multiply`, `divide`, `sqrt`, `pow`, `abs` |
| **string** | `upper`, `lower`, `trim`, `concat`, `split` |
| **list** | `push`, `pop`, `get`, `sort`, `filter`, `reverse` |
| **json** | `parse`, `stringify` |
| **date** | `now`, `format`, `parse`, `add`, `diff` |
| **http** | `get`, `post` |
| **crypto** | `hash`, `uuid` |
| **random** | `number`, `choice`, `shuffle` |
| **log** | `info`, `warn`, `error` |
| **system** | `env`, `sleep` |
| **meta** | `version`, `tools`, `metrics` |

---

## 🚀 Início rápido

### Instalação

Para instalar o OPEN-ROKO, clone o repositório e instale as dependências Python:

```bash
git clone https://github.com/RokoOfficial/OPEN-ROKO.git
cd OPEN-ROKO/HMP
sudo pip3 install -r requirements.txt
```

### Uso Básico

Para executar um script HMP, você pode usar o `HMPEngine`:

```python
from hmp.core.engine import HMPEngine

script_code = """
SET nome TO "Mundo"
CALL log.info WITH message="Olá, ${nome}!"
"""

engine = HMPEngine()
result = engine.execute(script_code)

if result["success"]:
    print("Script executado com sucesso!")
    print("Variáveis finais:", result["variables"])
else:
    print("Erro na execução do script:", result["error"])
```

### Exemplo de Script HMP

```hmp
# Define uma variável
SET contador TO 0

# Loop 5 vezes
LOOP 5 TIMES
    SET contador TO ${contador + 1}
    CALL log.info WITH message="Contador: ${contador}"
ENDLOOP

# Condicional
IF ${contador} > 3 THEN
    CALL log.info WITH message="Contador é maior que 3."
ELSE
    CALL log.info WITH message="Contador é 3 ou menos."
ENDIF

# Definição e chamada de função
FUNCTION somar(a, b)
    RETURN ${a + b}
ENDFUNCTION

CALL somar WITH a=10, b=20 AS resultado_soma
CALL log.info WITH message="Resultado da soma: ${resultado_soma}"

# Tratamento de erro
TRY
    CALL tool.nao_existente WITH param="valor"
CATCH erro
    CALL log.error WITH message="Erro capturado: ${erro}"
ENDTRY
```

### Subindo a API REST

```bash
python api/server.py
# Acesse: http://localhost:5000
```

### Executando via API

**Script HMP:**
```bash
curl -X POST http://localhost:5000/run \
  -d '{"script": "SET x TO 10\nCALL log.print WITH message=\"Hello!\""}'
```

**Tool específica:**
```bash
curl -X POST http://localhost:5000/tool/math.sum \
  -d '{"a": 10, "b": 5}'
```

---

## 🏗️ Arquitetura do projeto

```
OPEN-ROKO/
├── api/                      # API REST (Flask) e interface web
│   ├── server.py             # Servidor principal
│   └── templates/            # Templates HTML/CSS
│
├── HMP/                      # Motor e linguagem HMP
│   ├── src/hmp/              # Código do interpretador
│   ├── examples/             # Exemplos HMP
│   └── docs/                 # Documentação técnica
│
└── tools/                    # Ferramentas auxiliares
    └── hmp_client.py         # Cliente Python para a API
```

---

## 📚 Documentação

| Documento | Conteúdo |
| :--- | :--- |
| `HMP/docs/syntax.md` | Referência completa da sintaxe HMP |
| `HMP/docs/tools-reference.md` | Documentação das ferramentas nativas |
| `HMP/docs/architecture.md` | Visão geral da arquitetura do projeto |
| `HMP/examples/` | Exemplos funcionais de scripts |

---

## 🤝 Comunidade e contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório do GitHub.

---

## 📜 Licença

Este projeto é distribuído sob a licença descrita em `LICENSE`.

---

*The language of structured thought. The bridge between AI and real action.*
