"""Motor de execucao do HMP."""

import json
import re
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

from hmp.core.context import ExecutionContext, HMPConfig
from hmp.tools.registry import ToolRegistry
from hmp.expr.evaluator import safe_eval_expr
from hmp.expr.cache import ExpressionCache
from hmp.runtime.errors import HMPRuntimeError, HMPLimitError

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


class HMPEngine:
    """
    Motor de execucao do HMP.
    
    Processa scripts HMP e executa comandos de forma segura e deterministica.
    """
    
    VERSION = "3.0.0"
    
    def __init__(
        self,
        config: Optional[HMPConfig] = None,
        registry: Optional[ToolRegistry] = None,
        cache: Optional[ExpressionCache] = None,
        script_path: Optional[str] = None
    ):
        self.config = config or HMPConfig()
        self.registry = registry or ToolRegistry()
        self.cache = cache or ExpressionCache(maxsize=2000)
        self.script_path = script_path or os.getcwd()
        self._imported_modules = set()
        
        self._register_default_tools()
    
    def _register_default_tools(self) -> None:
        """Registra todas as tools nativas."""
        providers = [
            MathToolProvider(),
            StringToolProvider(),
            ListToolProvider(),
            JsonToolProvider(),
            DateToolProvider(),
            HttpToolProvider(),
            CryptoToolProvider(),
            RandomToolProvider(),
            LogToolProvider(),
            SystemToolProvider(),
            MetaToolProvider(),
        ]
        
        for provider in providers:
            self.registry.register_provider(provider)
    
    def execute(
        self, 
        script: str, 
        initial_vars: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executa um script HMP.
        
        Args:
            script: Codigo HMP a ser executado
            initial_vars: Variaveis iniciais opcionais
            
        Returns:
            Dicionario com resultado da execucao
        """
        context = ExecutionContext(
            registry=self.registry,
            cache=self.cache,
            config=self.config,
            initial_vars=initial_vars
        )
        
        result = {
            "success": True,
            "output": [],
            "variables": {},
            "return_value": None,
            "error": None
        }
        
        try:
            lines = script.strip().split('\n')
            self._register_functions(lines, context, result)
            self._execute_lines(lines, context, result)
            result["variables"] = {
                k: v for k, v in context.variables.items() 
                if not k.startswith('_')
            }
        except HMPLimitError as e:
            result["success"] = False
            result["error"] = str(e)
        except HMPRuntimeError as e:
            result["success"] = False
            result["error"] = str(e)
        except Exception as e:
            result["success"] = False
            result["error"] = f"Erro inesperado: {str(e)}"
        
        return result
    
    def _register_functions(
        self, 
        lines: List[str], 
        context: ExecutionContext, 
        result: Dict
    ) -> None:
        """Registra funcoes definidas no script."""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('FUNCTION '):
                match = re.match(r'FUNCTION\s+(\w+)\s*\(([^)]*)\)', line)
                if match:
                    func_name = match.group(1)
                    params_str = match.group(2).strip()
                    params = [p.strip() for p in params_str.split(',')] if params_str else []
                    
                    func_start = i + 1
                    func_end = func_start
                    depth = 1
                    
                    while func_end < len(lines) and depth > 0:
                        current = lines[func_end].strip()
                        if current.startswith('FUNCTION '):
                            depth += 1
                        elif current == 'ENDFUNCTION':
                            depth -= 1
                        func_end += 1
                    
                    context.functions[func_name] = {
                        'params': params,
                        'lines': lines[func_start:func_end-1]
                    }
                    result["output"].append(
                        f"[FUNCTION] {func_name}({', '.join(params)}) definida"
                    )
            i += 1
    
    def _execute_lines(
        self, 
        lines: List[str], 
        context: ExecutionContext, 
        result: Dict
    ) -> None:
        """Executa linhas do script."""
        i = 0
        while i < len(lines):
            context.increment_iteration()
            context.check_limits()
            
            line = lines[i].strip()
            
            if not line or line.startswith('#'):
                i += 1
                continue
            
            if line.startswith('FUNCTION '):
                i += self._skip_block(lines, i, 'FUNCTION ', 'ENDFUNCTION') + 1
                continue
            
            if line.startswith('IF ') and 'THEN' in line:
                skip = self._handle_if(lines, i, context, result)
                i += skip + 1
                continue
            
            if line.startswith('LOOP ') and 'TIMES' in line:
                skip = self._handle_loop(lines, i, context, result)
                i += skip + 1
                continue
            
            if line.startswith('WHILE '):
                skip = self._handle_while(lines, i, context, result)
                i += skip + 1
                continue
            
            if line.startswith('FOR EACH '):
                skip = self._handle_for_each(lines, i, context, result)
                i += skip + 1
                continue
            
            if line == 'TRY':
                skip = self._handle_try(lines, i, context, result)
                i += skip + 1
                continue
            
            if line == 'PARALLEL':
                skip = self._handle_parallel(lines, i, context, result)
                i += skip + 1
                continue
            
            if line.startswith('IMPORT '):
                self._handle_import(line, context, result)
                i += 1
                continue
            
            self._process_line(line, context, result)
            i += 1
    
    def _skip_block(
        self, 
        lines: List[str], 
        start: int, 
        start_keyword: str, 
        end_keyword: str
    ) -> int:
        """Pula um bloco de codigo."""
        i = start + 1
        depth = 1
        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if line.startswith(start_keyword):
                depth += 1
            elif line == end_keyword:
                depth -= 1
            i += 1
        return i - start - 1
    
    def _process_line(
        self, 
        line: str, 
        context: ExecutionContext, 
        result: Dict
    ) -> None:
        """Processa uma linha individual."""
        context.increment_iteration()
        context.check_limits()
        
        line = line.strip()
        if not line or line.startswith('#'):
            return
        
        if line.startswith('SET '):
            self._handle_set(line, context, result)
        elif line.startswith('CALL '):
            self._handle_call(line, context, result)
        elif line.startswith('RETURN '):
            self._handle_return(line, context, result)
    
    def _handle_set(
        self, 
        line: str, 
        context: ExecutionContext, 
        result: Dict
    ) -> None:
        """Processa comando SET."""
        match = re.match(r'SET\s+(\w+)\s+TO\s+(.+)', line)
        if match:
            var_name = match.group(1)
            value_str = match.group(2)
            value = self._parse_value(value_str, context)
            context.set_variable(var_name, value)
            result["output"].append(f"SET {var_name} = {value}")
    
    def _handle_call(
        self, 
        line: str, 
        context: ExecutionContext, 
        result: Dict
    ) -> None:
        """Processa comando CALL."""
        match = re.match(r'CALL\s+([\w.]+)\s+WITH\s+(.+)', line)
        if not match:
            match = re.match(r'CALL\s+([\w.]+)', line)
            if match:
                tool_name = match.group(1)
                params = {}
            else:
                return
        else:
            tool_name = match.group(1)
            params_str = match.group(2)
            params = self._parse_params(params_str, context)
        
        if tool_name in context.functions:
            tool_result = self._call_function(tool_name, params, context, result)
        else:
            tool_result = self.registry.execute(tool_name, params, context)
        
        label = params.get('label', 'default')
        context.last_result[label] = tool_result
        context.last_result['_last'] = tool_result
        
        result["output"].append(f"[CALL] {tool_name} -> {tool_result}")
    
    def _call_function(
        self, 
        func_name: str, 
        params: Dict, 
        context: ExecutionContext, 
        result: Dict
    ) -> Any:
        """Executa uma funcao definida pelo usuario."""
        if func_name not in context.functions:
            return {"error": f"Funcao {func_name} nao encontrada"}
        
        context.push_frame(func_name, context.variables.copy())
        try:
            func = context.functions[func_name]
            
            for param_name in func['params']:
                if param_name in params:
                    context.set_variable(param_name, params[param_name])
            
            func_result = None
            for line in func['lines']:
                context.check_limits()
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith('RETURN '):
                    return_expr = line[7:].strip()
                    func_result = self._parse_value(return_expr, context)
                    break
                else:
                    self._process_line(line, context, result)
            
            return func_result
        finally:
            context.pop_frame()
    
    def _handle_return(
        self, 
        line: str, 
        context: ExecutionContext, 
        result: Dict
    ) -> None:
        """Processa comando RETURN."""
        return_expr = line[7:].strip()
        result["return_value"] = self._parse_value(return_expr, context)
        result["output"].append(f"RETURN: {result['return_value']}")
    
    def _handle_import(
        self,
        line: str,
        context: ExecutionContext,
        result: Dict
    ) -> None:
        """Processa comando IMPORT."""
        # IMPORT "arquivo.hmp"
        # IMPORT "arquivo.hmp" AS modulo
        match = re.match(r'IMPORT\s+"([^"]+)"\s*(?:AS\s+(\w+))?', line)
        if not match:
            match = re.match(r"IMPORT\s+'([^']+)'\s*(?:AS\s+(\w+))?", line)
        
        if not match:
            result["output"].append("[IMPORT] Sintaxe invalida")
            return
        
        filepath = match.group(1)
        namespace = match.group(2)
        
        try:
            script_content = self._load_module(filepath)
            if script_content is None:
                result["output"].append(f"[IMPORT] Erro: arquivo '{filepath}' nao encontrado")
                return
            
            imported_engine = HMPEngine(
                config=self.config,
                registry=self.registry,
                cache=self.cache,
                script_path=os.path.dirname(filepath)
            )
            
            imported_lines = script_content.strip().split('\n')
            temp_context = ExecutionContext(
                registry=self.registry,
                cache=self.cache,
                config=self.config
            )
            temp_result = {"output": []}
            imported_engine._register_functions(imported_lines, temp_context, temp_result)
            
            if namespace:
                for func_name, func_def in temp_context.functions.items():
                    full_name = f"{namespace}.{func_name}"
                    context.functions[full_name] = func_def
                result["output"].append(f"[IMPORT] Modulo '{filepath}' importado como '{namespace}'")
            else:
                context.functions.update(temp_context.functions)
                result["output"].append(f"[IMPORT] Modulo '{filepath}' importado")
        
        except Exception as e:
            result["output"].append(f"[IMPORT] Erro ao carregar '{filepath}': {str(e)}")
    
    def _load_module(self, filepath: str) -> Optional[str]:
        """Carrega conteudo de um arquivo HMP."""
        try:
            # Tentar caminhos possíveis
            possible_paths = [
                filepath,
                os.path.join(self.script_path, filepath),
                os.path.join(os.getcwd(), filepath),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'examples', os.path.basename(filepath))
            ]
            
            abs_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    abs_path = os.path.abspath(path)
                    break
            
            if abs_path is None or abs_path in self._imported_modules:
                return None
            
            self._imported_modules.add(abs_path)
            
            with open(abs_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        except Exception:
            return None
    
    def _handle_if(
        self, 
        lines: List[str], 
        start: int, 
        context: ExecutionContext, 
        result: Dict
    ) -> int:
        """Processa bloco IF."""
        line = lines[start].strip()
        match = re.match(r'IF\s+(.+)\s+THEN', line)
        if not match:
            return 0
        
        condition_expr = match.group(1)
        condition = self._evaluate_expression(condition_expr, context)
        
        endif_idx = start + 1
        else_idx = -1
        depth = 1
        
        while endif_idx < len(lines) and depth > 0:
            current = lines[endif_idx].strip()
            if current.startswith('IF ') and 'THEN' in current:
                depth += 1
            elif current == 'ENDIF':
                depth -= 1
            elif current == 'ELSE' and depth == 1:
                else_idx = endif_idx
            endif_idx += 1
        
        context.push_frame('if')
        try:
            if condition:
                end = else_idx if else_idx > 0 else endif_idx - 1
                for i in range(start + 1, end):
                    context.check_limits()
                    self._process_line(lines[i], context, result)
            else:
                if else_idx > 0:
                    for i in range(else_idx + 1, endif_idx - 1):
                        context.check_limits()
                        self._process_line(lines[i], context, result)
        finally:
            context.pop_frame()
        
        return endif_idx - start - 1
    
    def _handle_loop(
        self, 
        lines: List[str], 
        start: int, 
        context: ExecutionContext, 
        result: Dict
    ) -> int:
        """Processa bloco LOOP."""
        line = lines[start].strip()
        match = re.match(r'LOOP\s+(\d+)\s+TIMES', line)
        if not match:
            return 0
        
        count = min(int(match.group(1)), self.config.max_loop_iterations)
        
        endloop_idx = start + 1
        depth = 1
        while endloop_idx < len(lines) and depth > 0:
            current = lines[endloop_idx].strip()
            if current.startswith('LOOP ') and 'TIMES' in current:
                depth += 1
            elif current == 'ENDLOOP':
                depth -= 1
            endloop_idx += 1
        
        context.push_frame('loop')
        try:
            for i in range(count):
                context.check_limits()
                context.set_variable('_loop_index', i)
                context.set_variable('loop_index', i)
                for j in range(start + 1, endloop_idx - 1):
                    context.check_limits()
                    self._process_line(lines[j], context, result)
        finally:
            context.pop_frame()
        
        return endloop_idx - start - 1
    
    def _handle_while(
        self, 
        lines: List[str], 
        start: int, 
        context: ExecutionContext, 
        result: Dict
    ) -> int:
        """Processa bloco WHILE."""
        line = lines[start].strip()
        match = re.match(r'WHILE\s+(.+)', line)
        if not match:
            return 0
        
        condition_expr = match.group(1)
        
        endwhile_idx = start + 1
        depth = 1
        while endwhile_idx < len(lines) and depth > 0:
            current = lines[endwhile_idx].strip()
            if current.startswith('WHILE '):
                depth += 1
            elif current == 'ENDWHILE':
                depth -= 1
            endwhile_idx += 1
        
        iteration = 0
        context.push_frame('while')
        try:
            while True:
                context.check_limits()
                
                condition = self._evaluate_expression(condition_expr, context)
                if not condition:
                    break
                
                iteration += 1
                if iteration > self.config.max_while_iterations:
                    result["output"].append(
                        f"[WHILE] Limite de {self.config.max_while_iterations} iteracoes atingido"
                    )
                    break
                
                context.set_variable('_loop_index', iteration - 1)
                context.set_variable('loop_index', iteration - 1)
                for j in range(start + 1, endwhile_idx - 1):
                    context.check_limits()
                    self._process_line(lines[j], context, result)
        finally:
            context.pop_frame()
        
        return endwhile_idx - start - 1
    
    def _handle_for_each(
        self, 
        lines: List[str], 
        start: int, 
        context: ExecutionContext, 
        result: Dict
    ) -> int:
        """Processa bloco FOR EACH."""
        line = lines[start].strip()
        match = re.match(r'FOR EACH\s+(\w+)\s+IN\s+(.+)', line)
        if not match:
            return 0
        
        item_var = match.group(1)
        list_expr = match.group(2).strip()
        
        items = self._parse_value(list_expr, context)
        if not isinstance(items, (list, tuple)):
            return 0
        
        endfor_idx = start + 1
        depth = 1
        while endfor_idx < len(lines) and depth > 0:
            current = lines[endfor_idx].strip()
            if current.startswith('FOR EACH '):
                depth += 1
            elif current == 'ENDFOR':
                depth -= 1
            endfor_idx += 1
        
        context.push_frame('for_each')
        try:
            for idx, item in enumerate(items):
                context.check_limits()
                context.set_variable(item_var, item)
                context.set_variable('_loop_index', idx)
                context.set_variable('loop_index', idx)
                for j in range(start + 1, endfor_idx - 1):
                    context.check_limits()
                    self._process_line(lines[j], context, result)
        finally:
            context.pop_frame()
        
        return endfor_idx - start - 1
    
    def _handle_try(
        self, 
        lines: List[str], 
        start: int, 
        context: ExecutionContext, 
        result: Dict
    ) -> int:
        """Processa bloco TRY/CATCH."""
        endtry_idx = start + 1
        catch_idx = -1
        depth = 1
        
        while endtry_idx < len(lines) and depth > 0:
            current = lines[endtry_idx].strip()
            if current == 'TRY':
                depth += 1
            elif current == 'CATCH' and depth == 1:
                catch_idx = endtry_idx
            elif current == 'ENDTRY':
                depth -= 1
            endtry_idx += 1
        
        context.push_frame('try')
        try:
            end_try_block = catch_idx if catch_idx > 0 else endtry_idx - 1
            for j in range(start + 1, end_try_block):
                context.check_limits()
                self._process_line(lines[j], context, result)
        except Exception as e:
            if catch_idx > 0:
                context.set_variable('_error', str(e))
                for j in range(catch_idx + 1, endtry_idx - 1):
                    context.check_limits()
                    self._process_line(lines[j], context, result)
        finally:
            context.pop_frame()
        
        return endtry_idx - start - 1
    
    def _handle_parallel(
        self, 
        lines: List[str], 
        start: int, 
        context: ExecutionContext, 
        result: Dict
    ) -> int:
        """Processa bloco PARALLEL."""
        endparallel_idx = start + 1
        depth = 1
        
        while endparallel_idx < len(lines) and depth > 0:
            current = lines[endparallel_idx].strip()
            if current == 'PARALLEL':
                depth += 1
            elif current == 'ENDPARALLEL':
                depth -= 1
            endparallel_idx += 1
        
        context.push_frame('parallel')
        try:
            for j in range(start + 1, endparallel_idx - 1):
                context.check_limits()
                self._process_line(lines[j], context, result)
        finally:
            context.pop_frame()
        
        return endparallel_idx - start - 1
    
    def _evaluate_expression(
        self, 
        expr: str, 
        context: ExecutionContext
    ) -> Any:
        """Avalia uma expressao que pode conter ${...}."""
        eval_vars = context.variables.copy()
        eval_vars['last_result'] = context.last_result
        eval_vars['loop_index'] = context.get_variable('_loop_index', 0)
        
        if expr.startswith('${') and expr.endswith('}') and expr.count('${') == 1:
            inner = expr[2:-1]
            try:
                return safe_eval_expr(inner, eval_vars, self.cache)
            except Exception:
                return expr
        
        if '${' in expr:
            def replace_var(match):
                var_expr = match.group(1)
                try:
                    return str(safe_eval_expr(var_expr, eval_vars, self.cache))
                except Exception:
                    return match.group(0)
            
            processed = re.sub(r'\$\{([^}]+)\}', replace_var, expr)
            
            try:
                return safe_eval_expr(processed, eval_vars, self.cache)
            except Exception:
                return processed
        
        try:
            return safe_eval_expr(expr, eval_vars, self.cache)
        except Exception:
            return expr
    
    def _interpolate_string(
        self,
        text: str,
        context: ExecutionContext
    ) -> str:
        """Interpola expressoes ${...} dentro de uma string."""
        import re
        
        def replace_expr(match):
            expr = match.group(0)
            result = self._evaluate_expression(expr, context)
            return str(result) if result != expr else expr
        
        pattern = r'\$\{[^}]+\}'
        return re.sub(pattern, replace_expr, text)
    
    def _parse_value(
        self, 
        value_str: str, 
        context: ExecutionContext
    ) -> Any:
        """Converte string de valor para tipo Python."""
        value_str = value_str.strip()
        
        if value_str.startswith('${') and value_str.endswith('}'):
            return self._evaluate_expression(value_str, context)
        
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            inner = value_str[1:-1]
            if '${' in inner:
                return self._interpolate_string(inner, context)
            return inner
        
        if value_str.lstrip('-').isdigit():
            return int(value_str)
        
        try:
            return float(value_str)
        except ValueError:
            pass
        
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False
        
        if value_str.startswith('[') and value_str.endswith(']'):
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                pass
        
        if value_str.startswith('{') and value_str.endswith('}'):
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                pass
        
        if value_str in context.variables:
            return context.get_variable(value_str)
        
        return value_str
    
    def _parse_params(
        self, 
        params_str: str, 
        context: ExecutionContext
    ) -> Dict:
        """Parse dos parametros WITH - respeita strings com virgulas."""
        params = {}
        
        parts = []
        current = ""
        in_string = False
        string_char = None
        in_brackets = 0
        in_braces = 0
        
        for char in params_str:
            if char in ('"', "'") and not in_string:
                in_string = True
                string_char = char
                current += char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
                current += char
            elif char == '[' and not in_string:
                in_brackets += 1
                current += char
            elif char == ']' and not in_string:
                in_brackets -= 1
                current += char
            elif char == '{' and not in_string:
                in_braces += 1
                current += char
            elif char == '}' and not in_string:
                in_braces -= 1
                current += char
            elif char == ',' and not in_string and in_brackets == 0 and in_braces == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            parts.append(current.strip())
        
        for part in parts:
            if '=' in part:
                key, val = part.split('=', 1)
                key = key.strip()
                val = self._parse_value(val.strip(), context)
                params[key] = val
        
        return params
