FROM docker.io/python:3.12.5-alpine3.20

ENV PYTHONOPTIMIZE=2
ENV UV_REQUIRE_HASHES=true
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app
COPY . .
RUN --mount=from=ghcr.io/astral-sh/uv:0.4.4,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["newsmgrbot"]
CMD ["run-polling"]
