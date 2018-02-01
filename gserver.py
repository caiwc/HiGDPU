from gevent.wsgi import WSGIServer
from web import create_app

app = create_app('web.config.DevConfig')

server = WSGIServer(('', 5000), app)
server.serve_forever()
