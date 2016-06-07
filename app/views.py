from aiohttp import web
from aiohttp_session import get_session
from aiohttp_jinja2 import template
from .helper_functions import get_trailers
from .helper_functions import get_movies
from .helper_functions import get_movie_by_id
from .helper_functions import send_email
from .helper_functions import get_trailers_by_title
from .db_connect import get_db_session


db = get_db_session()


@template('index.html')
async def index(request):
    _type = request.GET.get('movie_type')
    if not _type:
        _type = 'popular'
    return {'movie_type': _type}


@template('movies.html')
async def movies(request):
    _type = request.GET.get('movie_type')
    return {'movies': get_movies(_type)}


@template('single.html')
async def single(request):
    movie_id = request.match_info['movie_id']
    movie = get_movie_by_id(movie_id)
    trailers = get_trailers_by_title(movie['title'])
    return {'movie': movie,
            'trailers': trailers}


async def email(request):
    data = await request.post()
    message = ("Name: {}\n"
               "Email: {}\n\n"
               "URL: {}\n"
               "Client: {}\n\n"
               "Message: {}".format(data['name'],
                                    data['email'],
                                    request.path_qs,
                                    request.headers['USER-AGENT'],
                                    data['message']))
    send_email('Filmadvisor: Website Feedback', message)

    url = request.app.router['index'].url()

    return web.HTTPFound(url)
