# DragonMap v1.1

**DragonMap** is a fast, multithreaded port scanner with banner grabbing capabilities.
It scans open ports, identifies running services, and generates a detailed summary report in the terminal.

---

## NEW Features

- UDP Scan

## Features

- Multithreaded port scanning
- scan specific ports, ranges or all ports
- Service identification (port -> service)
- Banner grabbing (HTTP, SSH, FTP, etc.)
- Scan Duration and detailed summary
- Color-coded terminal output
- Clean CLI banner and professional look

---

## Installation

**Requirements:**

- Python 3.x
- Linux / Termux / Windows (WSL recommended)

**Steps:**

```bash
git clone https://github.com/doomdaydragon/DragonMap.git
cd DragonMap
```

## Usage

```bash
./dragonmap.sh <target> -p <ports>
./dragonmap.sh <target> -p <ports> -sU
```

**Examples:**
```bash
./dragonmap.sh scanme.nmap.org
./dragonmap.sh scanme.nmap.org -p 22
./dragonmap.sh scanme.nmap.org -p 1-1000
./dragonmap.sh scanme.nmap.org -p 22,80,443
./dragonmap.sh scanme.nmap.org -p all
./dragonmap.sh scanme.nmap.org -p 1-1000 -sU
```

**Made By DoomDayDragon**
