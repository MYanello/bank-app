RUNTIME ?= nerdctl
REGISTRY ?= codeberg.org/marcusjy/bank-app
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
