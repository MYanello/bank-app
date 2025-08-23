ARG DEBUG_IMAGE=ghcr.io/astral-sh/uv
ARG TAG=python3.13-trixie-slim
ARG DIGEST=sha256:07c6e125ca9f440b4d420b9e877aa11c0f44a406969c09d90c6f6ebb518d474c

FROM $DEBUG_IMAGE:$DEBUG_TAG@$DEBUG_DIGST AS debug

WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./.python-version ./
RUN uv sync --locked

COPY ./src ./

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
EXPOSE 8080

CMD ["uv", "run", "main.py"]
