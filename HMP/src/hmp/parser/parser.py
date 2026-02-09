"""Parser for HMP scripts into AST nodes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Sequence

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


class HMPParseError(Exception):
    """Erro de sintaxe no parser HMP."""

    def __init__(self, message: str, line: int):
        super().__init__(f"Linha {line}: {message}")
        self.line = line


@dataclass
class _Line:
    number: int
    text: str


class Parser:
    """Parser de scripts HMP para AST."""

    def __init__(self, source: str):
        self._lines = [
            _Line(number=i + 1, text=line)
            for i, line in enumerate(source.splitlines())
        ]
        self._index = 0

    def parse(self) -> Program:
        """Faz o parse do codigo fonte e retorna a AST."""
        statements = self._parse_block(stop_keywords=None)
        return Program(line=1, statements=statements)

    def _parse_block(self, stop_keywords: Optional[Sequence[str]]) -> List[Statement]:
        statements: List[Statement] = []

        while self._index < len(self._lines):
            current = self._lines[self._index]
            text = current.text.strip()

            if stop_keywords and text in stop_keywords:
                break

            if not text or text.startswith('#'):
                self._index += 1
                continue

            if text.startswith('FUNCTION '):
                statements.append(self._parse_function(current))
                continue

            if text.startswith('IF ') and 'THEN' in text:
                statements.append(self._parse_if(current))
                continue

            if text.startswith('LOOP ') and 'TIMES' in text:
                statements.append(self._parse_loop_times(current))
                continue

            if text.startswith('WHILE '):
                statements.append(self._parse_while(current))
                continue

            if text.startswith('FOR EACH '):
                statements.append(self._parse_for_each(current))
                continue

            if text == 'TRY':
                statements.append(self._parse_try(current))
                continue

            if text == 'PARALLEL':
                statements.append(self._parse_parallel(current))
                continue

            if text.startswith('IMPORT '):
                statements.append(self._parse_import(current))
                self._index += 1
                continue

            if text.startswith('SET '):
                statements.append(self._parse_set(current))
                self._index += 1
                continue

            if text.startswith('CALL '):
                statements.append(self._parse_call(current))
                self._index += 1
                continue

            if text.startswith('RETURN '):
                statements.append(self._parse_return(current))
                self._index += 1
                continue

            raise HMPParseError(f"Comando desconhecido: {text}", current.number)

        return statements

    def _parse_set(self, line: _Line) -> SetStatement:
        match = re.match(r'SET\s+(\w+)\s+TO\s+(.+)', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em SET", line.number)
        return SetStatement(line=line.number, name=match.group(1), value=match.group(2))

    def _parse_call(self, line: _Line) -> CallStatement:
        match = re.match(r'CALL\s+([\w.]+)\s+WITH\s+(.+)', line.text.strip())
        if match:
            return CallStatement(line=line.number, tool=match.group(1), params=match.group(2))
        match = re.match(r'CALL\s+([\w.]+)', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em CALL", line.number)
        return CallStatement(line=line.number, tool=match.group(1), params=None)

    def _parse_import(self, line: _Line) -> ImportStatement:
        match = re.match(r'IMPORT\s+(".*?"|\'.*?\')(\s+AS\s+(\w+))?', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em IMPORT", line.number)
        path_literal = match.group(1)
        namespace = match.group(3)
        path = path_literal[1:-1]
        return ImportStatement(line=line.number, path=path, namespace=namespace)

    def _parse_return(self, line: _Line) -> ReturnStatement:
        value = line.text.strip()[7:].strip()
        if not value:
            raise HMPParseError("RETURN requer um valor", line.number)
        return ReturnStatement(line=line.number, value=value)

    def _parse_if(self, line: _Line) -> IfStatement:
        match = re.match(r'IF\s+(.+)\s+THEN', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em IF", line.number)
        condition = match.group(1)
        self._index += 1
        body = self._parse_block(stop_keywords=('ELSE', 'ENDIF'))
        else_body: List[Statement] = []

        if self._index >= len(self._lines):
            raise HMPParseError("ENDIF nao encontrado", line.number)

        current = self._lines[self._index].text.strip()
        if current == 'ELSE':
            self._index += 1
            else_body = self._parse_block(stop_keywords=('ENDIF',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDIF':
            raise HMPParseError("ENDIF nao encontrado", line.number)
        self._index += 1
        return IfStatement(line=line.number, condition=condition, body=body, else_body=else_body)

    def _parse_loop_times(self, line: _Line) -> LoopTimesStatement:
        match = re.match(r'LOOP\s+(.+)\s+TIMES', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em LOOP", line.number)
        count = match.group(1)
        self._index += 1
        body = self._parse_block(stop_keywords=('ENDLOOP',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDLOOP':
            raise HMPParseError("ENDLOOP nao encontrado", line.number)
        self._index += 1
        return LoopTimesStatement(line=line.number, count=count, body=body)

    def _parse_while(self, line: _Line) -> WhileStatement:
        match = re.match(r'WHILE\s+(.+)', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em WHILE", line.number)
        condition = match.group(1)
        self._index += 1
        body = self._parse_block(stop_keywords=('ENDWHILE',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDWHILE':
            raise HMPParseError("ENDWHILE nao encontrado", line.number)
        self._index += 1
        return WhileStatement(line=line.number, condition=condition, body=body)

    def _parse_for_each(self, line: _Line) -> ForEachStatement:
        match = re.match(r'FOR EACH\s+(\w+)\s+IN\s+(.+)', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em FOR EACH", line.number)
        var_name = match.group(1)
        iterable = match.group(2)
        self._index += 1
        body = self._parse_block(stop_keywords=('ENDFOR',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDFOR':
            raise HMPParseError("ENDFOR nao encontrado", line.number)
        self._index += 1
        return ForEachStatement(line=line.number, var_name=var_name, iterable=iterable, body=body)

    def _parse_function(self, line: _Line) -> FunctionDef:
        match = re.match(r'FUNCTION\s+(\w+)\s*\(([^)]*)\)', line.text.strip())
        if not match:
            raise HMPParseError("Sintaxe invalida em FUNCTION", line.number)
        name = match.group(1)
        params_str = match.group(2).strip()
        params = [p.strip() for p in params_str.split(',')] if params_str else []
        self._index += 1
        body = self._parse_block(stop_keywords=('ENDFUNCTION',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDFUNCTION':
            raise HMPParseError("ENDFUNCTION nao encontrado", line.number)
        self._index += 1
        return FunctionDef(line=line.number, name=name, params=params, body=body)

    def _parse_try(self, line: _Line) -> TryCatchStatement:
        self._index += 1
        body = self._parse_block(stop_keywords=('CATCH', 'ENDTRY'))
        catch_body: List[Statement] = []

        if self._index >= len(self._lines):
            raise HMPParseError("ENDTRY nao encontrado", line.number)

        current = self._lines[self._index].text.strip()
        if current == 'CATCH':
            self._index += 1
            catch_body = self._parse_block(stop_keywords=('ENDTRY',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDTRY':
            raise HMPParseError("ENDTRY nao encontrado", line.number)
        self._index += 1
        return TryCatchStatement(line=line.number, body=body, catch_body=catch_body)

    def _parse_parallel(self, line: _Line) -> ParallelStatement:
        self._index += 1
        body = self._parse_block(stop_keywords=('ENDPARALLEL',))
        if self._index >= len(self._lines) or self._lines[self._index].text.strip() != 'ENDPARALLEL':
            raise HMPParseError("ENDPARALLEL nao encontrado", line.number)
        self._index += 1
        return ParallelStatement(line=line.number, body=body)
