#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
exec .venv/bin/mkdocs serve --dev-addr 127.0.0.1:8000
