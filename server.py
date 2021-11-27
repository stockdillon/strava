import http.server
import socketserver
import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import urllib
from strava import Strava

class Handler(BaseHTTPRequestHandler):
    def parse_params(self, path=''):
        params = urllib.parse.urlparse(path)
        param_dict = urllib.parse.parse_qs(params.query)
        return param_dict
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        param_dict = self.parse_params(self.path)
        print('param_dict:', param_dict)
        prof = Strava()
        self.wfile.write(bytes(json.dumps(prof.__dict__, default=lambda o: o.__dict__), encoding='utf-8'))


PORT = 5000

myserver = HTTPServer(("", 5000), Handler)
myserver.serve_forever()