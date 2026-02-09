# OPENROKOS — Cognitive Operating System

**OPENROKOS** é um **Cognitive Operating System** para automação de fluxos complexos com foco em **determinismo, rastreabilidade e segurança**. Ele combina uma linguagem declarativa própria (HMP), um motor de execução confiável e uma API para integrações em escala.

> Missão: tornar automações críticas auditáveis, previsíveis e fáceis de manter.

---

## ✨ Destaques

- **Linguagem declarativa (HMP)** com controle de fluxo completo, funções e módulos.
- **Ferramentas nativas** para operações matemáticas, strings, listas, JSON, HTTP e mais.
- **API REST** para execução de scripts e chamadas de tools.
- **Pronto para produção** com execução determinística e logs consistentes.

---

## 🚀 Início rápido

### 1) Execute um script HMP localmente

```bash
cd HMP
PYTHONPATH=src python -m hmp.cli.main run examples/hello_world.hmp
```

### 2) Suba a API REST

```bash
python api/server.py
# Acesse: http://localhost:5000
```

### 3) Execute via API

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

## 🧠 HMP Engine (High-level Modular Protocol)

### Recursos principais

| Recurso | Descrição |
| :--- | :--- |
| **Estruturas de controle** | `IF/ELSE`, `LOOP`, `WHILE`, `FOR EACH` |
| **Modularidade** | `IMPORT` com namespaces |
| **Funções** | Definição e execução de funções com parâmetros |
| **Tratamento de erros** | Blocos `TRY/CATCH` |
| **Paralelismo** | Blocos `PARALLEL` |

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
| **log** | `print`, `write` |
| **system** | `env`, `sleep` |
| **meta** | `version`, `tools`, `metrics` |

---

## 🏗️ Arquitetura do projeto

```
OPEN-ROKOS/
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
| `HMP/examples/` | Exemplos funcionais de scripts |

---

## 🤝 Comunidade e contribuição

Contribuições são bem-vindas! Se você quiser reportar bugs, sugerir melhorias ou abrir PRs:

1. Faça um fork do repositório
2. Crie sua branch com a proposta
3. Envie um Pull Request com contexto e testes

---

## 🧭 Roadmap

- [ ] Testes aprofundados para `IMPORT`
- [ ] `IMPORT` com wildcard (`*.hmp`)
- [ ] Marketplace de módulos
- [ ] Web IDE integrada
- [ ] Debug visual e profiling

---

## 📜 Licença

Este projeto é distribuído sob a licença descrita em `LICENSE`.

---

*The language of structured thought. The bridge between AI and real action.*
