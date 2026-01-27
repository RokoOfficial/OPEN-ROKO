# HMP - Guia de Sintaxe

Referencia completa da sintaxe da linguagem HMP.

## Indice

1. [Variaveis](#variaveis)
2. [Expressoes](#expressoes)
3. [Chamada de Tools](#chamada-de-tools)
4. [Importacao de Modulos](#importacao-de-modulos)
5. [Condicionais](#condicionais)
6. [Loops](#loops)
7. [Funcoes](#funcoes)
8. [Tratamento de Erros](#tratamento-de-erros)
9. [Execucao Paralela](#execucao-paralela)
10. [Variaveis Especiais](#variaveis-especiais)

---

## Variaveis

### SET - Definir Variaveis

```
SET <nome> TO <valor>
```

#### Tipos de Valores

```hmp
# String
SET nome TO "Maria"
SET cidade TO 'Sao Paulo'

# Numero inteiro
SET idade TO 25

# Numero decimal
SET preco TO 19.99

# Booleano
SET ativo TO true
SET finalizado TO false

# Lista
SET frutas TO ["maca", "banana", "laranja"]
SET numeros TO [1, 2, 3, 4, 5]

# Lista mista
SET dados TO ["texto", 123, true]
```

#### Expressoes em Variaveis

```hmp
# Referencia a variavel
SET copia TO ${nome}

# Expressao matematica
SET dobro TO ${idade * 2}
SET soma TO ${a + b + c}

# Interpolacao de string
SET saudacao TO "Ola, ${nome}!"
SET info TO "Idade: ${idade} anos"

# Acesso a lista
SET primeiro TO ${frutas[0]}
SET ultimo TO ${numeros[4]}

# Resultado de CALL anterior
SET resultado TO ${last_result}
```

#### Regras de Nomenclatura

- Letras, numeros e underscore (_)
- Nao pode comecar com numero
- Case-sensitive (`nome` != `Nome`)

---

## Expressoes

Expressoes sao avaliadas dentro de `${...}`

### Operadores Aritmeticos

| Operador | Descricao | Exemplo |
|----------|-----------|---------|
| `+` | Adicao | `${5 + 3}` = 8 |
| `-` | Subtracao | `${10 - 4}` = 6 |
| `*` | Multiplicacao | `${6 * 7}` = 42 |
| `/` | Divisao | `${20 / 4}` = 5 |
| `%` | Modulo | `${17 % 5}` = 2 |
| `**` | Potencia | `${2 ** 8}` = 256 |

### Operadores de Comparacao

| Operador | Descricao | Exemplo |
|----------|-----------|---------|
| `==` | Igual | `${x == 5}` |
| `!=` | Diferente | `${x != 0}` |
| `>` | Maior | `${x > 10}` |
| `<` | Menor | `${x < 100}` |
| `>=` | Maior ou igual | `${x >= 18}` |
| `<=` | Menor ou igual | `${x <= 65}` |

### Operadores Logicos

| Operador | Descricao | Exemplo |
|----------|-----------|---------|
| `AND` | E logico | `${x > 0 AND x < 100}` |
| `OR` | Ou logico | `${x == 0 OR x == 1}` |
| `NOT` | Negacao | `${NOT encontrado}` |

### Acesso a Dados

```hmp
# Acesso a lista por indice
SET lista TO [10, 20, 30]
SET item TO ${lista[1]}          # 20

# Acesso a dicionario por chave
SET obj TO {"nome": "Ana", "idade": 25}
SET nome TO ${obj["nome"]}       # "Ana"

# Acesso aninhado
SET dados TO {"user": {"nome": "Bob"}}
SET nome TO ${dados["user"]["nome"]}  # "Bob"
```

---

## Importacao de Modulos

### IMPORT - Importar Funcoes de Outros Arquivos

```
IMPORT "<arquivo>"
IMPORT "<arquivo>" AS <namespace>
```

#### Exemplo 1: Sem Namespace

```hmp
IMPORT "utils.hmp"

CALL dobro WITH valor=5
SET resultado TO ${last_result}
```

#### Exemplo 2: Com Namespace

```hmp
IMPORT "utils.hmp" AS math

CALL math.dobro WITH valor=5
```

#### Vantagens
- Reutilizar codigo entre scripts
- Organizar em modulos
- Evitar duplicacao

---

## Chamada de Tools

### CALL - Invocar Tools

```
CALL <categoria>.<tool> WITH <param1>=<valor1>, <param2>=<valor2>
```

#### Exemplos

```hmp
# Sem parametros
CALL crypto.uuid

# Com parametros
CALL math.sum WITH a=10, b=5

# Com variaveis
SET x TO 100
CALL math.multiply WITH a=${x}, b=2

# Com string
CALL log.print WITH message="Ola mundo!"

# Com lista
CALL string.concat WITH strings=["Ola", " ", "Mundo"]
```

#### Usando Resultados

```hmp
# Resultado fica em last_result
CALL math.sum WITH a=10, b=5
SET resultado TO ${last_result}

# Com label
CALL math.sum WITH a=10, b=5, label="soma"
CALL math.multiply WITH a=3, b=4, label="mult"
SET s TO ${last_result["soma"]}
SET m TO ${last_result["mult"]}
```

---

## Condicionais

### IF/THEN/ELSE/ENDIF

```hmp
IF <condicao> THEN
    <comandos>
ENDIF

IF <condicao> THEN
    <comandos_verdadeiro>
ELSE
    <comandos_falso>
ENDIF
```

#### Exemplos

```hmp
# Simples
SET idade TO 18
IF ${idade} >= 18 THEN
    CALL log.print WITH message="Maior de idade"
ENDIF

# Com ELSE
SET nota TO 7
IF ${nota} >= 6 THEN
    CALL log.print WITH message="Aprovado"
ELSE
    CALL log.print WITH message="Reprovado"
ENDIF

# Multiplas condicoes
SET idade TO 25
SET cnh TO true
IF ${idade} >= 18 AND ${cnh} == true THEN
    CALL log.print WITH message="Pode dirigir"
ENDIF

# Condicoes aninhadas
SET tipo TO "premium"
IF ${tipo} == "premium" THEN
    IF ${saldo} > 500 THEN
        CALL log.print WITH message="Cliente VIP"
    ENDIF
ENDIF
```

---

## Loops

### LOOP N TIMES

```hmp
LOOP <numero> TIMES
    <comandos>
ENDLOOP
```

Variavel especial: `${loop_index}` (comeca em 0)

```hmp
LOOP 5 TIMES
    CALL log.print WITH message="Iteracao ${loop_index}"
ENDLOOP
# Saida: 0, 1, 2, 3, 4
```

### WHILE

```hmp
WHILE <condicao>
    <comandos>
ENDWHILE
```

```hmp
SET contador TO 0
WHILE ${contador} < 5
    CALL log.print WITH message="Contador: ${contador}"
    SET contador TO ${contador + 1}
ENDWHILE
```

### FOR EACH

```hmp
FOR EACH <variavel> IN ${lista}
    <comandos>
ENDFOR
```

```hmp
SET frutas TO ["maca", "banana", "laranja"]
FOR EACH fruta IN ${frutas}
    CALL log.print WITH message="Fruta: ${fruta}"
ENDFOR

# Com indice
SET nomes TO ["Ana", "Bruno", "Carlos"]
FOR EACH nome IN ${nomes}
    SET pos TO ${loop_index + 1}
    CALL log.print WITH message="${pos}. ${nome}"
ENDFOR
```

---

## Funcoes

### FUNCTION/ENDFUNCTION

```hmp
FUNCTION <nome>(<param1>, <param2>, ...)
    <comandos>
    RETURN <valor>
ENDFUNCTION
```

#### Exemplos

```hmp
# Funcao simples
FUNCTION saudacao(nome)
    SET msg TO "Ola, ${nome}!"
    RETURN ${msg}
ENDFUNCTION

CALL saudacao WITH nome="Maria"
SET resultado TO ${last_result}

# Funcao com calculos
FUNCTION calcular_media(a, b, c)
    SET soma TO ${a + b + c}
    SET media TO ${soma / 3}
    RETURN ${media}
ENDFUNCTION

CALL calcular_media WITH a=10, b=20, c=30

# Funcao com condicional
FUNCTION classificar(nota)
    IF ${nota} >= 9 THEN
        RETURN "Excelente"
    ENDIF
    IF ${nota} >= 7 THEN
        RETURN "Bom"
    ENDIF
    RETURN "Regular"
ENDFUNCTION
```

---

## Tratamento de Erros

### TRY/CATCH/ENDTRY

```hmp
TRY
    <comandos_que_podem_falhar>
CATCH
    <comandos_se_houver_erro>
ENDTRY
```

Variavel especial: `${error}` (mensagem do erro)

```hmp
TRY
    CALL http.get WITH url="https://api.invalida.com"
    CALL log.print WITH message="Sucesso!"
CATCH
    CALL log.print WITH message="Erro: ${error}"
ENDTRY

# Fallback
TRY
    CALL http.get WITH url="https://api1.com"
    SET dados TO ${last_result}
CATCH
    SET dados TO {"fallback": true}
ENDTRY
```

---

## Execucao Paralela

### PARALLEL/ENDPARALLEL

```hmp
PARALLEL
    <comando1>
    <comando2>
    <comando3>
ENDPARALLEL
```

Ideal para requisicoes HTTP independentes.

```hmp
PARALLEL
    CALL http.get WITH url="https://api.com/user1", label="u1"
    CALL http.get WITH url="https://api.com/user2", label="u2"
    CALL http.get WITH url="https://api.com/user3", label="u3"
ENDPARALLEL

SET dados1 TO ${last_result["u1"]}
SET dados2 TO ${last_result["u2"]}
SET dados3 TO ${last_result["u3"]}
```

---

## Variaveis Especiais

| Variavel | Descricao | Contexto |
|----------|-----------|----------|
| `last_result` | Resultado do ultimo CALL | Global |
| `loop_index` | Indice atual do loop (0-based) | LOOP, FOR EACH |
| `error` | Mensagem de erro capturado | CATCH |

### Exemplos

```hmp
# last_result
CALL math.sum WITH a=5, b=3
SET soma TO ${last_result}  # 8

# loop_index
LOOP 3 TIMES
    CALL log.print WITH message="Index: ${loop_index}"
ENDLOOP
# Index: 0, Index: 1, Index: 2

# error
TRY
    CALL math.divide WITH a=10, b=0
CATCH
    CALL log.print WITH message="Capturado: ${error}"
ENDTRY
```

---

## Comentarios

Linhas que comecam com `#` sao ignoradas.

```hmp
# Este e um comentario
SET nome TO "Maria"  # Comentarios inline nao sao suportados
```

---

## Limites de Seguranca

| Limite | Valor |
|--------|-------|
| Iteracoes de loop | 1000 |
| Profundidade de chamada | 100 |
| Timeout HTTP | 30 segundos |
| Sleep maximo | 5 segundos |

---

Voltar para [README](../README.md) | Ver [Tools](tools-reference.md) | Ver [Arquitetura](architecture.md)
