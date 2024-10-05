FROM python:3.12-bookworm
LABEL authors="Ivan Moucha"

ENV LLM=0

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/" sh

COPY processor.py /
COPY pyproject.toml /
COPY src/ src/
COPY /llm /llm

RUN uv venv --python 3.12 \
    && uv sync \
    && . /.venv/bin/activate

RUN if [ "$LLM" -eq 1 ]; then \
        /.venv/bin/huggingface-cli download --local-dir /llm --resume-download unsloth/Llama-3.2-1B-Instruct; \
    fi

ENTRYPOINT ["uv", "run", "processor.py"]