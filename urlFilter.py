from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import cgi
import json
import re
import time
import threading
import urlparse
import redis


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search('urlinfo/1/\S+:\d+/*', self.path) is None:
            # format is /urlinfo/1/host:port/query
            # check if the url is in the correct format
            response = {}
            response['result'] = 'Bad Request'
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps(response))
        else:
            # request is in the correct format
            r = redis.Redis(host='db')
            response = {}
            url = '/'.join(self.path.split('/')[3:])
            if r.exists(url):
                # if url is known, send result and last update time
                result = r.lrange(url, 0, 2)
                response['timestamp'] = result[0]
                response['result'] = result[1]
                response['category'] = result[2]
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response))

            else:
                # else send unknown result and current time
                response['result'] = 'unknown'
                response['timestamp'] = int(time.time())
                response['category'] = 'unknown'
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response))
        return

    def do_POST(self):
        if self.path != '/urladd/1/':
            # check if the request format is correct
            response = {}
            response['result'] = 'Bad Request'
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps(response))
        else:
            if self.headers['Content-Type'] == 'application/json':
                # check that JSON is being sent as the content type
                length = int(self.headers['Content-Length'])
                timestamp = int(time.time())
                data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                r = redis.Redis(host='db')
                # delete key from redis if it already exists
                if r.exists(data['url']):
                    r.delete(data['url'])
                # create key in redis
                r.lpush(data['url'], data['category'], data['result'], timestamp)
                # send response
                response = {}
                response['result'] = 'success'
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(response))
            else:
                # if JSON was not set as content type, send response
                response = {}
                response['result'] = 'Bad Content-Type'
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps(response))
        return


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = ThreadedHTTPServer(('0.0.0.0', 8080), handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    run()
