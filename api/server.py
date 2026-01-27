"""
HMP API Server
REST API que expoe o protocolo HMP via HTTP.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'HMP', 'src'))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from hmp import run_script, list_tools
from hmp.tools.registry import ToolRegistry
from hmp.tools.math_tools import MathToolProvider
from hmp.tools.string_tools import StringToolProvider
from hmp.tools.list_tools import ListToolProvider
from hmp.tools.json_tools import JsonToolProvider
from hmp.tools.date_tools import DateToolProvider
from hmp.tools.http_tools import HttpToolProvider
from hmp.tools.crypto_tools import CryptoToolProvider
from hmp.tools.random_tools import RandomToolProvider
from hmp.tools.log_tools import LogToolProvider
from hmp.tools.system_tools import SystemToolProvider
from hmp.tools.meta_tools import MetaToolProvider
from hmp.core.context import ExecutionContext

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)




@app.route('/openrokos')
def openrokos_page():
    """Página sobre o OPENROKOS."""
    return render_template('openrokos.html')


@app.route('/engine')
def engine_page():
    """Pagina HMP Engine."""
    return render_template('engine.html')


@app.route('/engine/syntax')
def syntax_page():
    """Pagina Sintaxe."""
    return render_template('syntax.html')


@app.route('/engine/tools')
def tools_page():
    """Pagina Tools."""
    return render_template('tools.html')


@app.route('/api')
def api_docs_page():
    """Pagina API."""
    return render_template('api_docs.html')

registry = ToolRegistry()
registry.register_provider(MathToolProvider())
registry.register_provider(StringToolProvider())
registry.register_provider(ListToolProvider())
registry.register_provider(JsonToolProvider())
registry.register_provider(DateToolProvider())
registry.register_provider(HttpToolProvider())
registry.register_provider(CryptoToolProvider())
registry.register_provider(RandomToolProvider())
registry.register_provider(LogToolProvider())
registry.register_provider(SystemToolProvider())
registry.register_provider(MetaToolProvider())


def invoke_tool(tool_name, params):
    """Helper para invocar uma tool."""
    tool = registry.get(tool_name)
    if not tool:
        return None
    ctx = ExecutionContext()
    return tool.invoke(params, ctx)


@app.route('/')
def index():
    """Pagina inicial OPENROKOS."""
    return render_template('index.html')


@app.route('/api/info')
def api_info():
    """Informacoes da API."""
    return jsonify({
        'name': 'HMP API',
        'version': '2.0.0',
        'description': 'REST API para o Human Machine Protocol',
        'endpoints': {
            'GET /api/info': 'Informacoes da API (health check)',
            'GET /tools': 'Lista todas as 64 tools disponiveis',
            'GET /tools/<category>': 'Lista tools de uma categoria',
            'POST /run': 'Executa um script HMP inline',
            'GET /files': 'Lista arquivos .hmp disponiveis',
            'GET /files/<filename>': 'Retorna conteudo de um arquivo .hmp',
            'PUT /files/<filename>': 'Cria ou atualiza um arquivo .hmp',
            'DELETE /files/<filename>': 'Remove um arquivo .hmp do usuario',
            'POST /files/upload': 'Faz upload de um novo arquivo .hmp',
            'POST /run/file/<filename>': 'Executa um arquivo .hmp',
            'POST /tool/<name>': 'Executa uma tool diretamente',
            'GET /math/sum?a=X&b=Y': 'Soma dois numeros',
            'GET /date/now': 'Data/hora atual',
            'GET /random/number?min=X&max=Y': 'Numero aleatorio'
        },
        'total_tools': len(list_tools()),
        'status': 'online'
    })


@app.route('/tools', methods=['GET'])
def get_tools():
    """Lista todas as tools disponiveis."""
    tools = list_tools()
    
    categories = {}
    for tool in tools:
        category = tool.split('.')[0]
        if category not in categories:
            categories[category] = []
        categories[category].append(tool)
    
    return jsonify({
        'total': len(tools),
        'categories': categories
    })


@app.route('/tools/<category>', methods=['GET'])
def get_tools_by_category(category):
    """Lista tools de uma categoria especifica."""
    tools = list_tools()
    
    filtered = [t for t in tools if t.startswith(f"{category}.")]
    
    if not filtered:
        return jsonify({
            'error': f"Categoria '{category}' nao encontrada",
            'available_categories': list(set(t.split('.')[0] for t in tools))
        }), 404
    
    return jsonify({
        'category': category,
        'count': len(filtered),
        'tools': filtered
    })


@app.route('/run', methods=['POST'])
def run_hmp_script():
    """
    Executa um script HMP.
    
    Body JSON:
    {
        "script": "SET x TO 10\\nCALL log.print WITH message=\\"Ola!\\""
    }
    """
    data = request.get_json()
    
    if not data or 'script' not in data:
        return jsonify({
            'error': 'Campo "script" obrigatorio no body'
        }), 400
    
    script = data['script']
    
    try:
        result = run_script(script)
        return jsonify({
            'success': True,
            'output': result.get('output', []),
            'variables': result.get('variables', {}),
            'return_value': result.get('return_value')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'HMP', 'examples')
USER_FILES_DIR = os.path.join(os.path.dirname(__file__), '..', 'hmp_files')

os.makedirs(USER_FILES_DIR, exist_ok=True)


def get_all_hmp_files():
    """Retorna todos os arquivos HMP (exemplos + usuario)."""
    files = []
    
    if os.path.exists(EXAMPLES_DIR):
        for f in os.listdir(EXAMPLES_DIR):
            if f.endswith('.hmp'):
                filepath = os.path.join(EXAMPLES_DIR, f)
                files.append({
                    'name': f,
                    'size': os.path.getsize(filepath),
                    'source': 'examples',
                    'path': filepath
                })
    
    if os.path.exists(USER_FILES_DIR):
        for f in os.listdir(USER_FILES_DIR):
            if f.endswith('.hmp'):
                filepath = os.path.join(USER_FILES_DIR, f)
                files.append({
                    'name': f,
                    'size': os.path.getsize(filepath),
                    'source': 'user',
                    'path': filepath
                })
    
    return files


def find_hmp_file(filename):
    """Procura um arquivo HMP em todas as pastas."""
    if not filename.endswith('.hmp'):
        filename += '.hmp'
    
    user_path = os.path.join(USER_FILES_DIR, filename)
    if os.path.exists(user_path):
        return user_path
    
    examples_path = os.path.join(EXAMPLES_DIR, filename)
    if os.path.exists(examples_path):
        return examples_path
    
    return None


@app.route('/files', methods=['GET'])
def list_hmp_files():
    """Lista todos os arquivos .hmp disponiveis."""
    try:
        files = get_all_hmp_files()
        return jsonify({
            'count': len(files),
            'files': sorted([{'name': f['name'], 'size': f['size'], 'source': f['source']} 
                           for f in files], key=lambda x: x['name'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/<filename>', methods=['GET', 'PUT', 'DELETE'])
def manage_hmp_file(filename):
    """
    GET: Retorna o conteudo de um arquivo .hmp
    PUT: Cria ou atualiza um arquivo .hmp
    DELETE: Remove um arquivo .hmp (apenas arquivos do usuario)
    """
    if not filename.endswith('.hmp'):
        filename += '.hmp'
    
    if request.method == 'GET':
        filepath = find_hmp_file(filename)
        
        if not filepath:
            return jsonify({
                'error': f"Arquivo '{filename}' nao encontrado",
                'available': [f['name'] for f in get_all_hmp_files()]
            }), 404
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'filename': filename,
                'content': content,
                'source': 'user' if USER_FILES_DIR in filepath else 'examples'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Campo "content" obrigatorio'}), 400
        
        filepath = os.path.join(USER_FILES_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data['content'])
            return jsonify({
                'success': True,
                'message': f"Arquivo '{filename}' salvo com sucesso",
                'filename': filename,
                'size': os.path.getsize(filepath)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        filepath = os.path.join(USER_FILES_DIR, filename)
        
        if not os.path.exists(filepath):
            examples_path = os.path.join(EXAMPLES_DIR, filename)
            if os.path.exists(examples_path):
                return jsonify({'error': 'Nao e possivel deletar arquivos de exemplo'}), 403
            return jsonify({'error': f"Arquivo '{filename}' nao encontrado"}), 404
        
        try:
            os.remove(filepath)
            return jsonify({
                'success': True,
                'message': f"Arquivo '{filename}' removido com sucesso"
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/files/upload', methods=['POST'])
def upload_hmp_file():
    """
    Faz upload de um arquivo HMP.
    
    Body JSON:
    {
        "filename": "meu_script.hmp",
        "content": "SET x TO 10\\nCALL log.print WITH message=\\"Ola!\\""
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Body JSON obrigatorio'}), 400
    
    if 'filename' not in data or 'content' not in data:
        return jsonify({'error': 'Campos "filename" e "content" obrigatorios'}), 400
    
    filename = data['filename']
    if not filename.endswith('.hmp'):
        filename += '.hmp'
    
    filename = os.path.basename(filename)
    
    filepath = os.path.join(USER_FILES_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data['content'])
        return jsonify({
            'success': True,
            'message': f"Arquivo '{filename}' criado com sucesso",
            'filename': filename,
            'size': os.path.getsize(filepath)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/run/file/<filename>', methods=['POST'])
def run_hmp_file(filename):
    """
    Executa um arquivo .hmp.
    
    URL: /run/file/hello_world.hmp
    Body JSON (opcional):
    {
        "variables": {"nome": "Mundo"}
    }
    """
    if not filename.endswith('.hmp'):
        filename += '.hmp'
    
    filepath = find_hmp_file(filename)
    
    if not filepath:
        return jsonify({
            'error': f"Arquivo '{filename}' nao encontrado",
            'available': [f['name'] for f in get_all_hmp_files()]
        }), 404
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            script = f.read()
        
        data = request.get_json() or {}
        initial_vars = data.get('variables', {})
        
        if initial_vars:
            prefix = '\n'.join([f'SET {k} TO "{v}"' if isinstance(v, str) else f'SET {k} TO {v}' 
                               for k, v in initial_vars.items()])
            script = prefix + '\n' + script
        
        result = run_script(script)
        return jsonify({
            'success': True,
            'filename': filename,
            'output': result.get('output', []),
            'variables': result.get('variables', {}),
            'return_value': result.get('return_value')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/tool/<path:tool_name>', methods=['POST'])
def execute_tool(tool_name):
    """
    Executa uma tool diretamente.
    
    URL: /tool/math.sum
    Body JSON:
    {
        "a": 10,
        "b": 5
    }
    """
    params = request.get_json() or {}
    
    result = invoke_tool(tool_name, params)
    if result is None:
        return jsonify({
            'error': f"Tool '{tool_name}' nao encontrada",
            'available': list_tools()
        }), 404
    
    return jsonify({
        'success': True,
        'tool': tool_name,
        'result': result
    })


@app.route('/math/sum', methods=['POST', 'GET'])
def math_sum():
    """Soma dois numeros."""
    if request.method == 'GET':
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    else:
        data = request.get_json() or {}
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
    
    result = invoke_tool('math.sum', {'a': a, 'b': b})
    return jsonify({'result': result})


@app.route('/math/multiply', methods=['POST', 'GET'])
def math_multiply():
    """Multiplica dois numeros."""
    if request.method == 'GET':
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    else:
        data = request.get_json() or {}
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
    
    result = invoke_tool('math.multiply', {'a': a, 'b': b})
    return jsonify({'result': result})


@app.route('/string/upper', methods=['POST', 'GET'])
def string_upper():
    """Converte texto para maiusculas."""
    if request.method == 'GET':
        text = request.args.get('text', '')
    else:
        data = request.get_json() or {}
        text = data.get('text', '')
    
    result = invoke_tool('string.upper', {'text': text})
    return jsonify({'result': result})


@app.route('/string/lower', methods=['POST', 'GET'])
def string_lower():
    """Converte texto para minusculas."""
    if request.method == 'GET':
        text = request.args.get('text', '')
    else:
        data = request.get_json() or {}
        text = data.get('text', '')
    
    result = invoke_tool('string.lower', {'text': text})
    return jsonify({'result': result})


@app.route('/list/length', methods=['POST'])
def list_length():
    """Retorna o tamanho de uma lista."""
    data = request.get_json() or {}
    lst = data.get('list', [])
    
    result = invoke_tool('list.length', {'list': lst})
    return jsonify({'result': result})


@app.route('/json/parse', methods=['POST'])
def json_parse():
    """Faz parse de uma string JSON."""
    data = request.get_json() or {}
    text = data.get('text', '{}')
    
    result = invoke_tool('json.parse', {'text': text})
    return jsonify({'result': result})


@app.route('/date/now', methods=['GET'])
def date_now():
    """Retorna a data/hora atual."""
    result = invoke_tool('date.now', {})
    return jsonify({'result': result})


@app.route('/random/number', methods=['GET', 'POST'])
def random_number():
    """Gera um numero aleatorio."""
    if request.method == 'GET':
        min_val = float(request.args.get('min', 0))
        max_val = float(request.args.get('max', 100))
    else:
        data = request.get_json() or {}
        min_val = float(data.get('min', 0))
        max_val = float(data.get('max', 100))
    
    result = invoke_tool('random.number', {'min': min_val, 'max': max_val})
    return jsonify({'result': result})


@app.route('/crypto/hash', methods=['POST'])
def crypto_hash():
    """Gera hash de um texto."""
    data = request.get_json() or {}
    text = data.get('text', '')
    algorithm = data.get('algorithm', 'sha256')
    
    result = invoke_tool('crypto.hash', {'text': text, 'algorithm': algorithm})
    return jsonify({'result': result})


if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
