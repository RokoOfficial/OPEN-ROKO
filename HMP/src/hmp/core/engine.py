"""Engine for HMP scripts."""

import json
import re
import os
from typing import Any, Dict, List, Optional, Sequence, Union
from pathlib import Path

from hmp.core.context import ExecutionContext, HMPConfig
from hmp.tools.registry import ToolRegistry
from hmp.expr.evaluator import safe_eval_expr
from hmp.expr.cache import ExpressionCache
from hmp.runtime.errors import HMPRuntimeError, HMPLimitError
from hmp.parser.parser import Parser, HMPParseError
from hmp.parser.ast import (
    Program,
    Statement,
    SetStatement,
    CallStatement,
    ImportStatement,
    ReturnStatement,
    IfStatement,
    LoopTimesStatement,
    WhileStatement,
    ForEachStatement,
    FunctionDef,
    TryCatchStatement,
    ParallelStatement,
    Expression,
    Literal,
    Variable,
    InterpolatedString,
)

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
            parser = Parser(script)
            program = parser.parse()
            self._register_functions_ast(program, context, result)
            self._execute_program(program, context, result)
            
            # Coleta todas as variaveis globais
            result["variables"] = {
                k: v for k, v in context.variables.items() 
                if not k.startswith('_') and k != 'last_result'
            }
        except HMPParseError as e:
            result["success"] = False
            result["error"] = str(e)
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
    
    def _register_functions_ast(
        self,
        program: Program,
        context: ExecutionContext,
        result: Dict
    ) -> None:
        """Registra funcoes definidas no script."""
        for statement in program.statements:
            if isinstance(statement, FunctionDef):
                context.functions[statement.name] = {
                    "params": statement.params,
                    "body": statement.body,
                }

    def _execute_program(
        self,
        program: Program,
        context: ExecutionContext,
        result: Dict
    ) -> None:
        """Executa o programa."""
        self._execute_statements(program.statements, context, result, in_function=False)

    def _execute_statements(
        self,
        statements: Sequence[Statement],
        context: ExecutionContext,
        result: Dict,
        in_function: bool
    ) -> Optional[Any]:
        for statement in statements:
            context.increment_iteration()
            context.check_limits()
            returned = self._execute_statement(statement, context, result, in_function)
            if in_function and returned is not None:
                return returned
        return None

    def _execute_statement(
        self,
        statement: Statement,
        context: ExecutionContext,
        result: Dict,
        in_function: bool
    ) -> Optional[Any]:
        if isinstance(statement, SetStatement):
            value = self._evaluate_expression(statement.value, context)
            context.set_variable(statement.name, value)
            return None
            
        if isinstance(statement, CallStatement):
            val = self._execute_call(statement, context, result)
            return val if in_function else None
            
        if isinstance(statement, ImportStatement):
            self._execute_import(statement, context, result)
            return None
            
        if isinstance(statement, ReturnStatement):
            value = self._evaluate_expression(statement.value, context)
            result["return_value"] = value
            return value if in_function else None
            
        if isinstance(statement, IfStatement):
            condition = self._evaluate_expression(statement.condition, context)
            if condition:
                return self._execute_statements(statement.body, context, result, in_function)
            elif statement.else_body:
                return self._execute_statements(statement.else_body, context, result, in_function)
            return None
            
        if isinstance(statement, LoopTimesStatement):
            count = self._evaluate_expression(statement.count, context)
            for _ in range(int(count)):
                context.check_limits()
                returned = self._execute_statements(statement.body, context, result, in_function)
                if in_function and returned is not None:
                    return returned
            return None
            
        if isinstance(statement, WhileStatement):
            while self._evaluate_expression(statement.condition, context):
                context.check_limits()
                returned = self._execute_statements(statement.body, context, result, in_function)
                if in_function and returned is not None:
                    return returned
            return None
            
        if isinstance(statement, ForEachStatement):
            items = self._evaluate_expression(statement.iterable, context)
            if not isinstance(items, (list, tuple)):
                items = []
            
            context.push_frame('foreach')
            try:
                for item in items:
                    context.check_limits()
                    context.set_variable(statement.var_name, item)
                    returned = self._execute_statements(statement.body, context, result, in_function)
                    if in_function and returned is not None:
                        return returned
            finally:
                context.pop_frame()
            return None
            
        if isinstance(statement, TryCatchStatement):
            try:
                returned = self._execute_statements(statement.body, context, result, in_function)
                if in_function and returned is not None:
                    return returned
            except Exception as e:
                context.push_frame('catch')
                try:
                    context.set_variable(statement.error_var, str(e))
                    returned = self._execute_statements(statement.catch_body, context, result, in_function)
                    if in_function and returned is not None:
                        return returned
                finally:
                    context.pop_frame()
            return None
            
        if isinstance(statement, ParallelStatement):
            return self._execute_statements(statement.body, context, result, in_function)
            
        return None

    def _execute_call(
        self,
        statement: CallStatement,
        context: ExecutionContext,
        result: Dict
    ) -> Any:
        # Prepara argumentos
        args = {name: self._evaluate_expression(expr, context) for name, expr in statement.params.items()}
        
        # Verifica se e uma funcao definida no script
        if statement.tool in context.functions:
            func = context.functions[statement.tool]
            params_names = func["params"]
            body = func["body"]
            
            local_vars = {}
            for i, p_name in enumerate(params_names):
                if p_name in args:
                    local_vars[p_name] = args[p_name]
                else:
                    local_vars[p_name] = None
            
            context.push_frame(statement.tool, local_vars, is_function=True)
            try:
                val = self._execute_statements(body, context, result, in_function=True)
            finally:
                context.pop_frame()
                
            if statement.target:
                context.set_variable(statement.target, val)
            
            context.set_variable('last_result', val)
            return val
        
        # Caso contrario, tenta executar como tool
        try:
            val = context.registry.execute(statement.tool, args, context)
            if statement.target:
                context.set_variable(statement.target, val)
            
            context.set_variable('last_result', val)
            return val
        except Exception as e:
            raise HMPRuntimeError(f"Erro ao chamar tool '{statement.tool}': {str(e)}")

    def _execute_import(
        self,
        statement: ImportStatement,
        context: ExecutionContext,
        result: Dict
    ) -> None:
        module_path = statement.path
        if module_path in self._imported_modules:
            return
            
        # Tenta carregar modulo
        p = Path(self.script_path) / f"{module_path}.hmp"
        if not p.exists():
            p = Path(self.script_path) / "modules" / f"{module_path}.hmp"
            
        if p.exists():
            try:
                content = p.read_text()
                parser = Parser(content)
                program = parser.parse()
                # Registra as funcoes do modulo no contexto atual
                self._register_functions_ast(program, context, result)
                # Executa o corpo do modulo (se houver comandos fora de funcoes)
                self._execute_statements(program.statements, context, result, in_function=False)
                self._imported_modules.add(module_path)
            except Exception as e:
                raise HMPRuntimeError(f"Erro ao importar modulo '{module_path}': {str(e)}")
        else:
            # Tenta no diretorio do script atual
            script_dir = os.path.dirname(os.path.abspath(self.script_path))
            p = Path(script_dir) / f"{module_path}.hmp"
            if p.exists():
                try:
                    content = p.read_text()
                    parser = Parser(content)
                    program = parser.parse()
                    self._register_functions_ast(program, context, result)
                    self._execute_statements(program.statements, context, result, in_function=False)
                    self._imported_modules.add(module_path)
                    return
                except Exception as e:
                    raise HMPRuntimeError(f"Erro ao importar modulo '{module_path}': {str(e)}")
            
            # Tenta no diretorio atual de execucao
            p = Path(os.getcwd()) / f"{module_path}.hmp"
            if p.exists():
                try:
                    content = p.read_text()
                    parser = Parser(content)
                    program = parser.parse()
                    self._register_functions_ast(program, context, result)
                    self._execute_statements(program.statements, context, result, in_function=False)
                    self._imported_modules.add(module_path)
                    return
                except Exception as e:
                    raise HMPRuntimeError(f"Erro ao importar modulo '{module_path}': {str(e)}")
            
            # Tenta na pasta examples se estiver rodando um exemplo
            p = Path(os.getcwd()) / "examples" / f"{module_path}.hmp"
            if p.exists():
                try:
                    content = p.read_text()
                    parser = Parser(content)
                    program = parser.parse()
                    self._register_functions_ast(program, context, result)
                    self._execute_statements(program.statements, context, result, in_function=False)
                    self._imported_modules.add(module_path)
                    return
                except Exception as e:
                    raise HMPRuntimeError(f"Erro ao importar modulo '{module_path}': {str(e)}")
            
            raise HMPRuntimeError(f"Modulo '{module_path}' nao encontrado em {self.script_path} ou caminhos alternativos.")

    def _evaluate_expression(self, expr: Expression, context: ExecutionContext) -> Any:
        # Prepara dicionario de variaveis consolidado para o safe_eval_expr
        vars_map = context.variables.copy()
        for frame in context.call_stack:
            vars_map.update(frame.variables)
            
        if isinstance(expr, Literal):
            val = expr.value
            if isinstance(val, list):
                return [self._evaluate_expression(e, context) if isinstance(e, Expression) else e for e in val]
            if isinstance(val, dict):
                return {k: self._evaluate_expression(v, context) if isinstance(v, Expression) else v for k, v in val.items()}
            return val
            
        if isinstance(expr, Variable):
            name = expr.name
            if name.startswith('${') and name.endswith('}'):
                return safe_eval_expr(name[2:-1], vars_map, self.cache)
            return context.get_variable(name)
            
        if isinstance(expr, InterpolatedString):
            res = ""
            for part in expr.parts:
                if isinstance(part, str):
                    res += part
                else:
                    val = self._evaluate_expression(part, context)
                    res += str(val)
            return res
            
        return None
