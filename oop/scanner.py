from abc import ABC, abstractmethod
import socket


class BaseScanner(ABC):
    """Abstract class scanner."""

    @abstractmethod
    def scan(self):
        pass


class TCPPortScanner(BaseScanner):
    """Scanner port TCP."""

    def __init__(self, host, start_port, end_port, timeout=0.5):
        self._host = host
        self._start_port = start_port
        self._end_port = end_port
        self._timeout = timeout

    def _resolve_host(self):
        """Mengubah hostname menjadi IP."""
        return socket.gethostbyname(self._host)

    def scan(self):
        """Implementasi scan TCP."""
        target_ip = self._resolve_host()
        open_ports = []

        print("-" * 50)
        print(f"Target IP   : {target_ip}")
        print(f"Port Range  : {self._start_port}-{self._end_port}")
        print("-" * 50)

        for port in range(self._start_port, self._end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._timeout)

            result = sock.connect_ex((target_ip, port))
            sock.close()

            if result == 0:
                print(f"[+] Port {port} TERBUKA")
                open_ports.append(port)

        return {
            "host": self._host,
            "ip": target_ip,
            "start_port": self._start_port,
            "end_port": self._end_port,
            "open_ports": open_ports,
        }