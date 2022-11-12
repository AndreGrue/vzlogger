#!/usr/bin/env python3
#################################################################################
import http.server


###
class PostHttpHandler(http.server.BaseHTTPRequestHandler):
    """
    """
    def __init__(self, callback=None):
        self._callback = callback

    def do_POST(self):
        # get request
        path            = str(self.path)
        content_length  = int(self.headers['Content-Length'])
        host            = str(self.headers['Host'])
        accept          = str(self.headers['Accept'])
        content_type    = str(self.headers['Content-type'])
        user_agent      = str(self.headers['User-Agent'])
        post_data       = self.rfile.read(content_length).decode('utf-8')

        #print("POST request,\nPath: %s\nLength: %d\nhost: %s\ncontent_type: %s\n \nBody:\n%s\n"
        #       % (path, content_length, host, content_type, post_data ))

        if self._callback:
            self._callback(post_data)

        # send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


###
def run(server_class=http.server.HTTPServer, handler_class=PostHttpHandler, host='127.0.0.1', port=63333):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


###
def main():
    run()

###
if __name__ == "__main__":
    main()

