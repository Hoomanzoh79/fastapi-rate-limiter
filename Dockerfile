# STAGE 1 — BUILDER  
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

RUN apt-get update && apt-get install --no-install-recommends -y curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# uv binary
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

WORKDIR /build

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# STAGE 2 — RUNTIME  
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_DIR=/app \
    USER=appuser

RUN useradd -m -s /usr/sbin/nologin $USER

WORKDIR $APP_DIR

# uv binary
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

COPY --from=builder /usr/local /usr/local
COPY --from=builder /build/src ./src
COPY --from=builder /build/pyproject.toml ./
COPY --from=builder /build/uv.lock ./

ENV PYTHONPATH=$APP_DIR

USER $USER

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --workers 4 --port 8000"]