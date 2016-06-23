import os
import aiohttp_jinja2
import jinja2

from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from .config import SECRET_KEY, BASE_DIR
from . import views


app = web.Application(middlewares=[session_middleware(
    EncryptedCookieStorage(SECRET_KEY))])

# Routes
app.router.add_route('GET', '/', views.index, name='index')
app.router.add_route('POST', '/', views.email)

app.router.add_route('GET', '/movie/{movie_id}', views.single, name='movie')
app.router.add_route('POST', '/movie/{movie_id}', views.email)

app.router.add_route('GET', '/movies/{movie_type}', views.movies)

app.router.add_route('GET', '/popular', views.index, name='popular')
app.router.add_route('POST', '/popular', views.email)
app.router.add_route('GET', '/top', views.index, name='top')
app.router.add_route('POST', '/top', views.email)
app.router.add_route('GET', '/upcoming', views.index, name='upcoming')
app.router.add_route('POST', '/upcoming', views.email)

app.router.add_static('/static',
                      os.path.join(BASE_DIR, 'static'),
                      name='static')

aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(os.path.join(BASE_DIR,
                                                                 'templates')))


def runserver():
    web.run_app(app)
