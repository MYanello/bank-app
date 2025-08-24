RUNTIME ?= nerdctl
REGISTRY ?= ghcr.io/myanello/bank-app
BUILD_TARGET ?= debug
TAG := latest
IMAGE := $(REGISTRY):$(TAG)


.PHONY: build
build:
	$(RUNTIME) build -t $(IMAGE) --target $(BUILD_TARGET) .
.PHONY: push
push:
	$(RUNTIME) push $(IMAGE)
.PHONY: build-push
build-push: build push

.PHONY: run-docker
run-docker:
	$(RUNTIME) run --rm -p 8000:8000 $(IMAGE)

.PHONY: run-uv
run-uv:
	cd src && uv run main.py

.PHONY: install-poetry
install-poetry:
	python -m venv .venv
	poetry install

.PHONY: run-poetry
run-poetry: install-poetry
	source .venv/bin/activate && cd src && poetry run python main.py