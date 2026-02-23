# Referência de Ferramentas (Tools) do HMP

O OPEN-ROKO HMP Engine vem com um conjunto robusto de ferramentas nativas, organizadas por categoria, que podem ser invocadas usando o comando `CALL`. Essas ferramentas estendem a funcionalidade da linguagem, permitindo interações com o sistema, operações matemáticas, manipulação de dados e muito mais.

## Como Usar Ferramentas

Para chamar uma ferramenta, use a sintaxe `CALL <categoria>.<nome_da_ferramenta> WITH <parametro1>=<valor1>, <parametro2>=<valor2> AS <variavel_de_destino>`.

- `<categoria>`: O grupo ao qual a ferramenta pertence (ex: `math`, `string`, `log`).
- `<nome_da_ferramenta>`: O nome específico da ferramenta a ser executada (ex: `sum`, `upper`, `info`).
- `WITH`: Palavra-chave opcional para passar parâmetros nomeados.
- `<parametro>=<valor>`: Pares de chave-valor para os argumentos da ferramenta. Os valores podem ser literais ou expressões HMP.
- `AS <variavel_de_destino>`: Opcional. Atribui o resultado da ferramenta a uma variável específica. Se omitido, o resultado estará disponível em `last_result`.

### Exemplo:

```hmp
# Chama a ferramenta 'sum' da categoria 'math' com parâmetros 'a' e 'b'
CALL math.sum WITH a=10, b=5 AS total
CALL log.info WITH message="A soma é: ${total}"

# Chama uma ferramenta sem parâmetros e usa o last_result
CALL crypto.uuid
CALL log.info WITH message="UUID gerado: ${last_result}"
```

## Ferramentas Nativas por Categoria

### `math` - Operações Matemáticas

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `sum` | Soma dois ou mais números. | `a` (número), `b` (número), `...` | `CALL math.sum WITH a=10, b=20` |
| `multiply` | Multiplica dois ou mais números. | `a` (número), `b` (número), `...` | `CALL math.multiply WITH a=5, b=5` |
| `divide` | Divide dois números. | `a` (dividendo), `b` (divisor) | `CALL math.divide WITH a=100, b=10` |
| `sqrt` | Calcula a raiz quadrada de um número. | `value` (número) | `CALL math.sqrt WITH value=25` |
| `pow` | Calcula a potência de um número. | `base` (número), `exp` (expoente) | `CALL math.pow WITH base=2, exp=3` |
| `abs` | Retorna o valor absoluto de um número. | `value` (número) | `CALL math.abs WITH value=-10` |

### `string` - Manipulação de Strings

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `upper` | Converte uma string para maiúsculas. | `value` (string) | `CALL string.upper WITH value="hello"` |
| `lower` | Converte uma string para minúsculas. | `value` (string) | `CALL string.lower WITH value="WORLD"` |
| `trim` | Remove espaços em branco do início e fim de uma string. | `value` (string) | `CALL string.trim WITH value="  texto  "` |
| `concat` | Concatena várias strings ou elementos de uma lista. | `strings` (lista de strings) | `CALL string.concat WITH strings=["Olá", " ", "Mundo"]` |
| `split` | Divide uma string em uma lista de substrings. | `value` (string), `delimiter` (string) | `CALL string.split WITH value="a,b,c", delimiter=","` |

### `list` - Operações com Listas

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `push` | Adiciona um elemento ao final de uma lista. | `list` (lista), `item` (qualquer tipo) | `CALL list.push WITH list=${minha_lista}, item="novo"` |
| `pop` | Remove e retorna o último elemento de uma lista. | `list` (lista) | `CALL list.pop WITH list=${minha_lista}` |
| `get` | Retorna um elemento da lista pelo índice. | `list` (lista), `index` (número) | `CALL list.get WITH list=${minha_lista}, index=0` |
| `sort` | Ordena uma lista. | `list` (lista), `reverse` (booleano, opcional) | `CALL list.sort WITH list=${numeros}` |
| `filter` | Filtra elementos de uma lista com base em uma condição (não implementado nativamente, usar `FOR EACH` com `IF`). | N/A | N/A |
| `reverse` | Inverte a ordem dos elementos em uma lista. | `list` (lista) | `CALL list.reverse WITH list=${minha_lista}` |

### `json` - Manipulação JSON

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `parse` | Converte uma string JSON em um objeto HMP (dicionário/lista). | `value` (string JSON) | `CALL json.parse WITH value="{\"chave\": \"valor\"}"` |
| `stringify` | Converte um objeto HMP (dicionário/lista) em uma string JSON. | `value` (objeto HMP) | `CALL json.stringify WITH value=${meu_objeto}` |

### `date` - Operações com Datas e Horas

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `now` | Retorna a data e hora atual. | N/A | `CALL date.now` |
| `format` | Formata uma data/hora. | `date` (data/hora), `format_str` (string de formato) | `CALL date.format WITH date=${agora}, format_str="%Y-%m-%d"` |
| `parse` | Converte uma string em data/hora. | `value` (string), `format_str` (string de formato) | `CALL date.parse WITH value="2024-01-01", format_str="%Y-%m-%d"` |
| `add` | Adiciona um período a uma data/hora. | `date` (data/hora), `unit` (string), `amount` (número) | `CALL date.add WITH date=${agora}, unit="days", amount=7` |
| `diff` | Calcula a diferença entre duas datas/horas. | `date1` (data/hora), `date2` (data/hora), `unit` (string) | `CALL date.diff WITH date1=${data_futura}, date2=${data_passada}, unit="hours"` |

### `http` - Requisições HTTP

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `get` | Realiza uma requisição HTTP GET. | `url` (string), `headers` (dicionário, opcional), `params` (dicionário, opcional) | `CALL http.get WITH url="https://api.example.com/data"` |
| `post` | Realiza uma requisição HTTP POST. | `url` (string), `body` (string/dicionário, opcional), `headers` (dicionário, opcional) | `CALL http.post WITH url="https://api.example.com/submit", body="{\"key\":\"value\"}"` |

### `crypto` - Funções Criptográficas

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `hash` | Gera um hash de uma string (ex: SHA256). | `value` (string), `algorithm` (string, ex: "sha256") | `CALL crypto.hash WITH value="senha", algorithm="sha256"` |
| `uuid` | Gera um UUID (Universally Unique Identifier) v4. | N/A | `CALL crypto.uuid` |

### `random` - Geração de Valores Aleatórios

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `number` | Gera um número inteiro aleatório dentro de um intervalo. | `min` (número), `max` (número) | `CALL random.number WITH min=1, max=100` |
| `choice` | Escolhe um elemento aleatório de uma lista. | `list` (lista) | `CALL random.choice WITH list=["a", "b", "c"]` |
| `shuffle` | Embaralha os elementos de uma lista. | `list` (lista) | `CALL random.shuffle WITH list=${minha_lista}` |

### `log` - Registro de Informações

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `info` | Registra uma mensagem informativa. | `message` (string) | `CALL log.info WITH message="Operação concluída."` |
| `warn` | Registra uma mensagem de aviso. | `message` (string) | `CALL log.warn WITH message="Recurso obsoleto."` |
| `error` | Registra uma mensagem de erro. | `message` (string) | `CALL log.error WITH message="Falha na conexão."` |

### `system` - Interações com o Sistema

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `env` | Retorna o valor de uma variável de ambiente. | `name` (string) | `CALL system.env WITH name="PATH"` |
| `sleep` | Pausa a execução do script por um número de segundos. | `seconds` (número) | `CALL system.sleep WITH seconds=5` |

### `meta` - Informações do Motor

| Ferramenta | Descrição | Parâmetros | Exemplo |
| :--- | :--- | :--- | :--- |
| `version` | Retorna a versão do HMP Engine. | N/A | `CALL meta.version` |
| `tools` | Lista todas as ferramentas disponíveis. | N/A | `CALL meta.tools` |
| `metrics` | Retorna métricas de execução (uso de memória, tempo, etc.). | N/A | `CALL meta.metrics` |

---

Voltar para [README](../../README.md) | Ver [Sintaxe](syntax.md)
