PY = python3

# Paths
CLEAN   = scripts/clean_data.py
BASE    = scripts/baseline_report.py
ARCH    = scripts/archetype_report.py
SIM     = scripts/simulation_report.py
AUTO    = scripts/git_auto_commit.py

DATETIME = $(shell date "+%Y-%m-%d %H:%M")

# Targets ----------------------------------------------------------

all: baseline archetypes simulation

clean:
	$(PY) $(CLEAN)

baseline: clean
	@git checkout analysis-baseline
	$(PY) $(BASE)
	$(PY) $(AUTO) analysis-baseline "baseline run $(DATETIME)"

archetypes: clean
	@git checkout analysis-archetypes
	cp ~/Documents/gitresearch_outputs/analysis-baseline/weekly_rollup.csv ~/Documents/gitresearch_outputs/analysis-archetypes/ || true
	$(PY) $(ARCH)
	$(PY) $(AUTO) analysis-archetypes "archetype run $(DATETIME)"

simulation: clean
	@git checkout analysis-simulation
	cp ~/Documents/gitresearch_outputs/analysis-baseline/weekly_rollup.csv ~/Documents/gitresearch_outputs/analysis-simulation/ || true
	$(PY) $(SIM)
	$(PY) $(AUTO) analysis-simulation "simulation run $(DATETIME)"

.PHONY: all clean baseline archetypes simulation
