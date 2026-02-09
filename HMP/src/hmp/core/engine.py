"""Motor de execucao do HMP."""

import json
import re
import os
from typing import Any, Dict, List, Optional, Sequence
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
            parser = Parser(script)
            program = parser.parse()
            self._register_functions_ast(program, context, result)
            self._execute_program(program, context, result)
            result["variables"] = {
                k: v for k, v in context.variables.items() 
                if not k.startswith('_')
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
        """Registra funcoes definidas no script a partir da AST."""
        for statement in self._walk_statements(program.statements):
            if isinstance(statement, FunctionDef):
                context.functions[statement.name] = {
                    "params": statement.params,
                    "body": statement.body,
                }
                result["output"].append(
                    f"[FUNCTION] {statement.name}({', '.join(statement.params)}) definida"
                )

    def _walk_statements(
        self,
        statements: Sequence[Statement]
    ) -> Sequence[Statement]:
        """Percorre a arvore de statements em profundidade."""
        collected: List[Statement] = []
        for statement in statements:
            collected.append(statement)
            if isinstance(statement, IfStatement):
                collected.extend(self._walk_statements(statement.body))
                collected.extend(self._walk_statements(statement.else_body))
            elif isinstance(statement, LoopTimesStatement):
                collected.extend(self._walk_statements(statement.body))
            elif isinstance(statement, WhileStatement):
                collected.extend(self._walk_statements(statement.body))
            elif isinstance(statement, ForEachStatement):
                collected.extend(self._walk_statements(statement.body))
            elif isinstance(statement, TryCatchStatement):
                collected.extend(self._walk_statements(statement.body))
                collected.extend(self._walk_statements(statement.catch_body))
            elif isinstance(statement, ParallelStatement):
                collected.extend(self._walk_statements(statement.body))
            elif isinstance(statement, FunctionDef):
                collected.extend(self._walk_statements(statement.body))
        return collected
    
    def _execute_program(
        self,
        program: Program,
        context: ExecutionContext,
        result: Dict
    ) -> None:
        """Executa statements a partir da AST."""
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
            value = self._parse_value(statement.value, context)
            context.set_variable(statement.name, value)
            result["output"].append(f"SET {statement.name} = {value}")
            return None
        if isinstance(statement, CallStatement):
            self._execute_call(statement, context, result)
            return None
        if isinstance(statement, ImportStatement):
            self._execute_import(statement, context, result)
            return None
        if isinstance(statement, ReturnStatement):
            value = self._parse_value(statement.value, context)
            result["return_value"] = value
            result["output"].append(f"RETURN: {value}")
            return value if in_function else None
        if isinstance(statement, FunctionDef):
            return None
        if isinstance(statement, IfStatement):
            condition = self._evaluate_expression(statement.condition, context)
            context.push_frame('if')
            try:
                body = statement.body if condition else statement.else_body
                returned = self._execute_statements(
                    body, context, result, in_function=in_function
                )
                if in_function and returned is not None:
                    return returned
            finally:
                context.pop_frame()
            return None
        if isinstance(statement, LoopTimesStatement):
            count_value = self._parse_value(statement.count, context)
            try:
                count = int(count_value)
            except (TypeError, ValueError):
                count = 0
            count = min(count, self.config.max_loop_iterations)
            context.push_frame('loop')
            try:
                for i in range(count):
                    context.check_limits()
                    context.set_variable('_loop_index', i)
                    context.set_variable('loop_index', i)
                    returned = self._execute_statements(
                        statement.body, context, result, in_function=in_function
                    )
                    if in_function and returned is not None:
                        return returned
            finally:
                context.pop_frame()
            return None
        if isinstance(statement, WhileStatement):
            context.push_frame('while')
            try:
                while self._evaluate_expression(statement.condition, context):
                    context.check_limits()
                    returned = self._execute_statements(
                        statement.body, context, result, in_function=in_function
                    )
                    if in_function and returned is not None:
                        return returned
            finally:
                context.pop_frame()
            return None
        if isinstance(statement, ForEachStatement):
            items = self._parse_value(statement.items, context)
            if not isinstance(items, list):
                items = []
            context.push_frame('foreach')
            try:
                for item in items:
                    context.check_limits()
                    context.set_variable(statement.var_name, item)
                    returned = self._execute_statements(
                        statement.body, context, result, in_function=in_function
                    )
                    if in_function and returned is not None:
                        return returned
            finally:
                context.pop_frame()
            return None
        if isinstance(statement, TryCatchStatement):
            try:
                returned = self._execute_statements(
                    statement.body, context, result, in_function=in_function
                )
                if in_function and returned is not None:
                    return returned
            except Exception as e:
                context.push_frame('catch')
                try:
                    context.set_variable(statement.error_var, str(e))
                    returned = self._execute_statements(
                        statement.catch_body, context, result, in_function=in_function
                    )
                    if in_function and returned is not None:
                        return returned
                finally:
                    context.pop_frame()
            return None
        if isinstance(statement, ParallelStatement):
            # Execucao sequencial para manter determinismo no motor base
            # Extensoes podem implementar paralelismo real
            returned = self._execute_statements(
                statement.body, context, result, in_function=in_function
            )
            if in_function and returned is not None:
                return returned
            return None
        
        return None

    def _execute_call(
        self,
        statement: CallStatement,
        context: ExecutionContext,
        result: Dict
    ) -> Any:
        # Verifica se e uma funcao definida no script
        if statement.name in context.functions:
            func = context.functions[statement.name]
            params = func["params"]
            body = func["body"]
            
            # Prepara argumentos
            args = {}
            for i, param_name in enumerate(params):
                if i < len(statement.args):
                    args[param_name] = self._parse_value(statement.args[i], context)
                else:
                    args[param_name] = None
            
            # Executa corpo da funcao em novo frame
            context.push_frame(statement.name, args)
            try:
                return self._execute_statements(body, context, result, in_function=True)
            finally:
                context.pop_frame()
        
        # Caso contrario, tenta executar como tool
        args = [self._parse_value(arg, context) for arg in statement.args]
        try:
            val = context.registry.execute(statement.name, args, context)
            if statement.target:
                context.set_variable(statement.target, val)
                result["output"].append(f"CALL {statement.name} -> {statement.target} = {val}")
            else:
                result["output"].append(f"CALL {statement.name} -> {val}")
            return val
        except Exception as e:
            raise HMPRuntimeError(f"Erro ao chamar tool '{statement.name}': {str(e)}")

    def _execute_import(
        self,
        statement: ImportStatement,
        context: ExecutionContext,
        result: Dict
    ) -> None:
        module_name = statement.module
        if module_name in self._imported_modules:
            return
            
        # Tenta carregar modulo do sistema de arquivos
        possible_paths = [
            Path(self.script_path) / f"{module_name}.hmp",
            Path(self.script_path) / "modules" / f"{module_name}.hmp",
            Path(__file__).parent.parent / "stdlib" / f"{module_name}.hmp"
        ]
        
        content = None
        for p in possible_paths:
            if p.exists():
                content = p.read_text()
                break
        
        if content:
            try:
                parser = Parser(content)
                program = parser.parse()
                self._register_functions_ast(program, context, result)
                self._imported_modules.add(module_name)
                result["output"].append(f"IMPORT {module_name} sucesso")
            except Exception as e:
                raise HMPRuntimeError(f"Erro ao importar modulo '{module_name}': {str(e)}")
        else:
            # Tenta carregar como provider nativo se existir
            try:
                # Logica para carregar providers dinamicos se necessario
                result["output"].append(f"IMPORT {module_name} (nativo) ignorado")
            except Exception:
                raise HMPRuntimeError(f"Modulo '{module_name}' nao encontrado")

    def _parse_value(self, value: Any, context: ExecutionContext) -> Any:
        if isinstance(value, str) and value.startswith('$'):
            var_name = value[1:]
            return context.get_variable(var_name)
        if isinstance(value, str) and (value.startswith('{{') and value.endswith('}}')):
            expr = value[2:-2].strip()
            return self._evaluate_expression(expr, context)
        return value

    def _evaluate_expression(self, expr: str, context: ExecutionContext) -> Any:
        return safe_eval_expr(expr, context.variables, self.cache)
