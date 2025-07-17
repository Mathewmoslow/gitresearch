# Makefile for Graduate Research Workload Analysis with Data Integrity
# Author: Mathew Moslo
# Ensures computational reproducibility for research

# Define output directory
OUTPUT_DIR := ~/Documents/gitresearch_outputs

# Python interpreter
PYTHON := python3
VENV := venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

# Default target
.PHONY: all
all: venv verify-env baseline archetypes simulation
	@echo "✅ All analyses complete!"
	@echo "⚠️  Remember to run 'make lock-env' to preserve environment for reproducibility"

# Create and setup virtual environment
.PHONY: venv
venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	@echo "=== Setting up virtual environment ==="
	@$(PYTHON) --version
	@$(PYTHON) -m venv $(VENV)
	@$(VENV_PIP) install --upgrade pip setuptools wheel
	@if [ -f "requirements_lock.txt" ]; then \
		echo "Installing from locked requirements..."; \
		$(VENV_PIP) install -r requirements_lock.txt; \
	else \
		echo "Installing fresh packages (no lock file found)..."; \
		$(VENV_PIP) install pandas numpy matplotlib seaborn scipy; \
	fi
	@echo "✅ Virtual environment ready"

# Lock current environment for reproducibility
.PHONY: lock-env
lock-env: venv
	@echo "=== Locking environment versions ==="
	@$(VENV_PIP) freeze > requirements_lock.txt
	@$(VENV_PYTHON) -c "import pandas, numpy; print(f'Locked: pandas=={pandas.__version__}, numpy=={numpy.__version__}')"
	@echo "✅ Environment locked to requirements_lock.txt"
	@echo "📝 Add requirements_lock.txt to git for reproducibility"

# Verify environment matches research requirements
.PHONY: verify-env
verify-env: venv
	@echo "=== Verifying environment integrity ==="
	@$(VENV_PYTHON) verify_environment.py || (echo "❌ Environment verification failed!" && exit 1)

# Create reproducible environment from lock file
.PHONY: reproduce-env
reproduce-env:
	@echo "=== Creating reproducible environment ==="
	@if [ ! -f "requirements_lock.txt" ]; then \
		echo "❌ No requirements_lock.txt found!"; \
		exit 1; \
	fi
	@rm -rf venv_reproduce
	@$(PYTHON) -m venv venv_reproduce
	@venv_reproduce/bin/pip install --upgrade pip
	@venv_reproduce/bin/pip install -r requirements_lock.txt
	@echo "✅ Reproducible environment created in venv_reproduce/"
	@echo "Run: source venv_reproduce/bin/activate"

# Generate integrity report
.PHONY: integrity-report
integrity-report: venv
	@echo "=== Generating Research Integrity Report ==="
	@$(VENV_PYTHON) generate_integrity_report.py
	@echo "✅ Integrity report saved to $(OUTPUT_DIR)/RESEARCH_INTEGRITY.md"

# Clean all outputs
.PHONY: clean
clean:
	@echo "=== Cleaning outputs ==="
	rm -rf $(OUTPUT_DIR)/analysis-*
	rm -f $(OUTPUT_DIR)/tasks_cleaned.csv
	rm -f $(OUTPUT_DIR)/final_dashboard.png
	rm -f $(OUTPUT_DIR)/BSN_PROGRAM_WORKLOAD_ANALYSIS.md
	rm -f $(OUTPUT_DIR)/BSN_program_analysis.png
	rm -f $(OUTPUT_DIR)/COMPREHENSIVE_ANALYSIS.md
	rm -f $(OUTPUT_DIR)/comprehensive_analysis_summary.png
	rm -f $(OUTPUT_DIR)/EVIDENCE_BASED_ANALYSIS.md
	rm -f $(OUTPUT_DIR)/evidence_based_analysis.png
	rm -f data/tasks_cleaned.csv
	@echo "✅ Outputs cleaned"

# Deep clean - removes everything including virtual environments
.PHONY: deep-clean
deep-clean: clean
	@echo "=== Deep cleaning (including virtual environments) ==="
	rm -rf $(VENV) venv_reproduce
	@echo "✅ Deep clean complete"

# Run baseline analysis
.PHONY: baseline
baseline: venv verify-env
	@echo "\n=== Running Baseline Analysis ==="
	$(VENV_PYTHON) scripts/clean_data.py
	git checkout analysis-baseline
	$(VENV_PYTHON) scripts/baseline_report.py
	$(VENV_PYTHON) scripts/git_auto_commit.py analysis-baseline "baseline run $$(date '+%Y-%m-%d %H:%M')"

# Run archetype analysis
.PHONY: archetypes
archetypes: venv verify-env
	@echo "\n=== Running Archetype Analysis ==="
	$(VENV_PYTHON) scripts/clean_data.py
	git checkout analysis-archetypes
	mkdir -p $(OUTPUT_DIR)/analysis-archetypes
	cp $(OUTPUT_DIR)/analysis-baseline/weekly_rollup.csv $(OUTPUT_DIR)/analysis-archetypes/ 2>/dev/null || true
	$(VENV_PYTHON) scripts/archetype_report.py
	$(VENV_PYTHON) scripts/git_auto_commit.py analysis-archetypes "archetype run $$(date '+%Y-%m-%d %H:%M')"

# Run simulation analysis
.PHONY: simulation
simulation: venv verify-env
	@echo "\n=== Running Simulation Analysis ==="
	$(VENV_PYTHON) scripts/clean_data.py
	git checkout analysis-simulation
	mkdir -p $(OUTPUT_DIR)/analysis-simulation
	cp $(OUTPUT_DIR)/analysis-baseline/weekly_rollup.csv $(OUTPUT_DIR)/analysis-simulation/ 2>/dev/null || true
	$(VENV_PYTHON) scripts/simulation_report.py
	$(VENV_PYTHON) scripts/git_auto_commit.py analysis-simulation "simulation run $$(date '+%Y-%m-%d %H:%M')"

# Run final dashboard
.PHONY: dashboard
dashboard: venv verify-env
	@echo "\n=== Creating Final Dashboard ==="
	$(VENV_PYTHON) scripts/final_dashboard.py
	@echo "✅ Dashboard created at $(OUTPUT_DIR)/final_dashboard.png"

# Run evidence-based analysis
.PHONY: evidence
evidence: venv verify-env
	@echo "\n=== Generating Evidence-Based Analysis ==="
	$(VENV_PYTHON) scripts/evidence_based_report.py
	@echo "✅ Analysis created at $(OUTPUT_DIR)/BSN_PROGRAM_WORKLOAD_ANALYSIS.md"

# Run all reports and visualizations
.PHONY: all-reports
all-reports: dashboard evidence integrity-report
	@echo "✅ All reports and visualizations complete!"

# Full pipeline with all analyses and reports
.PHONY: full
full: clean all all-reports lock-env
	@echo "✅ Full pipeline complete with all analyses and reports!"
	@echo "📊 Environment locked for reproducibility"

# Check what files exist
.PHONY: check
check:
	@echo "=== Checking output files ==="
	@echo "Analysis outputs:"
	@ls -la $(OUTPUT_DIR)/analysis-*/ 2>/dev/null || echo "  No analysis directories found"
	@echo "\nReports and visualizations:"
	@ls -la $(OUTPUT_DIR)/*.md $(OUTPUT_DIR)/*.png $(OUTPUT_DIR)/*.csv 2>/dev/null || echo "  No reports found"
	@echo "\nIntegrity files:"
	@ls -la requirements_lock.txt verify_environment.py 2>/dev/null || echo "  No integrity files found"
	@echo "\nGit status:"
	@git status --short

# Help target
.PHONY: help
help:
	@echo "Graduate Research Workload Analysis - Make Targets"
	@echo "================================================"
	@echo ""
	@echo "ANALYSIS TARGETS:"
	@echo "  make all         - Run all three analyses (baseline, archetypes, simulation)"
	@echo "  make baseline    - Run baseline analysis only"
	@echo "  make archetypes  - Run archetype analysis only"
	@echo "  make simulation  - Run simulation analysis only"
	@echo ""
	@echo "REPORT TARGETS:"
	@echo "  make dashboard   - Create final dashboard visualization"
	@echo "  make evidence    - Generate evidence-based BSN analysis"
	@echo "  make all-reports - Generate all reports and visualizations"
	@echo ""
	@echo "INTEGRITY TARGETS:"
	@echo "  make lock-env    - Lock current environment versions"
	@echo "  make verify-env  - Verify environment matches requirements"
	@echo "  make reproduce-env - Create exact reproduction environment"
	@echo "  make integrity-report - Generate research integrity documentation"
	@echo ""
	@echo "UTILITY TARGETS:"
	@echo "  make full        - Clean, then run everything"
	@echo "  make clean       - Remove all generated outputs"
	@echo "  make deep-clean  - Remove all outputs and environments"
	@echo "  make check       - Check what output files exist"
	@echo "  make help        - Show this help message"
