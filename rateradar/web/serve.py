import http.server
import socketserver
import os

PORT = 8000
ROOT_DIRECTORY = "public"  # Specify your root directory here

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # You can add custom handling here if needed
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    root = os.path.join(os.path.dirname(__file__), ROOT_DIRECTORY)
    os.chdir(root)  # Change the current working directory to ROOT_DIRECTORY
    with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()