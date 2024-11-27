FROM docker.io/python:3.12.7-alpine3.20 as builder

RUN apk --no-cache add gcc musl-dev

COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /opt/uv/bin

WORKDIR /tmp/newsmgrbot
ENV PYTHONOPTIMIZE=2 \
    UV_COMPILE_BYTECODE=1 \
    UV_FROZEN=1 \
    UV_NO_CACHE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/newsmgrbot \
    UV_PYTHON=/usr/local/bin/python
COPY pyproject.toml uv.lock .
RUN /opt/uv/bin/uv sync --no-dev --no-install-project
COPY src src
COPY README.rst .
RUN /opt/uv/bin/uv sync --no-dev --no-editable


FROM docker.io/python:3.12.7-alpine3.20

COPY --from=builder /opt/newsmgrbot /opt/newsmgrbot

RUN addgroup -S newsmgrbot \
    && adduser -G newsmgrbot -S -D -H newsmgrbot
USER newsmgrbot

ENV PYTHONOPTIMIZE=2 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/newsmgrbot/bin:$PATH"

CMD ["newsmgrbot", "run-polling"]
