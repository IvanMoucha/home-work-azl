# Development

## Dependency
* Python 3.12
* PostgreSQL 16
  * by default the connection is using localhost:5432, to set different host, set env `DB_HOST`
* `uv` package manager

## Development Environment Setup
* `uv venv --python 3.12`
* `source .venv/bin/activate`
* `uv sync`

## Run Processor (scheduled one)
* `uv run processor.py`

## Run API
* `./.venv/bin/uvicorn api:app --reload --port 5000 --access-log --use-colors`
* OpenAPI documentation is available at `http://localhost:5000/docs`
* Swagger UI is available at `http://localhost:5000/redoc`

## Run API on K8s
* default API Key is: `azul-api-key`

## Testing API
### K8s
* `curl --request GET --url http://127.0.0.1:8080/health --header 'apikey: azul-api-key'`
### Development
* `curl --request GET --url http://127.0.0.1:5000/health`

## Usage of LLM model
* set environmental variable to `LLM=1`, default is `LLM=0`
  * `Dockerfile` line 4 (for deployment)
  * in local development run `LLM=1 uv run processor.py`
* to preload the LLM model run: `./.venv/bin/huggingface-cli download --local-dir ./llm --resume-download --local-dir-use-symlinks=False unsloth/Llama-3.2-1B-Instruct`
  * preloading is recommended to avoid the download of the model on each run and speed up container build