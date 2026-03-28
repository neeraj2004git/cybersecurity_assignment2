"""
nmap_scanner.py - Perform network scans using Nmap
Supports: Host discovery, port scanning, service detection, OS detection
Supports Windows, Linux, and macOS
"""

import subprocess
import sys
import shutil
import re
import time


# ─────────────────────────────────────────────
#  Nmap availability check
# ─────────────────────────────────────────────

def check_nmap() -> str:
    """Return path to nmap executable or exit with an error."""
    nmap_path = shutil.which("nmap")
    if not nmap_path:
        print("[!] Nmap is not installed or not in PATH.")
        print("    Install it from: https://nmap.org/download.html")
        sys.exit(1)
    return nmap_path


# ─────────────────────────────────────────────
#  Nmap runner
# ─────────────────────────────────────────────

def run_nmap(args: list, label: str) -> str:
    """Run nmap with given arguments and return stdout."""
    nmap = check_nmap()
    cmd = [nmap] + args
    print(f"\n[*] {label}")
    print(f"    Command: {' '.join(cmd)}\n")
    print("─" * 55)
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
        output = proc.stdout.decode(errors="replace")
        stderr = proc.stderr.decode(errors="replace")

        if proc.returncode != 0 and not output.strip():
            print(f"[!] Nmap error:\n{stderr}")
            return ""

        print(output)
        return output

    except subprocess.TimeoutExpired:
        print("[!] Scan timed out (120s). Try a smaller target or add -T4.")
        return ""
    except Exception as e:
        print(f"[!] Failed to run nmap: {e}")
        return ""


# ─────────────────────────────────────────────
#  Scan modes
# ─────────────────────────────────────────────

def host_discovery(target: str):
    """Ping scan – discover live hosts without port scanning."""
    run_nmap(["-sn", target], f"Host Discovery on {target}")


def port_scan_default(target: str):
    """Scan the top 1000 TCP ports (default nmap behaviour)."""
    run_nmap(["-sV", "--open", target], f"Default Port Scan on {target}")


def port_scan_custom(target: str, ports: str):
    """Scan user-specified ports (e.g. '22,80,443' or '1-1024')."""
    run_nmap(["-sV", "-p", ports, target], f"Custom Port Scan ({ports}) on {target}")


def service_detection(target: str):
    """Probe open ports for service/version info."""
    run_nmap(["-sV", "--version-intensity", "5", target], f"Service Detection on {target}")


def os_detection(target: str):
    """Attempt OS fingerprinting (requires root/administrator)."""
    print("\n[*] OS detection requires elevated privileges (root / Administrator).")
    run_nmap(["-O", "--osscan-guess", target], f"OS Detection on {target}")


def full_scan(target: str):
    """Comprehensive scan: service + OS + script engine."""
    run_nmap(["-sV", "-O", "--osscan-guess", "-sC", target], f"Full Scan on {target}")


# ─────────────────────────────────────────────
#  Menu
# ─────────────────────────────────────────────

MENU = """
  ┌─────────────────────────────────────────────┐
  │              Nmap Scanner Menu              │
  ├─────────────────────────────────────────────┤
  │  1. Host Discovery       (ping sweep)       │
  │  2. Default Port Scan    (top 1000 ports)   │
  │  3. Custom Port Scan     (you pick ports)   │
  │  4. Service Detection                       │
  │  5. OS Detection         (needs root/admin) │
  │  6. Full Scan            (all of the above) │
  │  0. Exit                                    │
  └─────────────────────────────────────────────┘
"""

HANDLERS = {
    "1": ("Host Discovery",       host_discovery),
    "2": ("Default Port Scan",    port_scan_default),
    "3": ("Custom Port Scan",     None),          # handled separately
    "4": ("Service Detection",    service_detection),
    "5": ("OS Detection",         os_detection),
    "6": ("Full Scan",            full_scan),
}


def get_target() -> str:
    target = input("\nEnter target (IP, hostname, or CIDR range): ").strip()
    if not target:
        print("[!] No target provided.")
        sys.exit(1)
    return target


def main():
    print("=" * 55)
    print("             Nmap Scanner")
    print("=" * 55)
    print("  IMPORTANT: Only scan networks you own or have")
    print("  explicit written permission to scan.")
    print("  Unauthorized scanning is illegal.")
    print("=" * 55)

    check_nmap()  # Fail fast if nmap missing

    while True:
        print(MENU)
        choice = input("  Select option: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            break

        if choice not in HANDLERS:
            print("  [!] Invalid choice. Please try again.")
            continue

        label, handler = HANDLERS[choice]

        if choice == "3":
            target = get_target()
            ports = input("  Enter ports (e.g. 22,80,443 or 1-1024): ").strip()
            if not ports:
                print("  [!] No ports specified.")
                continue
            start = time.time()
            port_scan_custom(target, ports)
        else:
            target = get_target()
            start = time.time()
            handler(target)

        elapsed = time.time() - start
        print(f"\n{'─'*55}")
        print(f"  Scan '{label}' completed in {elapsed:.2f}s")
        print(f"{'─'*55}")

        again = input("\n  Run another scan? (y/n) [y]: ").strip().lower()
        if again == "n":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
