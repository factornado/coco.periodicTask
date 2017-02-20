import os
import time
import json
from tornado import ioloop, web, httpserver, process
import logging

from utils import Config
from todo import todo
from do import do

config = Config('config.yml')

logging.basicConfig(
    level=20,  # Set to 20 for diasabling the debug logs.
    filename=config.conf['log']['file'],
    format='%(asctime)s (%(filename)s:%(lineno)s)- %(levelname)s - %(message)s',
    )
logging.Formatter.converter = time.gmtime
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('tornado').setLevel(logging.WARNING)
logging.info('='*80)


class Info(web.RequestHandler):
    def get(self):
        self.write(config.conf)


class Heartbeat(web.RequestHandler):
    def get(self):
        config.register()
        self.write("ok")


class Todo(web.RequestHandler):
    def initialize(self, config=None):
        assert config is not None
        self.config = config

    def post(self):
        out = todo(self.config)
        self.write(json.dumps(out))


class Do(web.RequestHandler):
    def initialize(self, config=None):
        assert config is not None
        self.config = config

    def post(self):
        out = do(self.config)
        self.write(json.dumps(out))


class SomeHandler(web.RequestHandler):
    def get(self, param=''):
        self.write(
            "Hello from service {}. "
            "You've asked for uri {}\n".format(
                config.conf['name'], param))

app = web.Application([
    ("/(swagger.json)", web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
    ("/swagger", web.RedirectHandler, {'url': '/swagger.json'}),
    ("/heartbeat", Heartbeat),
    ("/info", Info),
    ("/todo", Todo, {'config': config}),
    ("/do", Do, {'config': config}),
    ("/(.*)", SomeHandler),
    ])

if __name__ == '__main__':
    port = config.get_port()  # We need to have a fixed port in both forks.
    logging.info('Listening on port {}'.format(port))
    time.sleep(2)  # We sleep for a few seconds to let the registry start.
    if os.fork():
        config.register()
        server = httpserver.HTTPServer(app)
        server.bind(config.get_port(), address='0.0.0.0')
        server.start(config.conf['threads_nb'])
        ioloop.IOLoop.current().start()
    elif os.fork():
        process.fork_processes(config.conf['do_threads_nb'])
        ioloop.PeriodicCallback(config.do_callback,
                                config.conf['do_callback_period']*1000).start()
        ioloop.IOLoop.instance().start()
    elif os.fork():
        ioloop.PeriodicCallback(config.todo_callback,
                                config.conf['todo_callback_period']*1000).start()
        ioloop.IOLoop.instance().start()
    else:
        ioloop.PeriodicCallback(config.heartbeat,
                                config.conf['heartbeat']['period']*1000).start()
        ioloop.IOLoop.instance().start()
