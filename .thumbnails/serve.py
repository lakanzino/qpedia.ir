import http.server, socketserver, os, urllib.parse

ROOT = '/home/user/qpedia.ir'
PORT = 8080

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        path = urllib.parse.unquote(self.path)
        if path.lower().endswith(('.zip', '.png', '.csv', '.webp')):
            name = os.path.basename(path)
            self.send_header('Content-Disposition', f'attachment; filename="{name}"')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass

with socketserver.ThreadingTCPServer(('0.0.0.0', PORT), H) as httpd:
    httpd.serve_forever()
