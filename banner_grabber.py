import socket

def grab_banner(ip, port):

	try:

		s = socket.socket()
		s.settimeout(2)

		s.connect((ip, port))

		try:
			s.send(b"HEAD / HTTP/1.0\r\n\r\n")
		except:
			pass

		banner = s.recv(1024).decode(errors="ignore").strip()
		s.close()

		if banner:
			banner = banner.split("\n")[0]
			return banner

	except:
		pass

	return "Unknown"
