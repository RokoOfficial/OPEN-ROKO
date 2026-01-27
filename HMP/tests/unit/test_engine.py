"""Testes unitarios para o HMP Engine."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hmp import run_script, list_tools
from hmp.core.engine import HMPEngine


class TestVariables:
    """Testes de variaveis."""
    
    def test_set_string(self):
        result = run_script('SET nome TO "Maria"')
        assert result['variables']['nome'] == 'Maria'
    
    def test_set_number(self):
        result = run_script('SET idade TO 25')
        assert result['variables']['idade'] == 25
    
    def test_set_float(self):
        result = run_script('SET preco TO 19.99')
        assert result['variables']['preco'] == 19.99
    
    def test_set_list(self):
        result = run_script('SET frutas TO ["maca", "banana"]')
        assert result['variables']['frutas'] == ['maca', 'banana']
    
    def test_set_expression(self):
        result = run_script('''
            SET a TO 10
            SET b TO ${a * 2}
        ''')
        assert result['variables']['b'] == 20


class TestExpressions:
    """Testes de expressoes."""
    
    def test_arithmetic(self):
        result = run_script('SET x TO ${5 + 3 * 2}')
        assert result['variables']['x'] == 11
    
    def test_comparison(self):
        result = run_script('''
            SET a TO 10
            SET b TO ${a > 5}
        ''')
        assert result['variables']['b'] == True
    
    def test_string_interpolation(self):
        result = run_script('''
            SET nome TO "Mundo"
            SET msg TO "Ola, ${nome}!"
        ''')
        assert result['variables']['msg'] == 'Ola, Mundo!'


class TestLoops:
    """Testes de loops."""
    
    def test_loop_times(self):
        result = run_script('''
            SET soma TO 0
            LOOP 5 TIMES
                SET soma TO ${soma + 1}
            ENDLOOP
        ''')
        assert result['variables']['soma'] == 5
    
    def test_for_each(self):
        result = run_script('''
            SET numeros TO [1, 2, 3]
            SET soma TO 0
            FOR EACH n IN ${numeros}
                SET soma TO ${soma + n}
            ENDFOR
        ''')
        assert result['variables']['soma'] == 6
    
    def test_while(self):
        result = run_script('''
            SET i TO 0
            WHILE ${i} < 5
                SET i TO ${i + 1}
            ENDWHILE
        ''')
        assert result['variables']['i'] == 5


class TestConditionals:
    """Testes de condicionais."""
    
    def test_if_true(self):
        result = run_script('''
            SET x TO 10
            IF ${x} > 5 THEN
                SET resultado TO "maior"
            ENDIF
        ''')
        assert result['variables']['resultado'] == 'maior'
    
    def test_if_else(self):
        result = run_script('''
            SET x TO 3
            IF ${x} > 5 THEN
                SET resultado TO "maior"
            ELSE
                SET resultado TO "menor"
            ENDIF
        ''')
        assert result['variables']['resultado'] == 'menor'


class TestFunctions:
    """Testes de funcoes."""
    
    def test_function_simple(self):
        result = run_script('''
            FUNCTION dobro(x)
                RETURN ${x * 2}
            ENDFUNCTION
            
            CALL dobro WITH x=5
            SET resultado TO ${last_result["default"]}
        ''')
        assert result['variables']['resultado'] == 10
    
    def test_function_multiple_params(self):
        result = run_script('''
            FUNCTION soma(a, b)
                RETURN ${a + b}
            ENDFUNCTION
            
            CALL soma WITH a=10, b=20
            SET resultado TO ${last_result["default"]}
        ''')
        assert result['variables']['resultado'] == 30


class TestTools:
    """Testes de tools."""
    
    def test_list_tools(self):
        tools = list_tools()
        assert len(tools) >= 64
        assert 'math.sum' in tools
        assert 'string.upper' in tools
        assert 'list.length' in tools
    
    def test_math_sum(self):
        result = run_script('''
            CALL math.sum WITH a=10, b=5
        ''')
        assert 'output' in result
    
    def test_string_upper(self):
        result = run_script('''
            CALL string.upper WITH text="hello"
        ''')
        assert 'output' in result


class TestErrorHandling:
    """Testes de tratamento de erros."""
    
    def test_try_catch(self):
        result = run_script('''
            SET resultado TO "falhou"
            TRY
                SET resultado TO "sucesso"
            CATCH
                SET resultado TO "erro"
            ENDTRY
        ''')
        assert result['variables']['resultado'] == 'sucesso'


class TestReturn:
    """Testes de retorno."""
    
    def test_return_string(self):
        result = run_script('RETURN "ok"')
        assert result['return_value'] == 'ok'
    
    def test_return_number(self):
        result = run_script('RETURN 42')
        assert result['return_value'] == 42
    
    def test_return_expression(self):
        result = run_script('''
            SET x TO 10
            RETURN ${x * 2}
        ''')
        assert result['return_value'] == 20


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
