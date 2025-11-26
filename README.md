# Heineken Observability Kit (New Relic + Python)

Kit de scripts en Python estilo SRE para enviar **métricas, logs y traces** a New Relic
para entornos de Heineken (plantas, sites, SAP, APIs, etc.).

## Contenido

- `metrics_host.py` — CPU, RAM, disco del host.
- `metrics_sap_ping.py` — healthchecks a endpoints de SAP / APIs internas.
- `logs_json.py` — logs estructurados en JSON a New Relic.
- `traces.py` — spans/traces manuales para batches y jobs.
- `synthetic_check.py` — synthetic checks a URLs definidas en `.env`.

## Uso rápido

```bash
pip install -r requirements.txt
cp .env.example .env
# edita .env con tus claves y endpoints

cd src
python metrics_host.py
python metrics_sap_ping.py
python synthetic_check.py
