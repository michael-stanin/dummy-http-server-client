from http.server import BaseHTTPRequestHandler,HTTPServer
from typing import Iterable
import threading

class RequestResponse:
    def __init__(self, req_path, req_method='GET', res_code=200, res_content_type='application/json', res_body='') -> None:
        self.req_path = req_path
        self.req_method = req_method

        self.res_code = res_code
        self.res_content_type = res_content_type
        self.res_body = res_body

class CustomHTTPServer:
    """A simple configurable HTTP server.
    - Can be configured with different responses to different requests.
    - Note: by default server starts in a background thread.
    - WARNING: SERVER IS NOT SECURE AND FOR INTERNAL TESTING ONLY, NOT TO BE USED IN ANY PRODUCTION CODE!
    - example usage:
        - >>> responses = [RequestResponse('/someplace/', res_body='my response string')]
        - >>> my_server = CustomHTTPServer('localhost', 8080, responses)
        - >>> my_server.start()
        - >>> ... do stuff
        - >>> my_server.stop()

    TODO: till this point it only handles GET requests; however, CustomHandler can be easily extended to support more http request methods.
    """
    def __init__(self, host:str, port:str, req_res:Iterable[RequestResponse]):
        print('WARNING: SERVER IS NOT SECURE AND FOR INTERNAL TESTING ONLY, NOT TO BE USED IN ANY PRODUCTION CODE!')
        CustomHandler.req_res = self.__tidy_responses(req_res)
        print(CustomHandler.req_res)
        self.s = HTTPServer((host, port), CustomHandler)

    def start(self, in_thread=True):
        """starts the server.
        - :param in_thread:  if True, a background thread is started and will serve requests until stop is called, or KeyInterrupt. If False, this method will block until stop() is called from another thread, or KeyboardInterrupt is passed."""
        self.in_thread = in_thread
        if self.in_thread:
            self.thread = threading.Thread(target=self.s.serve_forever)
            self.thread.start()            
        else:
            self.s.serve_forever()

    def stop(self):
        if self.in_thread:
            self.s.shutdown()
            self.thread.join()
        else:
            self.s.socket.close()

    def __tidy_responses(self, req_res:Iterable[RequestResponse]):
        res = {}
        for r in req_res:
            res[(r.req_path, r.req_method)] = dict(code=r.res_code, content_type=r.res_content_type, body=r.res_body)
        return res

class CustomHandler(BaseHTTPRequestHandler):
    req_res = None
    def do_GET(self):
        print('request:')
        key = (self.path, 'GET')
        print(key)
        if key in self.req_res:
            res = self.req_res[key]
            print('response:')
            print(res)

            self.send_response(res['code'])
            self.send_header('Content-type',res['content_type'])
            self.end_headers()
            self.wfile.write(res['body'].encode('utf-8'))
        else:
            print('response: 404 not found!')
            self.send_response(404)
            self.end_headers()
        return


import json
if __name__ == '__main__':
    mything = {"key1": ("value1", "value2"), "key2": ["value3", "value4"]}
    my_json_response = json.dumps(mything)
    responses = [RequestResponse('/special-request/much-wow/42', res_body=my_json_response),
        RequestResponse('/', res_body='THIS IS A TEXT RESPONSE', res_content_type='text/plain')]
    try:
        # See https://pythonspeed.com/articles/docker-connection-refused/ to understand why it's not localhost -> it wouldn't listen on all interfaces and it won't be reachable by other pods
        server = CustomHTTPServer('0.0.0.0',5000, responses)
        print('Started http server')
        server.start()
         
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.stop()