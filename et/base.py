import json
import tornado.web

__author__ = 'xuemingli'


class RequestHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        raise NotImplementedError()

    def jsonify(self, **kwargs):
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        if self.application.settings.get('cors', True):
            self.set_header('Access-Control-Allow-Origin', "*")
            self.set_header('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept")
            self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.write(json.dumps(kwargs))
        self.finish()

    def abort(self, code, message):
        self.jsonify(code=code, message=str(message))

    def options(self, *args, **kwargs):
        if self.application.settings.get('cors', True):
            self.set_header('Access-Control-Allow-Origin', "*")
            self.set_header('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept")
            self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.finish()
