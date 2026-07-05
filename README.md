# PRISM v2 OS Kernel

Standalone, locally testable PRISM v2 kernel scaffold.

PRISM v2 converts user intent into a governed DAG and delegates execution to PRISM v1 through a bridge. By default the bridge runs in local mock mode so the kernel can be tested without GCP.

## Local test

```bash
cd prism-v2
python3 -m unittest discover -s tests -v
python3 main.py
```

## Run via API

```bash
curl -sS -H 'Content-Type: application/json' \
  -d '{"task":"build api service"}' \
  http://127.0.0.1:8080/run
```

## Real PRISM v1 bridge

Set `PRISM_V1_BASE_URL` to a deployed PRISM v1 service URL. The bridge calls `/api/coder/{operation}`.

```bash
export PRISM_V1_BASE_URL=https://<service>.run.app
```

## Runtime environment

- `PRISM_V1_BASE_URL`: optional PRISM v1 backend URL. Missing means local mock bridge.
- `PRISM_LAKEHOUSE_BASE_URL`: optional governance API URL. Missing means local governance rules.
- `PRISM_MODEL_CONFIG`: optional JSON file for model routes.
