#!/usr/bin/env bash
# 一键跑通：doctor -> train -> forecast -> eval
set -e
cd "$(dirname "$0")/.."
python -m cycloneforge.cli.main doctor
python -m cycloneforge.cli.main train --config config.example.yaml
python -m cycloneforge.cli.main forecast --config config.example.yaml --out forecast.json
python -m cycloneforge.cli.main eval --config config.example.yaml
