import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from services import identify_service
import threading
from colors import green, red, yellow, cyan, magenta
from banner import show_banner
import time
from banner_grabber import grab_banner
from scanner_udp import scan_udp

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


def scan_tcp(ip, port, total):
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
			open_ports.append((port, "tcp", service, banner))
			print(green(f"\n[+] {port}/tcp OPEN"), f"({service}) --> {banner}")
		print(f"\rScanning: {progress:.1f}%({scanned}/{total})", end="")

def scan_udp_wrapper(ip, port, total, no_response_ports, closed_ports, filtered_ports, results):
	global scanned
	result = scan_udp(ip, port, timeout=2)
	with lock:
		scanned +=1
		progress = (scanned / total) * 100

		if result == "closed":
			closed_ports.append(port)
		elif result == "filtered":
			filtered_ports.append(port)
		elif result == "root-required":
			print(red(f"[-] {port}/udp requires root privileges"))
		elif result == "no-response":
			no_response_ports.append(port)
		elif result == "open":
			service = identify_service(port)
			open_ports.append((port, "udp", service, "open"))
			results.append(green(f"\n[+] {port}/udp OPEN") + f"({service})")
		print(f"\rScanning: {progress:.1f}%({scanned}/{total})", end="")

def scan_range(target, ports, udp=False):
	ip = socket.gethostbyname(target)
	print(yellow(f"Resolved IP: {ip}"))
	total = len(ports)

	results = []
	no_response_ports = []
	closed_ports = []
	filtered_ports = []

	with ThreadPoolExecutor(max_workers=100) as executor:
		for port in ports:
			if udp:
				executor.submit(scan_udp_wrapper, ip, port, total, no_response_ports, closed_ports, filtered_ports, results)
			else:
				executor.submit(scan_tcp, ip, port, total)
	for r in results:
		print(r)

	if closed_ports:
		print(f"[*] {closed_ports[0]}-{closed_ports[-1]}/udp CLOSED")
	if filtered_ports:
		print(f"[*] {filtered_ports[0]}-{filtered_ports[-1]}/udp FILTERED")
	if no_response_ports:
		print(f"[*] {no_response_ports[0]}-{no_response_ports[-1]}/udp NO RESPONSE (open|filtered)")

	return ip, closed_ports, filtered_ports, no_response_ports

def print_summary(target, ip, total_ports, duration, closed_ports, filtered_ports, no_response_ports):
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
	for port, proto, service, banner in sorted(open_ports):
		print(green(f"  {port}/{proto}  -->  {service} --> {banner}"))

	if closed_ports:
		print(red(f"\nClosed Ports: {len(closed_ports)}"))
	if filtered_ports:
		print(yellow(f"\nFiltered Ports: {len(filtered_ports)}"))
	if no_response_ports:
		print(cyan(f"\nNo Response Ports: {len(no_response_ports)}"))

show_banner()
parser = argparse.ArgumentParser(description="DragonMap Port Scanner")
parser.add_argument("-sU", "--udp", action="store_true", help="Perform UDP Scan")
parser.add_argument("target", help="Target host")
parser.add_argument("-p", "--ports", default="1-1000", help="Port range")
args = parser.parse_args()

target = args.target
ports = parse_ports(args.ports)
print(cyan(f"Searching: {target}"))
start_time = time.time()

ip, closed_ports, filtered_ports, no_response_ports = scan_range(target, ports, udp=args.udp)
end_time = time.time()
duration = end_time - start_time
print_summary(target, ip, len(ports), duration, closed_ports, filtered_ports, no_response_ports)
