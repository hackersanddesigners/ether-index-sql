import os
from os.path import join, dirname
from dotenv import load_dotenv
import pymysql.cursors
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from jinja2 import Environment, FileSystemLoader
import get_from_db
from operator import itemgetter
from datetime import datetime

# -- load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class App(object):
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), './')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)

        def datetime_format(timestamp):
            # <https://stackoverflow.com/a/31548402>
            # divide by /1000 to convert from milliseconds to seconds
            ts = timestamp / 1000

            # <https://stackoverflow.com/a/37188257>
            ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')

            return ts

        self.jinja_env.filters['datetime'] = datetime_format

        # -- routes
        self.url_map = Map([
            Rule('/', endpoint='main'),
            Rule('/*', redirect_to='main'),
        ])

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except NotFound as e:
            print(e)
            return self.error_404()
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    # -- views
    def on_main(self, request, get_from_db=get_from_db):
        if request.method == 'GET':
            # -- setup db connection
            connection = pymysql.connect(host=os.getenv('DB_HOST'),
                                         user=os.getenv('DB_USER'),
                                         password=os.getenv('DB_PASSWORD'),
                                         db=os.getenv('DB_NAME'),
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

            # get all pads and sort them by timestamp
            pads = get_from_db.get_data(connection)
            pads = sorted(pads, key=itemgetter(1), reverse=True)

            ep_port = os.getenv('EP_PORT')

            return self.render_template('index.html', pads=pads, ep_port=ep_port)

    def error_404(self):
        response = self.render_template('404.html')
        response.status_code = 404
        return response


def create_app(with_static=True):
    app = App()
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5005, app, use_debugger=True, use_reloader=True)
