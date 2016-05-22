from aiohttp_session import get_session
from aiohttp_jinja2 import template

from .db_connect import db
from .helper_functions import get_trailers


@template('index.html')
async def index(request=None):
    session = await get_session(request)
    await request.post()
    query = request.POST.get('query')

    if not session.get('queries'):
        session['queries'] = []
    if (query is not None) and (query not in session['queries']):
        session['queries'].append(query)
    return {'queries': session['queries'][-5:][::-1],
            'trailers': get_trailers()[:10]}
