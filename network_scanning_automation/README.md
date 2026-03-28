# Cybersecurity Assignment 2 - Network Scanner

This folder contains three Python scripts I wrote for the network scanning assignment. Each one handles a different type of scan - ping, ARP, and nmap. All three work on Windows, Linux, and macOS.

---

## What's inside

ping_scanner.py - pings a host or a range of IPs and shows whether they're up or down along with the response time.

arp_scanner.py - reads the ARP table from your system and displays the IP to MAC address mappings.

nmap_scanner.py - a menu-driven nmap wrapper that supports host discovery, port scanning, service detection, and OS detection.

------

## Requirements

- Python 3.6 or above
- Nmap installed on your system (only needed for nmap_scanner.py)
- ping and arp are built into the OS so no install needed for those

To install nmap on Kali/Ubuntu:
```
sudo apt install nmap
```

---------

## How to run

Make sure you're in the network_scanner directory first, then:

```
python3 ping_scanner.py
python3 arp_scanner.py
python3 nmap_scanner.py
```

For OS detection with nmap you'll need to run it with sudo:
```
sudo python3 nmap_scanner.py
```

I tested all three on localhost (127.0.0.1) before running them on any network.

------------

## Notes

- Don't scan networks you don't own or have permission to scan
- The scripts accept user input at runtime, nothing is hardcoded
- Screenshots of the output are in the screenshots folder

------------

## Tools used

Python 3, Nmap, standard library only (no pip installs needed)
