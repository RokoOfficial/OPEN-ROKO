"""CLI principal do HMP."""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional

from hmp.core.engine import HMPEngine


def create_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog='hmp',
        description='HMP - Human Machine Protocol / Hybrid Macro Programming',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  hmp run script.hmp           Executa um script HMP
  hmp run script.hmp -v        Executa com saida detalhada
  hmp validate script.hmp      Valida sintaxe de um script
  hmp tools                    Lista todas as tools disponiveis
  hmp version                  Mostra versao do HMP
  hmp repl                     Inicia modo interativo
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponiveis')
    
    run_parser = subparsers.add_parser('run', help='Executa um script HMP')
    run_parser.add_argument('file', type=str, help='Arquivo HMP a executar')
    run_parser.add_argument('-v', '--verbose', action='store_true', help='Saida detalhada')
    run_parser.add_argument('-o', '--output', type=str, help='Arquivo de saida JSON')
    run_parser.add_argument('--var', action='append', nargs=2, metavar=('NOME', 'VALOR'),
                           help='Define variavel inicial')
    
    validate_parser = subparsers.add_parser('validate', help='Valida sintaxe de um script')
    validate_parser.add_argument('file', type=str, help='Arquivo HMP a validar')
    
    subparsers.add_parser('tools', help='Lista todas as tools disponiveis')
    subparsers.add_parser('version', help='Mostra versao do HMP')
    subparsers.add_parser('repl', help='Inicia modo interativo')
    
    return parser


def cmd_run(args: argparse.Namespace) -> int:
    """Executa um script HMP."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"Erro: Arquivo nao encontrado: {file_path}")
        return 1
    
    try:
        script = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return 1
    
    initial_vars = {}
    if args.var:
        for name, value in args.var:
            try:
                initial_vars[name] = json.loads(value)
            except json.JSONDecodeError:
                initial_vars[name] = value
    
    engine = HMPEngine()
    result = engine.execute(script, initial_vars)
    
    if args.verbose:
        print("\n=== Saida do Script ===")
        for line in result.get('output', []):
            print(line)
        print("\n=== Variaveis ===")
        for name, value in result.get('variables', {}).items():
            print(f"  {name} = {value}")
    
    if result.get('return_value') is not None:
        print(f"\nRetorno: {result['return_value']}")
    
    if not result.get('success', True):
        print(f"\nErro: {result.get('error')}")
        return 1
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\nResultado salvo em: {output_path}")
    
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Valida sintaxe de um script."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"Erro: Arquivo nao encontrado: {file_path}")
        return 1
    
    try:
        script = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return 1
    
    from hmp.parser.tokenizer import Tokenizer
    
    try:
        tokenizer = Tokenizer(script)
        tokens = tokenizer.tokenize()
        print(f"Validacao OK: {len(tokens)} tokens encontrados")
        return 0
    except Exception as e:
        print(f"Erro de sintaxe: {e}")
        return 1


def cmd_tools(args: argparse.Namespace) -> int:
    """Lista todas as tools disponiveis."""
    engine = HMPEngine()
    tools = engine.registry.list_by_category()
    
    print("\n=== Tools Disponiveis ===\n")
    
    for category in sorted(tools.keys()):
        print(f"[{category}]")
        for tool in sorted(tools[category]):
            tool_obj = engine.registry.get(tool)
            if tool_obj and tool_obj.description:
                print(f"  {tool}: {tool_obj.description}")
            else:
                print(f"  {tool}")
        print()
    
    total = sum(len(t) for t in tools.values())
    print(f"Total: {total} tools em {len(tools)} categorias")
    
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    """Mostra versao do HMP."""
    from hmp import __version__
    print(f"HMP - Human Machine Protocol v{__version__}")
    print("Motor de execucao para automacao e orquestracao de fluxos logicos")
    return 0


def cmd_repl(args: argparse.Namespace) -> int:
    """Inicia modo interativo."""
    from hmp import __version__
    
    print(f"HMP REPL v{__version__}")
    print("Digite comandos HMP ou 'exit' para sair\n")
    
    engine = HMPEngine()
    context_vars = {}
    
    while True:
        try:
            line = input("hmp> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAte logo!")
            break
        
        if not line:
            continue
        
        if line.lower() in ('exit', 'quit', 'q'):
            print("Ate logo!")
            break
        
        if line.lower() == 'vars':
            print("Variaveis:", context_vars)
            continue
        
        if line.lower() == 'clear':
            context_vars = {}
            print("Variaveis limpas")
            continue
        
        result = engine.execute(line, context_vars)
        
        for output in result.get('output', []):
            print(output)
        
        context_vars.update(result.get('variables', {}))
        
        if result.get('return_value') is not None:
            print(f"=> {result['return_value']}")
        
        if not result.get('success'):
            print(f"Erro: {result.get('error')}")
    
    return 0


def app() -> int:
    """Ponto de entrada principal da CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    commands = {
        'run': cmd_run,
        'validate': cmd_validate,
        'tools': cmd_tools,
        'version': cmd_version,
        'repl': cmd_repl,
    }
    
    if args.command in commands:
        return commands[args.command](args)
    
    parser.print_help()
    return 0


def main():
    """Funcao main para entry point."""
    sys.exit(app())


if __name__ == '__main__':
    main()
