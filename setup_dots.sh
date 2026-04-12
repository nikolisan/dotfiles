#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info() { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn() { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error() { echo -e "${RED}[ERROR]${RESET} $*"; }

echo
echo "┌───────────────────────────────┐"
echo -e "│    ${BOLD}Hyprland dot setup ${CYAN}${BOLD}v.1.0${RESET}   │"
echo -e "│      ${YELLOW}github.com/nikolisan${RESET}     │"
echo "└───────────────────────────────┘"
echo

if [[ "$(basename "$PWD")" != "dots" ]]; then
  error "Must be run from the 'dots' directory (current: $PWD)"
  exit 1
fi

dirs=(*/)

if [[ ! -d "${dirs[0]}" ]]; then
  warn "No directories found in $(pwd)"
  exit 0
fi

info "Found ${#dirs[@]} package(s) to stow"
echo

resolve_conflicts() {
  local output="$1"
  local target_dir
  target_dir="$(cd .. && pwd)"

  while IFS= read -r line; do
    if [[ "$line" =~ over\ existing\ target\ (.+)\ since ]] ||
       [[ "$line" =~ existing\ target\ is.*:\ (.+)$ ]]; then
      local conflict="${BASH_REMATCH[1]}"
      local target="${target_dir}/$(dirname "$conflict")"
      warn "  Conflict: ${BOLD}${target}${RESET}"
      echo -en "  ${YELLOW}Remove it? [Y/n]:${RESET} "
      read -r answer </dev/tty
      if [[ "${answer:-Y}" =~ ^[Yy]$ ]]; then
        rm -rf "$target"
      else
        return 1
      fi
    fi
  done <<<"$output"
  return 0
}

failed=()

for dir in "${dirs[@]}"; do
  name="${dir%/}"
  echo -en "${CYAN}[INFO]${RESET}  Linking ${BOLD}${name}${RESET}..."

  sim_output=$(stow --simulate "$name" 2>&1)
  if echo "$sim_output" | grep -q "would cause conflicts"; then
    echo -e "\r${YELLOW}[WARN]${RESET}  Linking ${BOLD}${name}${RESET}..."
    if ! resolve_conflicts "$sim_output"; then
      failed+=("$name")
      continue
    fi
  fi

  if ! stow_output=$(stow "$name" 2>&1); then
    echo -e "\r${RED}[ERROR]${RESET} Linking ${BOLD}${name}${RESET}..."
    failed+=("$name")
  else
    echo -e "\r${GREEN}[OK]${RESET}    Linking ${BOLD}${name}${RESET}..."
  fi
done

echo
if [[ ${#failed[@]} -gt 0 ]]; then
  warn "Failed to stow ${#failed[@]} package(s):"
  for name in "${failed[@]}"; do
    echo -e "  ${RED}•${RESET} ${BOLD}${name}${RESET}"
  done
  echo
fi
success "Done"
