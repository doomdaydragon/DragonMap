import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from services import identify_service
import threading
from colors import green, red, yellow, cyan, magenta
from banner import show_banner
import time
from banner_grabber import grab_banner

scanned = 0
lock = threading.Lock()
open_ports = []

def parse_ports(port_argument):
	if port_argument == "all":
		return list(range(1,65536))

	if "-" in port_argument:
		start, end = port_argument.split("-")
		return list(range(int(start), int(end) + 1))

	if "," in port_argument:
		return [int(p) for p in port_argument.split(",")]
	return [int(port_argument)]


def scan_port(ip, port, total):

	global scanned

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)

	open_port = False

	try:
		s.connect((ip, port))
		open_port = True
	except:
		pass
	finally:
		s.close()

	with lock:
		scanned += 1
		progress = (scanned / total) * 100

		if open_port:
			service = identify_service(port)
			banner = grab_banner(ip, port)
			open_ports.append((port, service))
			print(green(f"\n[+] {port}/tcp OPEN"), f"({service}) --> {banner}")

		print(f"\rScanning: {progress:.1f}%({scanned}/{total})", end="")

def scan_range(target, ports):
	ip = socket.gethostbyname(target)
	print(yellow(f"Resolved IP: {ip}"))

	total = len(ports)

	with ThreadPoolExecutor(max_workers=100) as executor:
		for port in ports:
			executor.submit(scan_port, ip, port, total)
	return ip

def print_summary(target, ip, total_ports, duration):
	print("\n")
	print("======== Scan Summary ========")

	print(cyan("Target:" + yellow(target)))
	print(cyan("IP Address:" + yellow(ip)))
	print(cyan("Ports Scanned:" + yellow(str(total_ports))))
	print(cyan("Open Ports:" + yellow(str(len(open_ports)))))
	print(green(f"Scan Duration: {duration:.2f} seconds"))

	print(yellow("\nOpen Port List:"))

	if len(open_ports) == 0:
		print(red(" No open ports found."))
	for port, service in sorted(open_ports):
		banner = grab_banner(ip, port)
		print(green(f"  {port}/tcp  -->  {service} --> {banner}"))

show_banner()

parser = argparse.ArgumentParser(description="DragonMap Port Scanner")
parser.add_argument("target", help="Target host")
parser.add_argument("-p", "--ports", default="1-1000", help="Port range")

args = parser.parse_args()

target = args.target
ports = parse_ports(args.ports)

print(cyan(f"Searching: {target}"))
start_time = time.time()
ip = scan_range(target, ports)

end_time = time.time()
duration = end_time - start_time

print_summary(target, ip, len(ports), duration)
