import json
import os
import platform
from http.server import HTTPServer, BaseHTTPRequestHandler

import psutil


def get_load_avg():
    if platform.system() != "Windows":
        load1, load5, _ = os.getloadavg()
        return load1, load5

    cpu_count = psutil.cpu_count() or 1
    cpu_percent = psutil.cpu_percent(interval=1.0)
    load = round(cpu_percent / 100.0 * cpu_count, 2)
    return load, load


class LoadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/load":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}).encode())
            return

        load1, load5 = get_load_avg()
        body = json.dumps({
            "load_1min": load1,
            "load_5min": load5,
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    server = HTTPServer((host, port), LoadHandler)
    print(f"Listening on {host}:{port}")
    server.serve_forever()
