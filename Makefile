PYTHON := 3.14
UV := uv
APP := nerd_life.py

.PHONY: help run run-plain run-nerd run-forever refresh-icons sync lock clean

help:
	@printf "Available targets:\n"
	@printf "  make run            - Run with block icons\n"
	@printf "  make run-plain      - Run with plain ASCII icons\n"
	@printf "  make run-nerd       - Run with Nerd Font icons\n"
	@printf "  make run-forever    - Run forever (until Ctrl+C)\n"
	@printf "  make refresh-icons  - Refresh Nerd Font glyph cache\n"
	@printf "  make sync           - Create/update uv environment\n"
	@printf "  make lock           - Update uv.lock\n"
	@printf "  make clean          - Remove local caches and bytecode\n"

run:
	$(UV) run --python $(PYTHON) $(APP) --icons blocks

run-plain:
	$(UV) run --python $(PYTHON) $(APP) --icons plain

run-nerd:
	$(UV) run --python $(PYTHON) $(APP) --icons nerd

run-forever:
	$(UV) run --python $(PYTHON) $(APP) --iterations 0

refresh-icons:
	$(UV) run --python $(PYTHON) $(APP) --icons nerd --refresh-icons

sync:
	$(UV) sync --python $(PYTHON)

lock:
	$(UV) lock --python $(PYTHON)

clean:
	rm -rf .venv .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
