import socket
import struct
from probes import get_probe

def scan_udp(ip, port, timeout=2):
	try:
		udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udp_sock.settimeout(timeout)

		icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
		icmp_sock.settimeout(timeout)

		payload = get_probe(port)
		if payload is None:
			payload = b"DragonMap"

		udp_sock.sendto(payload, (ip, port))

		try:
			data, addr = udp_sock.recvfrom(1024)
			if data:
				return "open"
		except socket.timeout:
			pass

		try:
			data, addr = icmp_sock.recvfrom(1024)
			icmp_header = data[20:28]
			icmp_type, icmp_code, _, _, _ =struct.unpack("!BBHHH", icmp_header)

			if icmp_type == 3 and icmp_code == 3:
				return "closed"

			if icmp_type == 3:
				return "filtered"

		except socket.timeout:
			return "no-response"

		finally:
			udp_sock.close()
			icmp_sock.close()

	except PermissionError:
		return "root-required"
	except Exception as e:
		return f"error:{type(e).__name__}"
