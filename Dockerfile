FROM ghcr.io/astral-sh/uv:0.13.9 AS uv

FROM python:3.14-slim

COPY --from=uv /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    MCP_TRANSPORT=http \
    PORT=8000

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY server.py .

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "python", "server.py"]
