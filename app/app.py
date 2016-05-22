import asyncio
import aiohttp_jinja2
import jinja2
import os
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from .config import SECRET_KEY, BASE_DIR
from . import views


app = web.Application(middlewares=[session_middleware(
        EncryptedCookieStorage(SECRET_KEY))])

# Routes
app.router.add_route('GET', '/', views.index)
app.router.add_route('POST', '/', views.index)
app.router.add_static('/static',
                      os.path.join(BASE_DIR, 'static'),
                      name='static')


aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(os.path.join(BASE_DIR,
                                                                 'templates')))


def runserver():
    web.run_app(app)
