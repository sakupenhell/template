FROM python:3.14-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

COPY uv.lock pyproject.toml ./

RUN uv venv /app/.venv && \
    uv sync --frozen --no-dev --no-install-project


FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --system --gid 10001 appgroup && \
    useradd --system --uid 10001 --gid appgroup --no-create-home --shell /sbin/nologin appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/.venv .venv
COPY --chown=appuser:appgroup . .

RUN chown -R root:root .venv && \
    chmod -R a-w .venv

EXPOSE 8000

USER 10001:10001

CMD ["python", "-m", "robyn", "main.py"]
