# OPENROKOS - Cognitive Operating System

**OPENROKOS** is a **Cognitive Operating System** designed for **complex workflow automation** with a focus on **total traceability** and **100% deterministic results**. It provides a robust platform for executing complex business logic, combining a powerful declarative language with a comprehensive set of native tools.

## 🚀 Project Status

The project is in a **functional, tested, and clean** state, ready for use in production environments.

## 💡 Key Features

OPENROKOS is built around three main pillars: the **HMP Engine**, the **REST API**, and a supporting **Web Interface**.

### 1. HMP Engine - Declarative Language

**HMP (High-level Modular Protocol)** is the core declarative language of the system.

| Feature | Description |
| :--- | :--- |
| **Control Structures** | Full support for `IF/ELSE`, `LOOP`, `WHILE`, and `FOR EACH`. |
| **Modularity** | `IMPORT` functionality for reusable modules, promoting organization and DRY (Don't Repeat Yourself) principles. |
| **Functions** | Definition of reusable functions with parameters. |
| **Error Handling** | `TRY/CATCH` blocks for robust exception management. |
| **Parallelism** | Task execution in parallel with the `PARALLEL` block, optimizing performance. |

### 2. Native Toolset

The HMP Engine features a set of **64 native tools** covering various automation needs.

| Category | Count | Example Tools |
| :--- | :--- | :--- |
| **math** | 13 | `sum`, `multiply`, `divide`, `sqrt`, `pow`, `abs` |
| **string** | 16 | `upper`, `lower`, `trim`, `concat`, `split` |
| **list** | 13 | `push`, `pop`, `get`, `sort`, `filter`, `reverse` |
| **json** | 2 | `parse`, `stringify` |
| **date** | 5 | `now`, `format`, `parse`, `add`, `diff` |
| **http** | 2 | `get`, `post` |
| **crypto** | 2 | `hash`, `uuid` |
| **random** | 3 | `number`, `choice`, `shuffle` |
| **log** | 2 | `print`, `write` |
| **system** | 2 | `env`, `sleep` |
| **meta** | 4 | `version`, `tools`, `metrics` |

### 3. REST API and Web Interface

A complete REST API allows for programmatic integration with the system, while the web interface offers a **professional landing page**, **comprehensive documentation**, and an **interactive demo**.

## 💻 Repository Structure

The project structure is organized for clarity and maintenance:

```
OPEN-ROKOS/
├── api/                      # REST API (Flask) and Web Interface (HTML/CSS)
│   ├── server.py             # Main API server
│   └── templates/            # Web interface HTML files
│
├── HMP/                      # HMP Engine (High-level Modular Protocol)
│   ├── src/hmp/              # Interpreter source code
│   ├── examples/             # HMP script examples
│   └── docs/                 # HMP technical documentation
│
└── tools/                    # Support tools
    └── hmp_client.py         # Python client for API interaction
```

## 🛠️ Getting Started

To start OPENROKOS and begin executing scripts:

### 1. Start the API Server

The API server is Flask-based and runs on port 5000 by default.

```bash
python api/server.py
# Accessible at: http://localhost:5000
```

### 2. Execute an HMP Script Locally

You can run HMP scripts directly via the command line:

```bash
cd HMP
PYTHONPATH=src python -m hmp.cli.main run examples/hello_world.hmp
```

### 3. Use the REST API

The API allows for script execution and direct tool calls:

**Execute a script:**
```bash
curl -X POST http://localhost:5000/run \
  -d '{"script": "SET x TO 10\nCALL log.print WITH message=\"Hello!\""}'
```

**Call a tool (example: `math.sum`):**
```bash
curl -X POST http://localhost:5000/tool/math.sum \
  -d '{"a": 10, "b": 5}'
```

## 📚 Additional Documentation

| File | Content |
| :--- | :--- |
| `HMP/docs/syntax.md` | Complete HMP syntax reference. |
| `HMP/examples/` | Collection of functional HMP examples. |

## 🎯 Design Philosophy

HMP was conceived to overcome the limitations of pure LLM-based systems in critical automation, ensuring:

1.  **Determinism:** The same input always produces the same output, essential for trust in automation.
2.  **Auditability:** Every execution step is logged and traceable.
3.  **Security:** Rigorous control and isolation of execution.
4.  **Extensibility:** Ease of adding new tools and modules.
5.  **Scalability:** Optimized for parallel task execution.

## 🔮 Next Steps

The development roadmap includes:

- [ ] Implementation of comprehensive unit tests for the `IMPORT` functionality.
- [ ] Support for wildcard `IMPORT` (`*.hmp`).
- [ ] Creation of an HMP module marketplace.
- [ ] Development of an integrated web IDE for editing and execution.
- [ ] Implementation of visual debugging tools and performance profiling.

---

*The language of structured thought. The bridge between AI and real action.*
