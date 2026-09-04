# -*- coding: utf-8 -*-
"""Static preview server for the QPedia scientist-posters gallery.
Serves the repo root inline (images render in-browser), ZIP stays downloadable.
Binds 0.0.0.0 for the Arena live-preview proxy."""
import http.server, socketserver, os, urllib.parse

ROOT = '/home/user/qpedia.ir'
PORT = 8080


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        path = urllib.parse.unquote(self.path)
        # ZIP is the only attachment; images/HTML stay inline for preview.
        if path.lower().endswith('.zip'):
            name = os.path.basename(path)
            self.send_header('Content-Disposition', f'attachment; filename="{name}"')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


with socketserver.ThreadingTCPServer(('0.0.0.0', PORT), H) as httpd:
    httpd.serve_forever()
