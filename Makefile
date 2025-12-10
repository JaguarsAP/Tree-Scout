# Makefile for Tree-Scout project

.PHONY: install test run clean

# Install all dependencies
install:
	pip install --upgrade pip
	pip install notebook ipywidgets yfinance requests pandas numpy matplotlib seaborn plotly scikit-learn python-dotenv pytest

# Run tests
test:
	pytest tests/ -v

# Run the notebook (requires jupyter)
run:
	jupyter notebook tree-cover-prediction.ipynb

# Clean generated files
clean:
	rm -f county_forest_loss_data.csv
	rm -f county_forest_data_enhanced.csv
	rm -f county_forest_data_train.csv
	rm -f county_forest_data_test.csv

# Setup environment file
setup-env:
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example - please add your GFW_API_KEY"; fi
