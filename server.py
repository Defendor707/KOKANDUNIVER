#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            api_file_path = parsed_path.path[1:]
            
            if api_file_path.startswith("api/graduate") and not api_file_path.endswith(".json"):
                api_file_path = os.path.join(api_file_path, "index.json")

            if os.path.exists(api_file_path):
                with open(api_file_path, "r") as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b"{\"error\": \"Not found\"}")
        else:
            super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"{\"message\": \"Feedback submitted successfully (mock response)\"}")
        else:
            super().do_POST()

if __name__ == "__main__":
    PORT = 5000
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print("Qoqon University Alumni server http://localhost:" + str(PORT) + " da ishlayapti")
        httpd.serve_forever()
