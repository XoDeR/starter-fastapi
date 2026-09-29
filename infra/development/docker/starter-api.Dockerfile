FROM ghcr.io/astral-sh/uv:latest AS uv
FROM python:3.12-slim-bookworm

COPY --from=uv /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY starter-api/pyproject.toml starter-api/uv.lock /app/
RUN uv sync --frozen --no-dev --no-install-project

COPY starter-api/ /app/
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["sh", "/app/scripts/start.sh"]
