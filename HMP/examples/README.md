# Exemplos HMP

Esta pasta contem exemplos de scripts HMP para demonstrar os recursos da linguagem.

## Exemplos Disponiveis

### Basico

| Arquivo | Descricao |
|---------|-----------|
| `hello_world.hmp` | Primeiro script - variaveis, interpolacao, CALL |
| `calculadora.hmp` | Funcoes e operacoes matematicas |
| `fibonacci.hmp` | Sequencia de Fibonacci com WHILE |

### Intermediario

| Arquivo | Descricao |
|---------|-----------|
| `lista_compras.hmp` | Manipulacao de listas e FOR EACH |
| `strings.hmp` | Tools de manipulacao de strings |
| `tratamento_erros.hmp` | Blocos TRY/CATCH e validacao |

## Como Executar

### Via CLI

```bash
cd HMP
hmp run examples/hello_world.hmp
```

### Via Python

```python
from hmp import run_script

with open('examples/hello_world.hmp') as f:
    script = f.read()

result = run_script(script)
print(result['output'])
```

### Via Demo

```bash
cd HMP
python run_demo.py
```

## Estrutura dos Exemplos

Cada exemplo segue a estrutura:

```hmp
# =============================================================================
# Nome do Exemplo - Breve descricao
# =============================================================================
# Este exemplo demonstra:
# - Recurso 1
# - Recurso 2
# - Recurso 3

# Codigo do exemplo...

RETURN resultado
```

## Criando Novos Exemplos

1. Crie um arquivo `.hmp` nesta pasta
2. Adicione comentarios explicativos
3. Use `RETURN` para indicar o resultado
4. Teste com `hmp run seu_exemplo.hmp`
