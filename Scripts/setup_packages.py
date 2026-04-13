#!/usr/bin/python3

import json
import shutil
import subprocess
import sys

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


def detect_package_manager():
    if shutil.which("yay"):
        return "yay", ["yay", "-S", "--noconfirm"]
    if shutil.which("pacman"):
        return "pacman", ["sudo", "pacman", "-S", "--noconfirm"]
    if shutil.which("apt"):
        return "apt", ["sudo", "apt", "install", "-y"]
    return None, None


def is_installed(name, pm_name):
    if pm_name in ("yay", "pacman"):
        result = subprocess.run(["pacman", "-Qi", name], capture_output=True, text=True)
        return result.returncode == 0
    if pm_name == "apt":
        result = subprocess.run(["dpkg", "-s", name], capture_output=True, text=True)
        return result.returncode == 0
    return False


def main():
    try:
        with open(SCRIPT_DIR / "packages.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        error("packages.json not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in packages.json: {e}")
        sys.exit(1)

    packages = data.get("required", [])
    if not packages:
        warn("No packages listed in packages.json")
        return

    pm_name, install_cmd = detect_package_manager()
    if not pm_name or not install_cmd:
        error("No supported package manager found (yay, pacman, apt)")
        sys.exit(1)

    info(f"Using {BOLD}{pm_name}{RESET} as package manager")
    print()

    missing = []
    for pkg in packages:
        name = pkg["name"]
        if is_installed(name, pm_name):
            success(f"{BOLD}{name}{RESET} is already installed")
        else:
            warn(f"{BOLD}{name}{RESET} is not installed")
            missing.append(pkg)

    if not missing:
        print()
        success("All packages are installed")
        return

    print()
    info(f"{len(missing)} package(s) to install:")
    for pkg in missing:
        desc = pkg.get("desc", "")
        print(f"  {CYAN}•{RESET} {BOLD}{pkg['name']}{RESET}  {desc}")

    print()
    answer = input(f"  {YELLOW}Install missing packages? [Y/n]:{RESET} ").strip()
    if answer and answer.lower() != "y":
        info("Skipped")
        return

    print()
    failed = []
    for pkg in missing:
        name = pkg["name"]
        info(f"Installing {BOLD}{name}{RESET}...")
        result = subprocess.run(install_cmd + [name])
        if result.returncode != 0:
            error(f"Failed to install {BOLD}{name}{RESET}")
            failed.append(name)
        else:
            success(f"Installed {BOLD}{name}{RESET}")

    print()
    if failed:
        warn(f"Failed to install {len(failed)} package(s):")
        for name in failed:
            print(f"  {RED}•{RESET} {BOLD}{name}{RESET}")
        print()
    else:
        success("All packages installed")


if __name__ == "__main__":
    print()
    print("┌─────────────────────────────────┐")
    print(f"│       {BOLD}Package setup {CYAN}{BOLD}v.{__VERSION__:.1f}{RESET}       │")
    print(f"│       {YELLOW}github.com/nikolisan{RESET}      │")
    print("└─────────────────────────────────┘")
    print()

    main()
