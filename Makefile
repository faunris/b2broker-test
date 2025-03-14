.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: install-hooks
install-hooks:
	pre-commit install

.PHONY: uninstall-hooks
uninstall-hooks:
	pre-commit uninstall
