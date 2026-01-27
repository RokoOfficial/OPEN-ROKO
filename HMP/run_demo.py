#!/usr/bin/env python3
"""Script de demonstracao do HMP Framework."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from hmp import run_script, list_tools, __version__


def main():
    print(f"=== HMP Framework v{__version__} ===\n")
    
    print("1. Executando Hello World:")
    print("-" * 40)
    result = run_script('''
SET nome TO "Mundo"
CALL log.print WITH message="Ola, ${nome}!"
RETURN "Sucesso!"
''')
    print(f"Retorno: {result['return_value']}")
    print()
    
    print("2. Operacoes Matematicas:")
    print("-" * 40)
    result = run_script('''
SET a TO 10
SET b TO 5
CALL math.sum WITH a=${a}, b=${b}
CALL log.print WITH message="Soma: ${a} + ${b} = ${last_result['default']}"
CALL math.multiply WITH a=${a}, b=${b}
CALL log.print WITH message="Multiplicacao: ${a} * ${b} = ${last_result['default']}"
''')
    print()
    
    print("3. Loop e Condicional:")
    print("-" * 40)
    result = run_script('''
SET numeros TO [1, 2, 3, 4, 5]
SET soma TO 0
FOR EACH n IN ${numeros}
    SET soma TO ${soma + n}
    CALL log.print WITH message="Somando ${n}, total: ${soma}"
ENDFOR
CALL log.print WITH message="Soma total: ${soma}"
''')
    print()
    
    print("4. Funcao Customizada:")
    print("-" * 40)
    result = run_script('''
FUNCTION dobrar(x)
    SET resultado TO ${x * 2}
    RETURN ${resultado}
ENDFUNCTION

CALL dobrar WITH x=21
SET dobro TO ${last_result["default"]}
CALL log.print WITH message="21 * 2 = ${dobro}"
''')
    print()
    
    print("5. Tools Disponiveis:")
    print("-" * 40)
    tools = list_tools()
    print(f"Total: {len(tools)} tools")
    
    categories = {}
    for tool in tools:
        cat = tool.split('.')[0]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    print("Categorias:", dict(sorted(categories.items())))
    print()
    
    print("=== Demonstracao Concluida! ===")


if __name__ == '__main__':
    main()
