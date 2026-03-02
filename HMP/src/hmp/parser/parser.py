"""Parser for HMP scripts into AST nodes."""

from __future__ import annotations

import ast as py_ast
from typing import List, Optional, Sequence, Dict, Any, Union

from hmp.parser.tokenizer import Tokenizer, Token, TokenType
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


class HMPParseError(Exception):
    """Erro de sintaxe no parser HMP."""

    def __init__(self, message: str, line: int, column: int = 0):
        super().__init__(f"Linha {line}, Coluna {column}: {message}")
        self.line = line
        self.column = column


class Parser:
    """Parser de scripts HMP para AST."""

    def __init__(self, source: str):
        tokenizer = Tokenizer(source)
        self._tokens = [t for t in tokenizer.tokenize() if t.type != TokenType.COMMENT]
        self._pos = 0

    def _peek(self, offset: int = 0) -> Token:
        if self._pos + offset < len(self._tokens):
            return self._tokens[self._pos + offset]
        return self._tokens[-1]

    def _advance(self) -> Token:
        token = self._peek()
        if token.type != TokenType.EOF:
            self._pos += 1
        return token

    def _match(self, *types: TokenType) -> bool:
        if self._peek().type in types:
            self._advance()
            return True
        return False

    def _expect(self, type: TokenType, message: str) -> Token:
        token = self._peek()
        if token.type == type:
            return self._advance()
        raise HMPParseError(message, token.line, token.column)

    def parse(self) -> Program:
        """Faz o parse do codigo fonte e retorna a AST."""
        statements = self._parse_block(stop_types=[TokenType.EOF])
        return Program(line=1, statements=statements)

    def _parse_block(self, stop_types: List[TokenType]) -> List[Statement]:
        statements: List[Statement] = []
        
        while self._peek().type not in stop_types and self._peek().type != TokenType.EOF:
            if self._match(TokenType.NEWLINE):
                continue
                
            statements.append(self._parse_statement())
            
            # Expect newline or EOF after statement
            if self._peek().type not in [TokenType.NEWLINE, TokenType.EOF] + stop_types:
                raise HMPParseError(f"Esperado nova linha apos comando, encontrado {self._peek().type} ({self._peek().value})", self._peek().line, self._peek().column)

        return statements

    def _parse_statement(self) -> Statement:
        token = self._peek()
        
        if self._match(TokenType.SET):
            return self._parse_set(token)
        if self._match(TokenType.CALL):
            return self._parse_call(token)
        if self._match(TokenType.IMPORT):
            return self._parse_import(token)
        if self._match(TokenType.IF):
            return self._parse_if(token)
        if self._match(TokenType.LOOP):
            return self._parse_loop(token)
        if self._match(TokenType.WHILE):
            return self._parse_while(token)
        if self._match(TokenType.FOR):
            return self._parse_for(token)
        if self._match(TokenType.FUNCTION):
            return self._parse_function(token)
        if self._match(TokenType.RETURN):
            return self._parse_return(token)
        if self._match(TokenType.TRY):
            return self._parse_try(token)
        if self._match(TokenType.PARALLEL):
            return self._parse_parallel(token)
            
        raise HMPParseError(f"Comando inesperado: {token.value}", token.line, token.column)

    def _parse_set(self, start_token: Token) -> SetStatement:
        name_token = self._expect(TokenType.IDENTIFIER, "Esperado nome da variavel apos SET")
        self._expect(TokenType.TO, "Esperado TO apos nome da variavel")
        value = self._parse_expression()
        return SetStatement(line=start_token.line, name=name_token.value, value=value)

    def _parse_call(self, start_token: Token) -> CallStatement:
        tool_token = self._expect(TokenType.IDENTIFIER, "Esperado nome da tool apos CALL")
        params = {}
        target = None
        
        if self._match(TokenType.WITH):
            while True:
                param_name = self._expect(TokenType.IDENTIFIER, "Esperado nome do parametro").value
                self._expect(TokenType.EQUALS, "Esperado '=' apos nome do parametro")
                param_value = self._parse_expression()
                params[param_name] = param_value
                
                if not self._match(TokenType.COMMA):
                    break
        
        if self._match(TokenType.AS):
            target = self._expect(TokenType.IDENTIFIER, "Esperado nome da variavel apos AS").value
            
        return CallStatement(line=start_token.line, tool=tool_token.value, params=params, target=target)

    def _parse_import(self, start_token: Token) -> ImportStatement:
        path_token = self._expect(TokenType.STRING, "Esperado caminho do modulo (string) apos IMPORT")
        path = path_token.value[1:-1]
        namespace = None
        if self._match(TokenType.AS):
            namespace = self._expect(TokenType.IDENTIFIER, "Esperado namespace apos AS").value
        return ImportStatement(line=start_token.line, path=path, namespace=namespace)

    def _parse_if(self, start_token: Token) -> IfStatement:
        condition = self._parse_complex_expression(stop_types=[TokenType.THEN])
        self._expect(TokenType.THEN, "Esperado THEN apos condicao do IF")
        self._match(TokenType.NEWLINE)
        
        body = self._parse_block(stop_types=[TokenType.ELSE, TokenType.ENDIF])
        else_body = []
        
        if self._match(TokenType.ELSE):
            self._match(TokenType.NEWLINE)
            else_body = self._parse_block(stop_types=[TokenType.ENDIF])
            
        self._expect(TokenType.ENDIF, "Esperado ENDIF para fechar bloco IF")
        return IfStatement(line=start_token.line, condition=condition, body=body, else_body=else_body)

    def _parse_loop(self, start_token: Token) -> LoopTimesStatement:
        count = self._parse_complex_expression(stop_types=[TokenType.TIMES])
        self._expect(TokenType.TIMES, "Esperado TIMES apos contagem do LOOP")
        self._match(TokenType.NEWLINE)
        body = self._parse_block(stop_types=[TokenType.ENDLOOP])
        self._expect(TokenType.ENDLOOP, "Esperado ENDLOOP para fechar bloco LOOP")
        return LoopTimesStatement(line=start_token.line, count=count, body=body)

    def _parse_while(self, start_token: Token) -> WhileStatement:
        condition = self._parse_complex_expression(stop_types=[TokenType.DO, TokenType.NEWLINE, TokenType.EOF])
        # Suporta ambas as sintaxes:
        # 1) WHILE <condicao>
        # 2) WHILE <condicao> DO
        self._match(TokenType.DO)
        self._match(TokenType.NEWLINE)
        body = self._parse_block(stop_types=[TokenType.ENDWHILE])
        self._expect(TokenType.ENDWHILE, "Esperado ENDWHILE para fechar bloco WHILE")
        return WhileStatement(line=start_token.line, condition=condition, body=body)

    def _parse_for(self, start_token: Token) -> ForEachStatement:
        self._expect(TokenType.EACH, "Esperado EACH apos FOR")
        var_name = self._expect(TokenType.IDENTIFIER, "Esperado nome da variavel apos FOR EACH").value
        self._expect(TokenType.IN, "Esperado IN apos variavel")
        iterable = self._parse_complex_expression(stop_types=[TokenType.NEWLINE, TokenType.EOF])
        self._match(TokenType.NEWLINE)
        body = self._parse_block(stop_types=[TokenType.ENDFOR])
        self._expect(TokenType.ENDFOR, "Esperado ENDFOR para fechar bloco FOR")
        return ForEachStatement(line=start_token.line, var_name=var_name, iterable=iterable, body=body)

    def _parse_function(self, start_token: Token) -> FunctionDef:
        name = self._expect(TokenType.IDENTIFIER, "Esperado nome da funcao").value
        params = []
        
        if self._match(TokenType.LPAREN):
            if not self._match(TokenType.RPAREN):
                while True:
                    param_name = self._expect(TokenType.IDENTIFIER, "Esperado nome do parametro").value
                    params.append(param_name)
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN, "Esperado ')' apos parametros")
        
        self._match(TokenType.NEWLINE)
        body = self._parse_block(stop_types=[TokenType.ENDFUNCTION])
        self._expect(TokenType.ENDFUNCTION, "Esperado ENDFUNCTION para fechar bloco FUNCTION")
        return FunctionDef(line=start_token.line, name=name, params=params, body=body)

    def _parse_return(self, start_token: Token) -> ReturnStatement:
        value = self._parse_expression()
        return ReturnStatement(line=start_token.line, value=value)

    def _parse_try(self, start_token: Token) -> TryCatchStatement:
        self._match(TokenType.NEWLINE)
        body = self._parse_block(stop_types=[TokenType.CATCH, TokenType.ENDTRY])
        catch_body = []
        error_var = "error"
        
        if self._match(TokenType.CATCH):
            if self._peek().type == TokenType.IDENTIFIER:
                error_var = self._advance().value
            self._match(TokenType.NEWLINE)
            catch_body = self._parse_block(stop_types=[TokenType.ENDTRY])
            
        self._expect(TokenType.ENDTRY, "Esperado ENDTRY para fechar bloco TRY")
        return TryCatchStatement(line=start_token.line, body=body, catch_body=catch_body, error_var=error_var)

    def _parse_parallel(self, start_token: Token) -> ParallelStatement:
        self._match(TokenType.NEWLINE)
        body = self._parse_block(stop_types=[TokenType.ENDPARALLEL])
        self._expect(TokenType.ENDPARALLEL, "Esperado ENDPARALLEL para fechar bloco PARALLEL")
        return ParallelStatement(line=start_token.line, body=body)

    def _parse_expression(self) -> Expression:
        token = self._advance()
        
        if token.type == TokenType.STRING:
            val = token.value[1:-1]
            if '${' in val:
                return self._parse_interpolated_string(val, token.line)
            return Literal(line=token.line, value=val)
            
        if token.type == TokenType.NUMBER:
            try:
                val = float(token.value)
                if val.is_integer():
                    val = int(val)
                return Literal(line=token.line, value=val)
            except ValueError:
                return Literal(line=token.line, value=token.value)
                
        if token.type == TokenType.EXPRESSION:
            expr_content = token.value[2:-1]
            return Variable(line=token.line, name=f"${{{expr_content}}}")
            
        if token.type == TokenType.IDENTIFIER:
            if token.value.lower() == 'true': return Literal(line=token.line, value=True)
            if token.value.lower() == 'false': return Literal(line=token.line, value=False)
            if token.value.lower() in ('none', 'null'): return Literal(line=token.line, value=None)
            return Variable(line=token.line, name=token.value)

        if token.type == TokenType.LBRACKET:
            elements = []
            if not self._match(TokenType.RBRACKET):
                while True:
                    elements.append(self._parse_expression())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RBRACKET, "Esperado colchete de fechamento")
            return Literal(line=token.line, value=elements)

        if token.type == TokenType.LBRACE:
            members = {}
            if not self._match(TokenType.RBRACE):
                while True:
                    key_token = self._expect(TokenType.STRING, "Esperado chave (string) para o dicionario")
                    self._expect(TokenType.COLON, "Esperado ':' apos a chave do dicionario")
                    value = self._parse_expression()
                    members[key_token.value[1:-1]] = value
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RBRACE, "Esperado chave de fechamento")
            return Literal(line=token.line, value=members)

        raise HMPParseError(f"Expressao invalida: {token.value}", token.line, token.column)

    def _parse_complex_expression(self, stop_types: List[TokenType]) -> Expression:
        start_line = self._peek().line
        expr_parts = []
        
        # Adicionamos ELSE e ENDIF como stop_types implicitos para evitar que sejam consumidos por expressoes
        actual_stop_types = stop_types + [TokenType.ELSE, TokenType.ENDIF, TokenType.ENDWHILE, TokenType.ENDFOR, TokenType.ENDLOOP, TokenType.ENDFUNCTION]
        
        while self._peek().type not in actual_stop_types and self._peek().type not in [TokenType.NEWLINE, TokenType.EOF]:
            token = self._advance()
            expr_parts.append(token.value)
            
        expr_str = " ".join(expr_parts).strip()
        if expr_str.startswith("${") and expr_str.endswith("}"):
            expr_str = expr_str[2:-1]
            
        return Variable(line=start_line, name=f"${{{expr_str}}}")

    def _parse_interpolated_string(self, content: str, line: int) -> InterpolatedString:
        import re
        parts: List[Union[str, Expression]] = []
        last_pos = 0
        for match in re.finditer(r'\$\{(.*?)\}', content):
            if match.start() > last_pos:
                parts.append(content[last_pos:match.start()])
            expr_str = match.group(1)
            parts.append(Variable(line=line, name=f"${{{expr_str}}}"))
            last_pos = match.end()
        if last_pos < len(content):
            parts.append(content[last_pos:])
        return InterpolatedString(line=line, parts=parts)
