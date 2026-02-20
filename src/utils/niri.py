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

    def save_config(self):
        pass

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
        data = json.loads(response)
        return data.get("Ok", {}).get("Outputs", {})

    def get_output_details(self, output_name):
        output_data = self.outputs.get(output_name)
        if not output_data:
            return None

        current_mode_index = output_data.get("current_mode")
        modes = output_data.get("modes", [])

        resolution = None
        if (
            current_mode_index is not None
            and modes
            and 0 <= current_mode_index < len(modes)
        ):
            current_mode = modes[current_mode_index]
            resolution = {
                "width": current_mode.get("width"),
                "height": current_mode.get("height"),
            }

        logical_info = output_data.get("logical", {})

        return {
            "resolution": resolution,
            "logical_position": {
                "x": logical_info.get("x"),
                "y": logical_info.get("y"),
            },
            "logical_size": {
                "width": logical_info.get("width"),
                "height": logical_info.get("height"),
            },
            "scale": logical_info.get("scale"),
            "transform": logical_info.get("transform"),
        }
