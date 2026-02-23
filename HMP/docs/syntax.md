# Sintaxe da Linguagem HMP

A linguagem HMP (High-level Modular Protocol) é uma linguagem de script declarativa projetada para automação e orquestração de fluxos de trabalho. Sua sintaxe é simples e intuitiva, permitindo que os usuários definam tarefas de forma clara e concisa.

## Comandos Principais

### `SET`

Usado para definir ou atualizar o valor de uma variável.

```hmp
SET variavel TO "valor"
SET numero TO 123
SET booleano TO TRUE
SET lista TO [1, 2, 3]
SET resultado TO ${10 * 5}
```

### `CALL`

Usado para invocar uma ferramenta (tool) ou uma função definida no script. Pode receber parâmetros e atribuir o resultado a uma variável.

```hmp
CALL log.info WITH message="Olá, mundo!"
CALL math.sum WITH a=10, b=20 AS soma_total
CALL minha_funcao WITH param1="valor1", param2="valor2"
```

### `IMPORT`

Usado para importar módulos HMP externos, permitindo a reutilização de código e a organização de scripts maiores.

```hmp
IMPORT "meu_modulo"
IMPORT "utilidades" AS utils
```

### `IF / THEN / ELSE / ENDIF`

Estrutura condicional para executar blocos de código com base em uma condição.

```hmp
IF ${idade} >= 18 THEN
    CALL log.info WITH message="Maior de idade."
ELSE
    CALL log.info WITH message="Menor de idade."
ENDIF

IF ${status} == "ativo" THEN
    CALL processar.ativo
ENDIF
```

### `LOOP / TIMES / ENDLOOP`

Executa um bloco de código um número especificado de vezes.

```hmp
LOOP 5 TIMES
    CALL log.info WITH message="Iteração de loop."
ENDLOOP

SET count TO 3
LOOP ${count} TIMES
    CALL log.info WITH message="Loop dinâmico."
ENDLOOP
```

### `WHILE / ENDWHILE`

Executa um bloco de código repetidamente enquanto uma condição for verdadeira.

```hmp
SET i TO 0
WHILE ${i} < 5
    SET i TO ${i + 1}
    CALL log.info WITH message="Contador: ${i}"
ENDWHILE
```

### `FOR EACH / IN / ENDFOR`

Itera sobre os elementos de uma lista ou outro iterável.

```hmp
SET frutas TO ["maçã", "banana", "laranja"]
FOR EACH fruta IN frutas
    CALL log.info WITH message="Fruta: ${fruta}"
ENDFOR
```

### `FUNCTION / ENDFUNCTION`

Define uma função reutilizável que pode aceitar parâmetros e retornar um valor.

```hmp
FUNCTION somar(a, b)
    RETURN ${a + b}
ENDFUNCTION

CALL somar WITH a=10, b=20 AS resultado
CALL log.info WITH message="Resultado da função: ${resultado}"
```

### `RETURN`

Usado dentro de uma função para especificar o valor de retorno.

```hmp
FUNCTION get_saudacao(nome)
    RETURN "Olá, ${nome}!"
ENDFUNCTION
```

### `TRY / CATCH / ENDTRY`

Permite o tratamento de erros, executando um bloco de código em caso de exceção.

```hmp
TRY
    CALL tool.nao_existente WITH param="valor"
CATCH erro
    CALL log.error WITH message="Erro capturado: ${erro}"
ENDTRY
```

### `PARALLEL / ENDPARALLEL`

Executa um bloco de código em paralelo (a implementação exata pode variar dependendo do motor de execução).

```hmp
PARALLEL
    CALL tarefa.um
    CALL tarefa.dois
ENDPARALLEL
```

## Tipos de Dados

HMP suporta os seguintes tipos de dados:

- **Strings**: Delimitadas por aspas duplas (`"`) ou simples (`'`). Suportam interpolação com `${}`.
  ```hmp
  SET mensagem TO "Olá, mundo!"
  SET nome TO 'Alice'
  SET saudacao TO "Bem-vindo, ${nome}!"
  ```
- **Números**: Inteiros e decimais.
  ```hmp
  SET idade TO 30
  SET preco TO 99.99
  ```
- **Booleanos**: `TRUE` e `FALSE`.
  ```hmp
  SET ativo TO TRUE
  ```
- **Listas**: Coleções ordenadas de valores, delimitadas por colchetes `[]`.
  ```hmp
  SET cores TO ["vermelho", "verde", "azul"]
  SET numeros TO [1, 2, 3, ${4 * 2}]
  ```
- **Nulo**: `NONE` ou `NULL`.
  ```hmp
  SET valor_nulo TO NONE
  ```

## Expressões

Expressões são avaliadas dinamicamente e podem incluir:

- **Operadores Aritméticos**: `+`, `-`, `*`, `/`, `%`.
- **Operadores de Comparação**: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- **Operadores Lógicos**: `AND`, `OR`, `NOT`.
- **Acesso a Variáveis**: `variavel` ou `${variavel}`.
- **Acesso a Propriedades/Índices**: `${lista[0]}`, `${objeto.propriedade}`.

Expressões podem ser usadas em comandos como `SET`, `IF`, `WHILE`, `LOOP`, `RETURN` e como parâmetros de `CALL`.

```hmp
SET x TO 10
SET y TO 20
SET soma TO ${x + y}
IF ${soma} > 25 AND ${x} < ${y} THEN
    CALL log.info WITH message="Condição complexa verdadeira."
ENDIF
```

## Comentários

Comentários são indicados pelo caractere `#` e são ignorados pelo interpretador.

```hmp
# Este é um comentário de linha única
SET variavel TO 1 # Este é um comentário inline
```
