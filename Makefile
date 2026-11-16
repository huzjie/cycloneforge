.PHONY: install doctor train forecast eval test clean

install:
	pip install -e ".[serve]"

doctor:
	python -m cycloneforge.cli.main doctor

train:
	python -m cycloneforge.cli.main train --config config.example.yaml

forecast:
	python -m cycloneforge.cli.main forecast --config config.example.yaml --out forecast.json

eval:
	python -m cycloneforge.cli.main eval --config config.example.yaml

test:
	pytest -q

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
