"""
arp_scanner.py - Retrieve ARP table and display IP-MAC mappings
Supports Windows, Linux, and macOS
"""

import subprocess
import platform
import re
import socket
import sys
import ipaddress


# ─────────────────────────────────────────────
#  ARP table parsing
# ─────────────────────────────────────────────

def get_arp_table_windows() -> list:
    """Parse `arp -a` output on Windows."""
    entries = []
    try:
        output = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL).decode(errors="replace")
    except Exception as e:
        print(f"[!] Failed to run arp -a: {e}")
        return entries

    # Typical line: "  192.168.1.1          00-50-56-c0-00-08     dynamic"
    pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3})\s+([\da-fA-F]{2}[:-][\da-fA-F]{2}[:-][\da-fA-F]{2}"
        r"[:-][\da-fA-F]{2}[:-][\da-fA-F]{2}[:-][\da-fA-F]{2})\s+(\S+)"
    )
    for match in pattern.finditer(output):
        ip, mac, entry_type = match.groups()
        entries.append({"ip": ip, "mac": mac.upper(), "type": entry_type})
    return entries


def get_arp_table_unix() -> list:
    """Parse `arp -n` output on Linux/macOS."""
    entries = []

    # Try Linux style first (arp -n)
    try:
        output = subprocess.check_output(["arp", "-n"], stderr=subprocess.DEVNULL).decode(errors="replace")
        # Linux: "192.168.1.1   ether  00:50:56:c0:00:08  C  eth0"
        pattern = re.compile(
            r"(\d{1,3}(?:\.\d{1,3}){3})\s+\S+\s+([\da-fA-F:]{17})\s+(\S+)"
        )
        for match in pattern.finditer(output):
            ip, mac, flags = match.groups()
            entries.append({"ip": ip, "mac": mac.upper(), "type": flags})
        if entries:
            return entries
    except Exception:
        pass

    # Fallback: macOS / BSD (arp -a)
    try:
        output = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL).decode(errors="replace")
        # macOS: "? (192.168.1.1) at 00:50:56:c0:00:08 on en0 ifscope [ethernet]"
        pattern = re.compile(
            r"\((\d{1,3}(?:\.\d{1,3}){3})\)\s+at\s+([\da-fA-F:]{17})\s+on\s+(\S+)"
        )
        for match in pattern.finditer(output):
            ip, mac, iface = match.groups()
            entries.append({"ip": ip, "mac": mac.upper(), "type": iface})
    except Exception as e:
        print(f"[!] Failed to run arp -a: {e}")

    return entries


def get_arp_table() -> list:
    system = platform.system().lower()
    if system == "windows":
        return get_arp_table_windows()
    else:
        return get_arp_table_unix()


# ─────────────────────────────────────────────
#  Optional: resolve hostnames
# ─────────────────────────────────────────────

def resolve_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""


# ─────────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────────

def print_table(entries: list, resolve: bool = False):
    if not entries:
        print("\n  [!] No ARP entries found.\n")
        return

    col_ip = 18
    col_mac = 20
    col_type = 12
    col_host = 30

    header = f"  {'IP Address':<{col_ip}} {'MAC Address':<{col_mac}} {'Type':<{col_type}}"
    if resolve:
        header += f" {'Hostname':<{col_host}}"
    sep = "  " + "─" * (len(header) - 2)

    print(f"\n{sep}")
    print(header)
    print(sep)

    for e in entries:
        hostname = resolve_hostname(e["ip"]) if resolve else ""
        row = f"  {e['ip']:<{col_ip}} {e['mac']:<{col_mac}} {e['type']:<{col_type}}"
        if resolve:
            row += f" {hostname:<{col_host}}"
        print(row)

    print(sep)
    print(f"\n  Total entries: {len(entries)}\n")


# ─────────────────────────────────────────────
#  Filtering
# ─────────────────────────────────────────────

def filter_entries(entries: list, filter_ip: str) -> list:
    """Filter entries by IP prefix or full IP."""
    return [e for e in entries if e["ip"].startswith(filter_ip)]


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────

def main():
    print("=" * 55)
    print("          ARP Table Scanner")
    print("=" * 55)
    print("  Options:")
    print("    1. Show full ARP table")
    print("    2. Filter by IP / subnet prefix")
    print("=" * 55)

    choice = input("\nChoice [1/2]: ").strip()

    resolve = input("Resolve hostnames? (y/n) [n]: ").strip().lower() == "y"

    entries = get_arp_table()

    if not entries:
        print("\n[!] Could not retrieve ARP table. Try running as administrator/root.")
        sys.exit(1)

    if choice == "2":
        prefix = input("Enter IP prefix to filter (e.g. 192.168.1): ").strip()
        entries = filter_entries(entries, prefix)
        if not entries:
            print(f"\n[!] No entries matching prefix '{prefix}'.")
            sys.exit(0)

    print_table(entries, resolve=resolve)


if __name__ == "__main__":
    main()
