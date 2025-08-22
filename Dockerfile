ARG DEBUG_IMAGE=ghcr.io/astral-sh/uv:python3.13-trixie-slim@sha256:07c6e125ca9f440b4d420b9e877aa11c0f44a406969c09d90c6f6ebb518d474c


FROM $DEBUG_IMAGE AS debug

WORKDIR /app
COPY ./src/pyproject.toml ./src/uv.lock ./src/.python-version ./
RUN uv sync
COPY ./src ./

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
EXPOSE 8080
