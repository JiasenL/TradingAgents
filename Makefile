SHELL      := /usr/bin/env zsh
.SHELLFLAGS := -i -c

.PHONY: run shell

# conda activate tradingagents
run:
	set -a && . $(CURDIR)/.env && set +a && \
	python -m cli.main
