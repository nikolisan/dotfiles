#!/usr/bin/python3

import subprocess
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent

try:
    with open(REPO_DIR / "version", "r") as f:
        __VERSION__ = float(f.read().strip())
except Exception:
    __VERSION__ = 1.0


RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
RESET = "\033[0m"


def info(msg):
    print(f"{CYAN}[INFO]{RESET}  {msg}")


def success(msg):
    print(f"{GREEN}[OK]{RESET}    {msg}")


def warn(msg):
    print(f"{YELLOW}[WARN]{RESET}  {msg}")


def error(msg):
    print(f"{RED}[ERROR]{RESET} {msg}")


def parse_services(md_path: Path) -> list[tuple[str, list[str]]]:
    """Parse the markdown table and return a list of (name, command_args) tuples."""
    services = []
    in_table = False

    for line in md_path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            in_table = False
            continue

        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 2:
            continue

        # Skip header and separator rows
        if cols[0].lower() == "service" or re.match(r"^[-:]+$", cols[0]):
            in_table = True
            continue

        if in_table and cols[0] and cols[1]:
            name = cols[0]
            cmd = cols[1].split()
            services.append((name, cmd))

    return services


SERVICES_MD = Path(__file__).parent / "systemd_services.md"

if not SERVICES_MD.exists():
    error(f"Services file not found: {SERVICES_MD}")
    exit(1)

services = parse_services(SERVICES_MD)


print()
print("┌─────────────────────────────────┐")
print(f"│  {BOLD}Systemd services setup {CYAN}{BOLD}v.{__VERSION__:.1f}{RESET}   │")
print(f"│      {YELLOW}github.com/nikolisan{RESET}       │")
print("└─────────────────────────────────┘")
print()

if not services:
    warn(f"No services found in {SERVICES_MD}")
    exit(0)

info(f"Found {len(services)} service(s) to enable")
print()

failed = []

for name, cmd in services:
    print(f"{CYAN}[INFO]{RESET}  Enabling {BOLD}{name}{RESET}...", end="\r", flush=True)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{RED}[ERROR]{RESET} Enabling {BOLD}{name}{RESET}...")
        err_msg = (result.stderr or result.stdout).strip()
        if err_msg:
            for line in err_msg.splitlines():
                print(f"         {line}")
        failed.append(name)
    else:
        print(f"{GREEN}[OK]{RESET}    Enabling {BOLD}{name}{RESET}...")

print()
if failed:
    warn(f"Failed to enable {len(failed)} service(s):")
    for name in failed:
        print(f"  {RED}•{RESET} {BOLD}{name}{RESET}")
    print()

success("Done")
