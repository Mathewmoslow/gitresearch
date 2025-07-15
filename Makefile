# Makefile for Graduate Research Workload Analysis
# Multi-branch pipeline with external outputs

# Define output directory
OUTPUT_DIR := ~/Documents/gitresearch_outputs

# Default target
.PHONY: all
all: baseline archetypes simulation
	@echo "✅ All analyses complete!"

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
	rm -f data/tasks_cleaned.csv  # Also clean from data directory if exists
	@echo "✅ Outputs cleaned"

# Deep clean - removes everything including git-tracked generated files
.PHONY: deep-clean
deep-clean: clean
	@echo "=== Deep cleaning (including git-tracked files) ==="
	git clean -fdx outputs/ 2>/dev/null || true
	git clean -fdx data/tasks_cleaned.csv 2>/dev/null || true
	rm -rf outputs/ 2>/dev/null || true
	@echo "✅ Deep clean complete"

# Run baseline analysis
.PHONY: baseline
baseline:
	@echo "\n=== Running Baseline Analysis ==="
	python3 scripts/clean_data.py
	git checkout analysis-baseline
	python3 scripts/baseline_report.py
	python3 scripts/git_auto_commit.py analysis-baseline "baseline run $$(date '+%Y-%m-%d %H:%M')"

# Run archetype analysis
.PHONY: archetypes
archetypes:
	@echo "\n=== Running Archetype Analysis ==="
	python3 scripts/clean_data.py
	git checkout analysis-archetypes
	# Ensure output directory exists
	mkdir -p $(OUTPUT_DIR)/analysis-archetypes
	# Copy baseline results if they exist
	cp $(OUTPUT_DIR)/analysis-baseline/weekly_rollup.csv $(OUTPUT_DIR)/analysis-archetypes/ 2>/dev/null || true
	python3 scripts/archetype_report.py
	python3 scripts/git_auto_commit.py analysis-archetypes "archetype run $$(date '+%Y-%m-%d %H:%M')"

# Run simulation analysis
.PHONY: simulation
simulation:
	@echo "\n=== Running Simulation Analysis ==="
	python3 scripts/clean_data.py
	git checkout analysis-simulation
	# Ensure output directory exists
	mkdir -p $(OUTPUT_DIR)/analysis-simulation
	# Try to copy from baseline
	cp $(OUTPUT_DIR)/analysis-baseline/weekly_rollup.csv $(OUTPUT_DIR)/analysis-simulation/ 2>/dev/null || true
	python3 scripts/simulation_report.py
	python3 scripts/git_auto_commit.py analysis-simulation "simulation run $$(date '+%Y-%m-%d %H:%M')"

# Run final dashboard
.PHONY: dashboard
dashboard:
	@echo "\n=== Creating Final Dashboard ==="
	python3 scripts/final_dashboard.py
	@echo "✅ Dashboard created at $(OUTPUT_DIR)/final_dashboard.png"

# Run comprehensive report
.PHONY: report
report:
	@echo "\n=== Generating Comprehensive Report ==="
	python3 scripts/comprehensive_report.py
	@echo "✅ Report created at $(OUTPUT_DIR)/COMPREHENSIVE_ANALYSIS.md"

# Run evidence-based analysis
.PHONY: evidence
evidence:
	@echo "\n=== Generating Evidence-Based Analysis ==="
	python3 scripts/evidence_based_report.py
	@echo "✅ Analysis created at $(OUTPUT_DIR)/BSN_PROGRAM_WORKLOAD_ANALYSIS.md"

# Run all reports and visualizations
.PHONY: all-reports
all-reports: dashboard report evidence
	@echo "✅ All reports and visualizations complete!"

# Full pipeline with all analyses and reports
.PHONY: full
full: clean all all-reports
	@echo "✅ Full pipeline complete with all analyses and reports!"

# Check what files exist
.PHONY: check
check:
	@echo "=== Checking output files ==="
	@echo "Analysis outputs:"
	@ls -la $(OUTPUT_DIR)/analysis-*/ 2>/dev/null || echo "  No analysis directories found"
	@echo "\nReports and visualizations:"
	@ls -la $(OUTPUT_DIR)/*.md $(OUTPUT_DIR)/*.png $(OUTPUT_DIR)/*.csv 2>/dev/null || echo "  No reports found"
	@echo "\nGit status:"
	@git status --short

# Help target
.PHONY: help
help:
	@echo "Graduate Research Workload Analysis - Make Targets"
	@echo "================================================"
	@echo "  make all         - Run all three analyses (baseline, archetypes, simulation)"
	@echo "  make baseline    - Run baseline analysis only"
	@echo "  make archetypes  - Run archetype analysis only"
	@echo "  make simulation  - Run simulation analysis only"
	@echo "  make dashboard   - Create final dashboard visualization"
	@echo "  make report      - Generate comprehensive analysis report"
	@echo "  make evidence    - Generate evidence-based BSN analysis"
	@echo "  make all-reports - Generate all reports and visualizations"
	@echo "  make full        - Clean, then run everything (analyses + reports)"
	@echo "  make clean       - Remove all generated outputs"
	@echo "  make deep-clean  - Remove all outputs including git-tracked files"
	@echo "  make check       - Check what output files exist"
	@echo "  make help        - Show this help message"
