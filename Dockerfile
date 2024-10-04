FROM python:3.12-bookworm
LABEL authors="Ivan Moucha"

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/" sh

COPY processor.py /
COPY pyproject.toml /
COPY src/ src/

RUN uv venv --python 3.12 \
    && uv sync

ENTRYPOINT ["uv", "run", "processor.py"]