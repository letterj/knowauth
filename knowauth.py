#! /usr/evn/python



import BaseHTTPServer
import cgi
import json
import time


HOST_NAME = '127.0.0.1'     # IP to use
PORT_NUMBER = 8080 	        # Set this to the necessary port 

with open('catalog.json','r') as f:
    catalog = f.read()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        """Respond to a GET request."""
	print time.asctime(), "GET Request"
	if s.headers.has_key('x-auth-user'):
	   acct = s.headers['x-auth-user']     
	else:
	   s.send_response(500)

        body = catalog % {'account': acct}
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(body)

    def do_POST(s):
	"""Respond to a POST request."""
        form = cgi.FieldStorage(
            fp=s.rfile, 
            headers=s.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':s.headers['Content-Type'],
                     })

	data = json.loads(form.value)
	print form.value
	acct = data['auth']['passwordCredentials']['username']		

        body = catalog % {'account': acct}
	print time.asctime(), "POST Request"
	s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(body)

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
