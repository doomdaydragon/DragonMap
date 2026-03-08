import socket

def grab_banner(ip, port):
	try:
		s = socket.socket()
		s.settimeout(2)
		s.connect((ip, port))

		#Port Based Tries
		probes = {
			80: b"HEAD / HTTP/1.0\r\n\r\n",
			21: b"HELLO\r\n",
			25: b"EHLO example.com\r\n"
		}

		if port in probes:
			try:
				s.send(probes[port])
			except Exception:
				pass

		banner = s.recv(1024).decode(errors="ignore").strip()
		s.close()

		if banner:
			banner = banner.split("\n")[0]
			return banner

	except socket.timeout:
		return "Timeout"
	except ConnectionRefusedError:
		return "Connection Refused"
	except Exception:
		return "Unknown"

	return "Unknown"
