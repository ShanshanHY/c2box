from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
import json
import c2box
import convert

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if parsed_url.path == "/convert":
            if "sub" in query_params:
                outbounds = c2box.build_outbound(query_params["sub"])
                if "template" in query_params:
                    try:
                        req = requests.get(url=query_params["template"][0])
                        template = req.json()
                    except:
                        self.send_response(401)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write("Get Template Fail".encode())
                        return
                    outbounds = convert.base.merge_dict(template, outbounds)
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', 'attachment; filename=config.json')
                self.end_headers()
                self.wfile.write(json.dumps(outbounds, ensure_ascii=False, indent=4).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("No Clash Subscribe".encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not Found".encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
