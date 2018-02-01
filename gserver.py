from gevent.wsgi import WSGIServer
from web import create_app

app = create_app('web.config.DevConfig')

server = WSGIServer(('', 80), app)
server.serve_forever()
