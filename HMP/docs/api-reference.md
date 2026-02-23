# HMP API Reference

REST API para o Human Machine Protocol (HMP).

**Versao:** 2.0.0  
**Base URL:** `https://sua-app.replit.app` ou `http://localhost:5000`

---

## Visao Geral

A HMP API permite:
- Executar scripts HMP via HTTP
- Gerenciar arquivos .hmp (upload, edicao, remocao)
- Chamar qualquer uma das 64 tools diretamente
- Integrar o HMP em qualquer aplicacao

---

## Autenticacao

Atualmente a API nao requer autenticacao. Todas as rotas sao publicas.

---

## Endpoints

### Health Check

```
GET /
```

Retorna informacoes da API e status.

**Resposta:**
```json
{
  "name": "HMP API",
  "version": "2.0.0",
  "description": "REST API para o Human Machine Protocol",
  "total_tools": 64,
  "status": "online",
  "endpoints": { ... }
}
```

---

### Tools

#### Listar Todas as Tools

```
GET /tools
```

**Resposta:**
```json
{
  "total": 64,
  "categories": {
    "math": ["math.sum", "math.subtract", ...],
    "string": ["string.upper", "string.lower", ...],
    ...
  }
}
```

#### Listar Tools por Categoria

```
GET /tools/<categoria>
```

**Exemplo:** `GET /tools/math`

**Resposta:**
```json
{
  "category": "math",
  "count": 13,
  "tools": ["math.sum", "math.subtract", "math.multiply", ...]
}
```

#### Executar Tool Diretamente

```
POST /tool/<nome_da_tool>
```

**Exemplo:** `POST /tool/math.sum`

**Body:**
```json
{
  "a": 10,
  "b": 5
}
```

**Resposta:**
```json
{
  "success": true,
  "tool": "math.sum",
  "result": 15.0
}
```

---

### Execucao de Scripts

#### Executar Script Inline

```
POST /run
```

**Body:**
```json
{
  "script": "SET x TO 10\nSET y TO 20\nCALL math.sum WITH a=${x}, b=${y}\nRETURN ${last_result[\"default\"]}"
}
```

**Resposta:**
```json
{
  "success": true,
  "output": [
    "SET x = 10",
    "SET y = 20",
    "[CALL] math.sum -> 30.0",
    "RETURN: 30.0"
  ],
  "variables": {
    "x": 10,
    "y": 20
  },
  "return_value": 30.0
}
```

#### Executar Arquivo HMP

```
POST /run/file/<filename>
```

**Exemplo:** `POST /run/file/hello_world.hmp`

**Body (opcional):**
```json
{
  "variables": {
    "nome": "Noka",
    "valor": 100
  }
}
```

**Resposta:**
```json
{
  "success": true,
  "filename": "hello_world.hmp",
  "output": ["..."],
  "variables": { ... },
  "return_value": "..."
}
```

---

### Gerenciamento de Arquivos

#### Listar Arquivos Disponiveis

```
GET /files
```

**Resposta:**
```json
{
  "count": 7,
  "files": [
    {"name": "hello_world.hmp", "size": 624, "source": "examples"},
    {"name": "meu_script.hmp", "size": 150, "source": "user"}
  ]
}
```

#### Upload de Arquivo

```
POST /files/upload
```

**Body:**
```json
{
  "filename": "meu_script.hmp",
  "content": "SET x TO 10\nCALL log.print WITH message=\"Valor: ${x}\"\nRETURN ${x * 2}"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Arquivo 'meu_script.hmp' criado com sucesso",
  "filename": "meu_script.hmp",
  "size": 75
}
```

#### Obter Conteudo de Arquivo

```
GET /files/<filename>
```

**Resposta:**
```json
{
  "filename": "meu_script.hmp",
  "content": "SET x TO 10\n...",
  "source": "user"
}
```

#### Atualizar Arquivo

```
PUT /files/<filename>
```

**Body:**
```json
{
  "content": "SET x TO 20\nRETURN ${x}"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Arquivo 'meu_script.hmp' salvo com sucesso",
  "filename": "meu_script.hmp",
  "size": 25
}
```

#### Remover Arquivo

```
DELETE /files/<filename>
```

**Resposta:**
```json
{
  "success": true,
  "message": "Arquivo 'meu_script.hmp' removido com sucesso"
}
```

> **Nota:** Apenas arquivos do usuario podem ser removidos. Arquivos de exemplo sao protegidos.

---

### Endpoints Rapidos

Atalhos para operacoes comuns:

| Endpoint | Metodo | Descricao |
|----------|--------|-----------|
| `/math/sum?a=X&b=Y` | GET/POST | Soma dois numeros |
| `/math/multiply?a=X&b=Y` | GET/POST | Multiplica dois numeros |
| `/string/upper?text=X` | GET/POST | Converte para maiusculas |
| `/string/lower?text=X` | GET/POST | Converte para minusculas |
| `/date/now` | GET | Data/hora atual |
| `/random/number?min=X&max=Y` | GET/POST | Numero aleatorio |
| `/crypto/hash` | POST | Gera hash de texto |
| `/list/length` | POST | Tamanho de uma lista |
| `/json/parse` | POST | Parse de JSON |

---

## Codigos de Erro

| Codigo | Descricao |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Requisicao invalida (parametros faltando) |
| 403 | Proibido (ex: deletar arquivo de exemplo) |
| 404 | Nao encontrado |
| 500 | Erro interno do servidor |

**Formato de erro:**
```json
{
  "error": "Descricao do erro",
  "available": ["lista", "de", "opcoes"]
}
```

---

## Exemplos com cURL

### Executar script simples
```bash
curl -X POST https://sua-api.replit.app/run \
  -H "Content-Type: application/json" \
  -d '{"script": "SET x TO 42\nRETURN ${x * 2}"}'
```

### Criar e executar arquivo
```bash
# Criar arquivo
curl -X POST https://sua-api.replit.app/files/upload \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "teste.hmp",
    "content": "SET nome TO \"API\"\nCALL log.print WITH message=\"Ola, ${nome}!\"\nRETURN \"OK\""
  }'

# Executar arquivo
curl -X POST https://sua-api.replit.app/run/file/teste.hmp \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Chamar tool diretamente
```bash
curl -X POST https://sua-api.replit.app/tool/string.upper \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'
```

---

## Cliente Python

Use o cliente Python para integrar facilmente:

```python
from hmp_client import HMPClient

client = HMPClient("https://sua-api.replit.app")

# Executar script
result = client.run_script('SET x TO 10\nRETURN ${x * 2}')
print(result['return_value'])  # 20

# Executar arquivo
result = client.run_file('hello_world.hmp')
print(result['output'])

# Chamar tools
print(client.math_sum(10, 5))       # 15.0
print(client.string_upper('ola'))   # OLA
print(client.crypto_uuid())         # uuid gerado

# Listar arquivos
files = client.list_files()
print(files['count'])
```

---

## Categorias de Tools

| Categoria | Qtd | Descricao |
|-----------|-----|-----------|
| math | 13 | Operacoes matematicas |
| string | 16 | Manipulacao de texto |
| list | 13 | Operacoes com listas |
| json | 2 | Parse e stringify JSON |
| date | 5 | Data e hora |
| http | 2 | Requisicoes HTTP |
| crypto | 2 | Hash e UUID |
| random | 3 | Numeros aleatorios |
| log | 2 | Log e debug |
| system | 2 | Variaveis de ambiente |
| meta | 4 | Introspeccao |

Para lista completa, consulte `docs/tools-reference.md`.
