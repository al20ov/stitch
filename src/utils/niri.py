import json
import os
import socket


class Niri:
    def __init__(self):
        self.socket_path = os.getenv("NIRI_SOCKET")
        if not self.socket_path:
            raise ValueError("NIRI_SOCKET environment variable not set")

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)
        self.outputs = self._get_outputs()
        self.sock.close()

    def _get_outputs(self):
        self.sock.sendall(b'"Outputs"')
        self.sock.shutdown(socket.SHUT_WR)
        chunks = []
        while True:
            data = self.sock.recv(4096)
            if not data:
                break
            chunks.append(data)

        response = b"".join(chunks).decode("utf-8")
        return json.loads(response)


if __name__ == "__main__":
    try:
        niri = Niri()

        outputs_dict = niri.outputs.get("Ok", {}).get("Outputs", {})

        for output_name, output_data in outputs_dict.items():
            vrr_supported = output_data.get("vrr_supported", "N/A")

            print(f"{output_name}: VRR supported: {vrr_supported}")

    except (ValueError, FileNotFoundError, ConnectionRefusedError) as e:
        print(f"Error communicating with Niri socket: {e}")
