# Projetos HMP (complexos e validados)

Esta pasta reúne sistemas HMP mais completos, cobrindo automação, orquestração e fluxo com LLM/fallback.

## Projetos

1. `automacao_incidentes.hmp`
   - Classificação de incidentes, priorização e ação automática.

2. `orquestracao_etl_resiliente.hmp`
   - ETL resiliente com descarte de dados inválidos e relatório final.

3. `fluxo_llm_classificacao.hmp`
   - Pipeline de classificação com tentativa HTTP para LLM e fallback determinístico local.

4. `orquestrador_multiagente.hmp`
   - Orquestração de etapas por agentes (planner/executor/qa) com histórico.

## Como validar

No diretório `HMP`:

```bash
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from hmp.core.engine import HMPEngine

engine = HMPEngine()
files = sorted(Path('projetos').glob('*.hmp'))
for f in files:
    result = engine.execute(f.read_text(encoding='utf-8'))
    print(f.name, '=>', 'OK' if result['success'] else result['error'])
PY
```

Todos os scripts desta pasta foram validados dessa forma neste ambiente.
