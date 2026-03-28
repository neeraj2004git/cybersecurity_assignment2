"""
ping_scanner.py - Scan hosts using ping and measure response time
Supports Windows, Linux, and macOS
"""

import subprocess
import platform
import socket
import ipaddress
import re
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_ping_command(host: str) -> list:
    """Build the correct ping command for the current OS."""
    system = platform.system().lower()
    if system == "windows":
        # -n 1 = 1 packet, -w 1000 = 1000ms timeout
        return ["ping", "-n", "1", "-w", "1000", host]
    else:
        # Linux / macOS: -c 1 = 1 packet, -W 1 = 1s timeout
        return ["ping", "-c", "1", "-W", "1", host]


def parse_rtt(output: str) -> str:
    """Extract round-trip time from ping output."""
    # Windows: "Average = 1ms"
    match = re.search(r"Average\s*=\s*([\d.]+\s*ms)", output, re.IGNORECASE)
    if match:
        return match.group(1)
    # Linux/macOS: "time=1.23 ms"
    match = re.search(r"time[=<]([\d.]+)\s*ms", output)
    if match:
        return f"{match.group(1)} ms"
    return "N/A"


def ping_host(host: str) -> dict:
    """Ping a single host and return status and RTT."""
    result = {"host": host, "status": "Down", "rtt": "N/A", "hostname": ""}

    # Try reverse DNS
    try:
        result["hostname"] = socket.gethostbyaddr(host)[0]
    except Exception:
        result["hostname"] = ""

    cmd = get_ping_command(host)
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3,
        )
        if proc.returncode == 0:
            result["status"] = "Up"
            result["rtt"] = parse_rtt(proc.stdout.decode(errors="replace"))
    except subprocess.TimeoutExpired:
        result["status"] = "Timeout"
    except Exception as e:
        result["status"] = f"Error: {e}"

    return result


def scan_range(network_range: str, max_workers: int = 50) -> list:
    """Scan all hosts in a CIDR network range concurrently."""
    try:
        net = ipaddress.ip_network(network_range, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network range: {e}")
        return []

    hosts = [str(ip) for ip in net.hosts()]
    if not hosts:
        print("[!] No hosts in range.")
        return []

    print(f"\n[*] Scanning {len(hosts)} host(s) in {network_range} ...\n")
    results = []

    with ThreadPoolExecutor(max_workers=min(max_workers, len(hosts))) as executor:
        futures = {executor.submit(ping_host, h): h for h in hosts}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            status_symbol = "✔" if res["status"] == "Up" else "✘"
            hostname_str = f"  ({res['hostname']})" if res["hostname"] else ""
            print(
                f"  [{status_symbol}] {res['host']:<18} {res['status']:<10} RTT: {res['rtt']}{hostname_str}"
            )

    return results


def print_summary(results: list):
    up = [r for r in results if r["status"] == "Up"]
    print(f"\n{'─'*50}")
    print(f"  Summary: {len(up)}/{len(results)} host(s) reachable")
    print(f"{'─'*50}")
    if up:
        print("\n  Reachable hosts:")
        for r in up:
            hn = f"  ({r['hostname']})" if r["hostname"] else ""
            print(f"    {r['host']:<18} RTT: {r['rtt']}{hn}")


def main():
    print("=" * 50)
    print("       Ping Scanner")
    print("=" * 50)
    print("  Enter a single IP, hostname, or CIDR range.")
    print("  Examples:  127.0.0.1  |  192.168.1.0/24  |  google.com")
    print("=" * 50)

    target = input("\nTarget: ").strip()
    if not target:
        print("[!] No target provided. Exiting.")
        sys.exit(1)

    start = time.time()

    # Decide: single host or range
    if "/" in target:
        results = scan_range(target)
    else:
        print(f"\n[*] Pinging {target} ...\n")
        res = ping_host(target)
        results = [res]
        status_symbol = "✔" if res["status"] == "Up" else "✘"
        hn = f"  ({res['hostname']})" if res["hostname"] else ""
        print(f"  [{status_symbol}] {res['host']:<18} {res['status']:<10} RTT: {res['rtt']}{hn}")

    print_summary(results)
    print(f"\n  Scan completed in {time.time() - start:.2f}s\n")


if __name__ == "__main__":
    main()
