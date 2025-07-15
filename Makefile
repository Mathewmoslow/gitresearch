# Makefile for concurrent analysis pipeline
SHELL := /bin/bash
OUTPUT_BASE := ~/Documents/gitresearch_outputs
.PHONY: all baseline archetypes simulation clean help

# Default target
all: baseline archetypes simulation
	@echo "✅ All analyses complete!"

# Help target
help:
	@echo "Available targets:"
	@echo "  make baseline    - Run baseline analysis"
	@echo "  make archetypes  - Run archetype analysis"
	@echo "  make simulation  - Run Monte Carlo simulation"
	@echo "  make all         - Run all analyses"
	@echo "  make clean       - Clean all outputs"
	@echo "  make status      - Show git status across branches"

# Baseline analysis
baseline:
	@echo "=== Running Baseline Analysis ==="
	python3 scripts/clean_data.py
	git checkout analysis-baseline
	python3 scripts/baseline_report.py
	-python3 scripts/git_auto_commit.py analysis-baseline "baseline run $$(date '+%Y-%m-%d %H:%M')"

# Archetype analysis  
archetypes: 
	@echo "=== Running Archetype Analysis ==="
	python3 scripts/clean_data.py
	git checkout analysis-archetypes
	# Ensure output directory exists
	mkdir -p $(OUTPUT_BASE)/analysis-archetypes
	# Copy baseline results if they exist
	-cp $(OUTPUT_BASE)/analysis-baseline/weekly_rollup.csv $(OUTPUT_BASE)/analysis-archetypes/ 2>/dev/null || true
	python3 scripts/archetype_report.py
	-python3 scripts/git_auto_commit.py analysis-archetypes "archetype run $$(date '+%Y-%m-%d %H:%M')"

# Simulation analysis
simulation:
	@echo "=== Running Simulation Analysis ==="
	python3 scripts/clean_data.py
	git checkout analysis-simulation
	# Ensure output directory exists
	mkdir -p $(OUTPUT_BASE)/analysis-simulation
	# Try to copy from baseline
	-cp $(OUTPUT_BASE)/analysis-baseline/weekly_rollup.csv $(OUTPUT_BASE)/analysis-simulation/ 2>/dev/null || true
	python3 scripts/simulation_report.py
	-python3 scripts/git_auto_commit.py analysis-simulation "simulation run $$(date '+%Y-%m-%d %H:%M')"

# Clean all outputs
clean:
	@echo "=== Cleaning outputs ==="
	rm -rf $(OUTPUT_BASE)/analysis-*
	@echo "✅ Outputs cleaned"

# Show status across all branches
status:
	@echo "=== Git Status Across Branches ==="
	@for branch in main analysis-baseline analysis-archetypes analysis-simulation; do \
		echo -e "\n--- $$branch ---"; \
		git log $$branch --oneline -1 2>/dev/null || echo "Branch not found"; \
	done
	@echo -e "\n=== Current Branch ==="
	@git branch --show-current

# Dashboard creation
dashboard:
	@echo "=== Creating Final Dashboard ==="
	python3 scripts/final_dashboard.py