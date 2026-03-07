class Colors:
	RED = "\033[91m"
	GREEN = "\033[92m"
	YELLOW = "\033[93m"
	CYAN = "\033[96m"
	MAGENTA = "\033[95m"
	RESET = "\033[0m"

def green(text):
	return f"{Colors.GREEN}{text}{Colors.RESET}"

def red(text):
	return f"{Colors.RED}{text}{Colors.RESET}"

def cyan(text):
	return f"{Colors.CYAN}{text}{Colors.RESET}"

def yellow(text):
	return f"{Colors.YELLOW}{text}{Colors.RESET}"

def magenta(text):
	return f"{Colors.MAGENTA}{text}{Colors.RESET}"
