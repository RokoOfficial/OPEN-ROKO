# HMP - Referencia de Tools

Documentacao completa das 64 tools nativas do HMP.

## Indice

1. [math](#math-13-tools) - Operacoes matematicas
2. [string](#string-16-tools) - Manipulacao de strings
3. [list](#list-13-tools) - Operacoes com listas
4. [json](#json-2-tools) - Parse e stringify JSON
5. [date](#date-5-tools) - Data e hora
6. [http](#http-2-tools) - Requisicoes HTTP
7. [crypto](#crypto-2-tools) - Hash e UUID
8. [random](#random-3-tools) - Numeros aleatorios
9. [log](#log-2-tools) - Logging e debug
10. [system](#system-2-tools) - Sistema operacional
11. [meta](#meta-4-tools) - Metadados e introspeccao

---

## math (13 tools)

Operacoes matematicas.

### math.sum

Soma dois numeros.

```hmp
CALL math.sum WITH a=10, b=5
# Resultado: 15
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `a` | numero | Primeiro operando |
| `b` | numero | Segundo operando |

### math.subtract

Subtrai b de a.

```hmp
CALL math.subtract WITH a=20, b=8
# Resultado: 12
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `a` | numero | Minuendo |
| `b` | numero | Subtraendo |

### math.multiply

Multiplica dois numeros.

```hmp
CALL math.multiply WITH a=6, b=7
# Resultado: 42
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `a` | numero | Primeiro fator |
| `b` | numero | Segundo fator |

### math.divide

Divide a por b.

```hmp
CALL math.divide WITH a=100, b=4
# Resultado: 25
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `a` | numero | Dividendo |
| `b` | numero | Divisor (nao pode ser 0) |

### math.power

Eleva base ao expoente.

```hmp
CALL math.power WITH base=2, exponent=10
# Resultado: 1024
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `base` | numero | Base |
| `exponent` | numero | Expoente |

### math.mod

Retorna resto da divisao.

```hmp
CALL math.mod WITH a=17, b=5
# Resultado: 2
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `a` | numero | Dividendo |
| `b` | numero | Divisor |

### math.abs

Retorna valor absoluto.

```hmp
CALL math.abs WITH value=-42
# Resultado: 42
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `value` | numero | Numero |

### math.round

Arredonda numero.

```hmp
CALL math.round WITH value=3.14159, decimals=2
# Resultado: 3.14
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `value` | numero | Numero a arredondar |
| `decimals` | numero | Casas decimais (opcional, padrao 0) |

### math.floor

Arredonda para baixo.

```hmp
CALL math.floor WITH value=3.9
# Resultado: 3
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `value` | numero | Numero |

### math.ceil

Arredonda para cima.

```hmp
CALL math.ceil WITH value=3.1
# Resultado: 4
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `value` | numero | Numero |

### math.sqrt

Raiz quadrada.

```hmp
CALL math.sqrt WITH value=16
# Resultado: 4
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `value` | numero | Numero (>= 0) |

### math.min

Retorna menor valor de uma lista.

```hmp
CALL math.min WITH values=[5, 2, 8, 1, 9]
# Resultado: 1
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `values` | lista | Lista de numeros |

### math.max

Retorna maior valor de uma lista.

```hmp
CALL math.max WITH values=[5, 2, 8, 1, 9]
# Resultado: 9
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `values` | lista | Lista de numeros |

---

## string (16 tools)

Manipulacao de strings.

### string.concat

Concatena lista de strings.

```hmp
CALL string.concat WITH strings=["Ola", " ", "Mundo"]
# Resultado: "Ola Mundo"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `strings` | lista | Lista de strings |

### string.split

Divide string por separador.

```hmp
CALL string.split WITH text="a,b,c", separator=","
# Resultado: ["a", "b", "c"]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto a dividir |
| `separator` | string | Separador |

### string.join

Une lista com separador.

```hmp
CALL string.join WITH items=["a", "b", "c"], separator="-"
# Resultado: "a-b-c"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `items` | lista | Lista de strings |
| `separator` | string | Separador |

### string.upper

Converte para maiusculas.

```hmp
CALL string.upper WITH text="hello"
# Resultado: "HELLO"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |

### string.lower

Converte para minusculas.

```hmp
CALL string.lower WITH text="HELLO"
# Resultado: "hello"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |

### string.trim

Remove espacos das extremidades.

```hmp
CALL string.trim WITH text="  hello  "
# Resultado: "hello"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |

### string.length

Retorna tamanho da string.

```hmp
CALL string.length WITH text="Hello"
# Resultado: 5
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |

### string.substring

Extrai parte da string.

```hmp
CALL string.substring WITH text="Hello World", start=0, end=5
# Resultado: "Hello"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `start` | numero | Indice inicial |
| `end` | numero | Indice final (opcional) |

### string.replace

Substitui texto.

```hmp
CALL string.replace WITH text="ola mundo", old="mundo", new="HMP"
# Resultado: "ola HMP"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto original |
| `old` | string | Texto a substituir |
| `new` | string | Novo texto |

### string.contains

Verifica se contem substring.

```hmp
CALL string.contains WITH text="Hello World", search="World"
# Resultado: true
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `search` | string | Substring a buscar |

### string.startswith

Verifica se comeca com.

```hmp
CALL string.startswith WITH text="Hello World", prefix="Hello"
# Resultado: true
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `prefix` | string | Prefixo |

### string.endswith

Verifica se termina com.

```hmp
CALL string.endswith WITH text="Hello World", suffix="World"
# Resultado: true
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `suffix` | string | Sufixo |

### string.repeat

Repete string N vezes.

```hmp
CALL string.repeat WITH text="ab", count=3
# Resultado: "ababab"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `count` | numero | Numero de repeticoes |

### string.reverse

Inverte string.

```hmp
CALL string.reverse WITH text="hello"
# Resultado: "olleh"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |

### string.pad_left

Preenche a esquerda.

```hmp
CALL string.pad_left WITH text="5", length=3, char="0"
# Resultado: "005"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `length` | numero | Tamanho final |
| `char` | string | Caractere de preenchimento |

### string.pad_right

Preenche a direita.

```hmp
CALL string.pad_right WITH text="5", length=3, char="0"
# Resultado: "500"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `length` | numero | Tamanho final |
| `char` | string | Caractere de preenchimento |

---

## list (13 tools)

Operacoes com listas.

### list.length

Retorna tamanho da lista.

```hmp
CALL list.length WITH list=[1, 2, 3, 4, 5]
# Resultado: 5
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |

### list.get

Obtem item por indice.

```hmp
CALL list.get WITH list=["a", "b", "c"], index=1
# Resultado: "b"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `index` | numero | Indice (0-based) |

### list.set

Define item em indice.

```hmp
CALL list.set WITH list=["a", "b", "c"], index=1, value="X"
# Resultado: ["a", "X", "c"]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `index` | numero | Indice |
| `value` | any | Novo valor |

### list.push

Adiciona item ao final.

```hmp
CALL list.push WITH list=[1, 2], item=3
# Resultado: [1, 2, 3]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `item` | any | Item a adicionar |

### list.pop

Remove e retorna ultimo item.

```hmp
CALL list.pop WITH list=[1, 2, 3]
# Resultado: {"item": 3, "list": [1, 2]}
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |

### list.slice

Extrai parte da lista.

```hmp
CALL list.slice WITH list=[1, 2, 3, 4, 5], start=1, end=4
# Resultado: [2, 3, 4]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `start` | numero | Indice inicial |
| `end` | numero | Indice final (opcional) |

### list.contains

Verifica se contem item.

```hmp
CALL list.contains WITH list=[1, 2, 3], item=2
# Resultado: true
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `item` | any | Item a buscar |

### list.index

Retorna indice do item.

```hmp
CALL list.index WITH list=["a", "b", "c"], item="b"
# Resultado: 1
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `item` | any | Item a buscar |

### list.reverse

Inverte ordem da lista.

```hmp
CALL list.reverse WITH list=[1, 2, 3]
# Resultado: [3, 2, 1]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |

### list.sort

Ordena lista.

```hmp
CALL list.sort WITH list=[3, 1, 4, 1, 5]
# Resultado: [1, 1, 3, 4, 5]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |

### list.unique

Remove duplicatas.

```hmp
CALL list.unique WITH list=[1, 2, 2, 3, 3, 3]
# Resultado: [1, 2, 3]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |

### list.flatten

Achata lista aninhada.

```hmp
CALL list.flatten WITH list=[[1, 2], [3, 4], [5]]
# Resultado: [1, 2, 3, 4, 5]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista aninhada |

### list.filter

Filtra lista por condicao.

```hmp
SET numeros TO [1, 2, 3, 4, 5, 6]
CALL list.filter WITH list=${numeros}, condition="item > 3"
# Resultado: [4, 5, 6]
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |
| `condition` | string | Expressao de filtro |

---

## json (2 tools)

Parse e stringify JSON.

### json.parse

Converte string JSON para objeto.

```hmp
CALL json.parse WITH text='{"nome": "Ana", "idade": 25}'
# Resultado: {"nome": "Ana", "idade": 25}
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | String JSON |

### json.stringify

Converte objeto para string JSON.

```hmp
SET obj TO {"nome": "Ana", "idade": 25}
CALL json.stringify WITH value=${obj}
# Resultado: '{"nome": "Ana", "idade": 25}'
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `value` | any | Valor a converter |

---

## date (5 tools)

Operacoes com data e hora.

### date.now

Retorna data/hora atual.

```hmp
CALL date.now
# Resultado: "2024-12-02T15:30:00"
```

### date.format

Formata data.

```hmp
CALL date.format WITH date="2024-12-02", format="%d/%m/%Y"
# Resultado: "02/12/2024"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `date` | string | Data ISO |
| `format` | string | Formato (strftime) |

### date.parse

Converte string para data.

```hmp
CALL date.parse WITH text="02/12/2024", format="%d/%m/%Y"
# Resultado: "2024-12-02T00:00:00"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto da data |
| `format` | string | Formato de entrada |

### date.add

Adiciona tempo a data.

```hmp
CALL date.add WITH date="2024-12-02", days=7
# Resultado: "2024-12-09"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `date` | string | Data ISO |
| `days` | numero | Dias a adicionar |
| `hours` | numero | Horas (opcional) |
| `minutes` | numero | Minutos (opcional) |

### date.diff

Diferenca entre datas.

```hmp
CALL date.diff WITH date1="2024-12-02", date2="2024-12-09"
# Resultado: 7
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `date1` | string | Primeira data |
| `date2` | string | Segunda data |

---

## http (2 tools)

Requisicoes HTTP.

### http.get

Requisicao GET.

```hmp
CALL http.get WITH url="https://api.github.com/users/octocat"
# Resultado: {"login": "octocat", ...}
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `url` | string | URL da requisicao |
| `headers` | objeto | Headers (opcional) |

### http.post

Requisicao POST.

```hmp
CALL http.post WITH url="https://api.exemplo.com/dados", body={"nome": "teste"}
# Resultado: resposta do servidor
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `url` | string | URL da requisicao |
| `body` | objeto | Corpo da requisicao |
| `headers` | objeto | Headers (opcional) |

---

## crypto (2 tools)

Criptografia e hashing.

### crypto.hash

Gera hash de texto.

```hmp
CALL crypto.hash WITH text="senha123", algorithm="sha256"
# Resultado: "ef92b778..."
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `text` | string | Texto |
| `algorithm` | string | Algoritmo (md5, sha256) |

### crypto.uuid

Gera UUID unico.

```hmp
CALL crypto.uuid
# Resultado: "550e8400-e29b-41d4-a716-446655440000"
```

---

## random (3 tools)

Numeros aleatorios.

### random.number

Gera numero aleatorio.

```hmp
CALL random.number WITH min=1, max=100
# Resultado: 42 (aleatorio)
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `min` | numero | Minimo (opcional, padrao 0) |
| `max` | numero | Maximo (opcional, padrao 1) |

### random.choice

Escolhe item aleatorio de lista.

```hmp
CALL random.choice WITH items=["a", "b", "c"]
# Resultado: "b" (aleatorio)
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `items` | lista | Lista de opcoes |

### random.shuffle

Embaralha lista.

```hmp
CALL random.shuffle WITH list=[1, 2, 3, 4, 5]
# Resultado: [3, 1, 5, 2, 4] (aleatorio)
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `list` | lista | Lista |

---

## log (2 tools)

Logging e debug.

### log.print

Imprime mensagem no console.

```hmp
CALL log.print WITH message="Ola mundo!"
# Saida: [LOG] Ola mundo!
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `message` | string | Mensagem |

### log.write

Escreve log estruturado.

```hmp
CALL log.write WITH level="info", message="Operacao concluida"
# Saida: [INFO] Operacao concluida
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `level` | string | Nivel (info, warn, error) |
| `message` | string | Mensagem |

---

## system (2 tools)

Sistema operacional.

### system.env

Obtem variavel de ambiente.

```hmp
CALL system.env WITH name="USER"
# Resultado: "usuario"
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `name` | string | Nome da variavel |

**Variaveis permitidas:** USER, HOME, PATH, LANG, SHELL, TERM, PWD, HOSTNAME

### system.sleep

Pausa execucao.

```hmp
CALL system.sleep WITH seconds=2
# Pausa por 2 segundos
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `seconds` | numero | Segundos (maximo 5) |

---

## meta (4 tools)

Metadados e introspeccao.

### meta.version

Retorna versao do HMP.

```hmp
CALL meta.version
# Resultado: "3.0.0"
```

### meta.tools

Lista todas as tools disponiveis.

```hmp
CALL meta.tools
# Resultado: ["math.sum", "math.subtract", ...]
```

### meta.metrics

Retorna metricas de execucao.

```hmp
CALL meta.metrics
# Resultado: {"iterations": 100, "tools_called": 15, ...}
```

### meta.cache_stats

Estatisticas do cache de expressoes.

```hmp
CALL meta.cache_stats
# Resultado: {"hits": 50, "misses": 10, "size": 60}
```

---

Voltar para [README](../README.md) | Ver [Sintaxe](syntax.md) | Ver [Arquitetura](architecture.md)
