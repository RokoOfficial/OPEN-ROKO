"""
Modulo de contribuicoes e extensoes do HMP.

Este modulo contem tools opcionais e extensoes de terceiros.
Para criar sua propria extensao, crie um ToolProvider e registre-o.

Exemplo:
    from hmp.tools.base import BaseTool, ToolProvider
    
    class MinhaToolProvider(ToolProvider):
        def get_tools(self):
            return [MinhaTool()]
"""
