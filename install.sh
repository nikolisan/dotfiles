#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
BOLD="\033[1m"
RESET="\033[0m"

info() { echo -e "${CYAN}[INFO]${RESET}  $1"; }
success() { echo -e "${GREEN}[OK]${RESET}    $1"; }
warn() { echo -e "${YELLOW}[WARN]${RESET}  $1"; }
error() { echo -e "${RED}[ERROR]${RESET} $1"; }

VERSION=$(cat version 2>/dev/null || echo "1.0")

echo
echo "┌────────────────────────────────┐"
echo -e "│        ${BOLD}HyprlandDM ${CYAN}${BOLD}v.${VERSION}${RESET}        │"
echo -e "│      ${YELLOW}github.com/nikolisan${RESET}      │"
echo "└────────────────────────────────┘"
echo

# ── Step 1: Install required packages ────────────────────────────────
info "Step 1: Installing required packages"

python3 Scripts/setup_packages.py

# ── Step 2: Set fish as default shell ────────────────────────────────
info "Step 2: Setting fish as default shell"

FISH_PATH=$(command -v fish 2>/dev/null || true)

if [[ -z "$FISH_PATH" ]]; then
  error "fish is not installed — cannot set as default shell"
  exit 1
fi

CURRENT_SHELL=$(getent passwd "$USER" | cut -d: -f7)

if [[ "$CURRENT_SHELL" == "$FISH_PATH" ]]; then
  success "fish is already the default shell"
else
  # Make sure fish is in /etc/shells
  if ! grep -qxF "$FISH_PATH" /etc/shells; then
    info "Adding ${BOLD}${FISH_PATH}${RESET} to /etc/shells"
    echo "$FISH_PATH" | sudo tee -a /etc/shells >/dev/null
  fi

  info "Changing default shell to ${BOLD}fish${RESET}"
  chsh -s "$FISH_PATH"
  success "Default shell set to ${BOLD}fish${RESET} (takes effect on next login)"
fi
echo

# ── Step 3: Stow dotfiles ────────────────────────────────────────────
info "Step 3: Installing dotfiles"
echo
python3 Scripts/setup_dots.py

# ── Step 4: Enable systemd services ─────────────────────────────────
info "Step 4: Enabling systemd services"
echo
python3 Scripts/setup_services.py

success "All done!"
