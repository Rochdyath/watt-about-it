#!/usr/bin/env bash
set -e
if ! command -v gitleaks >/dev/null 2>&1; then
  echo "install gitleaks first"
  exit 1
fi
gitleaks detect --no-banner --redact
