UV = uv
MIX = mix

.PHONY: all install install-elixir install-python run test lint validate clean

all: install

install: install-elixir install-python

install-elixir:
	$(MIX) deps.get

install-python:
	cd python && $(UV) sync

run:
	$(MIX) run

test:
	$(MIX) test

lint:
	$(MIX) format --check-formatted
	cd python && $(UV) run ruff check .

validate: lint test

clean:
	rm -rf _build deps
	rm -rf python/.venv python/__pycache__
