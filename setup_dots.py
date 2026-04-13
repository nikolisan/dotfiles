#!/usr/bin/python3

try:
    with open("version", "r") as f:
        __VERSION__ = float(f.read().strip())
except Exception:
    __VERSION__ = 1.0


import subprocess
import os
import re
import shutil
from pathlib import Path

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


def resolve_conflicts(output: str) -> bool:

    target_dir = cwd.resolve().parent
    pattern = re.compile(
        r"over existing target (.+?) since|existing target is.*?: (.+)$"
    )

    for line in output.splitlines():
        m = pattern.search(line)
        if m:
            conflict = m.group(1) or m.group(2)
            target = target_dir / Path(conflict).parent
            warn(f"  Conflict: {BOLD}{target}{RESET}")
            answer = input(f"  {YELLOW}Remove it? [Y/n]:{RESET} ").strip()
            if answer == "" or answer.lower() == "y":
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target)
                else:
                    target.unlink(missing_ok=True)
            else:
                return False

    return True


cwd = Path(".")
if cwd.resolve().name != "dots":
    error(f"Must be run from the 'dots' directory (current: {cwd.resolve()})")
    exit(1)

dirs = {(path := Path(d.path)).name: path for d in os.scandir(cwd) if d.is_dir()}

print()
print("┌───────────────────────────────┐")
print(f"│    {BOLD}Hyprland dot setup {CYAN}{BOLD}v.{__VERSION__:.1f}{RESET}   │")
print(f"│      {YELLOW}github.com/nikolisan{RESET}     │")
print("└───────────────────────────────┘")
print()

if not dirs:
    warn(f"No directories found in {cwd.resolve()}")
    exit(0)

info(f"Found {len(dirs)} package(s) to stow")
print()


failed = []

not_config_dirs = {}

for name in dirs.keys() - not_config_dirs:
    print(f"{CYAN}[INFO]{RESET}  Linking {BOLD}{name}{RESET}...", end="\r", flush=True)

    sim = subprocess.run(["stow", "--simulate", name], capture_output=True, text=True)
    sim_output = sim.stdout + sim.stderr

    if "would cause conflicts" in sim_output:
        print(
            f"{YELLOW}[WARN]{RESET}  Linking {BOLD}{name}{RESET} would cause conflicts."
        )
        if not resolve_conflicts(sim_output):
            failed.append(name)
            continue

    result = subprocess.run(["stow", name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{RED}[ERROR]{RESET} Linking {BOLD}{name}{RESET}...")
        failed.append(name)
    else:
        print(f"{GREEN}[OK]{RESET}    Linking {BOLD}{name}{RESET}...")

print()
if failed:
    warn(f"Failed to stow {len(failed)} package(s):")
    for name in failed:
        print(f"  {RED}•{RESET} {BOLD}{name}{RESET}")
    print()

success("Done")
