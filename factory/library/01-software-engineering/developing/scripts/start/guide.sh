#!/usr/bin/env bash
set -euo pipefail

ask_yes_no() {
  local prompt="$1"
  local answer=""
  local normalized=""
  while true; do
    printf '%s (yes/no): ' "$prompt"
    read -r answer
    normalized="$(printf '%s' "$answer" | tr '[:upper:]' '[:lower:]')"
    case "$normalized" in
      yes|y) return 0 ;;
      no|n) return 1 ;;
      *) printf '%s\n' "Please answer yes or no." ;;
    esac
  done
}

printf '\n'
printf '%s\n' "Sovereign Guided Next Command"
printf '%s\n' "Answer a few yes/no questions. You will get one exact next command."
printf '\n'

if ! ask_yes_no "Do you already have a feature idea?"; then
  printf '\nNext command:\n  /plan\n\n'
  exit 0
fi

if ! ask_yes_no "Did you confirm the spec (acceptance criteria + data shape)?"; then
  printf '\nNext command:\n  /plan\n\n'
  exit 0
fi

if ! ask_yes_no "Are contracts locked for the feature domain?"; then
  printf '\nNext command:\n  /contract\n\n'
  exit 0
fi

if ! ask_yes_no "Is implementation done for this feature?"; then
  if ask_yes_no "Do you want beginner-safe build mode?"; then
    printf '\nNext command:\n  /build\n'
    printf '%s\n' "Preset: build:beginner (plain-language guidance, no advanced flags)"
    printf '\n'
  else
    printf '\nNext command:\n  /build\n\n'
  fi
  exit 0
fi

if ! ask_yes_no "Did you run tests?"; then
  printf '\nNext command:\n  /test\n\n'
  exit 0
fi

if ! ask_yes_no "Did you run quality checks?"; then
  printf '\nNext command:\n  /quality all\n'
  printf '%s\n' "Preset: quality:quick -> run /quality before deeper checks"
  printf '\n'
  exit 0
fi

if ask_yes_no "Do you want to deploy now?"; then
  if ask_yes_no "Deploy to production?"; then
    printf '\nNext command:\n  /deploy prod\n'
    printf '%s\n' "Preset: deploy:dry-run -> use preview first if unsure"
    printf '\n'
  else
    printf '\nNext command:\n  /deploy\n\n'
  fi
  exit 0
fi

printf '\nNext command:\n  bash scripts/start/status-dashboard.sh\n\n'
