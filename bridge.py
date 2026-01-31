import http.server
import json
import os

PORT = 8080

class BridgeHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/update_command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Menerima data dari Dashboard (script.js)
                data = json.loads(post_data)
                
                # Menulis data ke command.json agar dibaca main.py
                with open("command.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                # Mengirim respon balik ke browser
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
                print(f"[✔] Perintah diterima: {data['tool_name']} -> {data['target']}")
                
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)

    # Mengizinkan CORS agar browser tidak memblokir permintaan
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    print(f"🚀 Bridge Server aktif di http://localhost:{PORT}")
    print("Gunakan server ini sebagai pengganti 'python -m http.server'")
    http.server.HTTPServer(('', PORT), BridgeHandler).serve_forever()
