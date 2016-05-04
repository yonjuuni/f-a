import asyncio
import aiohttp
import sys
import signal
from helper_functions import get_logger
from db_connect import db, Movie
from pprint import pprint
from config import APP_DEBUG as DEBUG
from urllib.parse import quote


QUERY_LIMIT = 100
URL = 'http://www.omdbapi.com/'
REQUEST_TIMEOUT = 10


logger = get_logger(__file__)
loop = asyncio.get_event_loop()
conn = aiohttp.TCPConnector(limit=50)
session = aiohttp.ClientSession(loop=loop, connector=conn)


async def get_json(session, url, query):
    with aiohttp.Timeout(REQUEST_TIMEOUT):
        async with session.get(url, params=query) as response:
            assert response.status == 200
            return await response.json()


async def omdb_get(movie):
    query = {'y': movie.year if movie.year else '',
             't': quote(movie.title),
             'plot': 'full'
             }
    data = await get_json(session, URL, query)

    if DEBUG:
        pprint(data)

    return data


async def check_movie(movie):
    print('{}: Working'.format(movie.id))
    try:
        res = await omdb_get(movie)
    except:
        if DEBUG:
            print('Exception took place. Details: ', sys.exc_info())
        logger.error('{} :: "{}" :: {}'.format(movie.id, movie.title,
                                               sys.exc_info()))
        res = {}
        res['errors'] = True
    else:
        return res


async def work_item(movie):
    res = await check_movie(movie)

    if res:
        if res.get('Response', 0) == 'True':

            if res.get('Type') in ['movie', 'series', 'episode']:
                movie.type = res.get('Type')

            movie.imdb_id = res.get('imdbID')

            if res.get('Poster') != 'N/A':
                movie.poster_url = res.get('Poster')
            else:
                movie.poster_url = None

            if res.get('imdbRating') != 'N/A':
                movie.imdb_rating = float(res.get('imdbRating'))

            # movie.genres = res.get('genres')
            # movie.actors = res.get('actors')

            if res.get('Plot') != 'N/A':
                movie.description = res.get('Plot')
            else:
                movie.description = None
        else:
            print('{}: Not found ({})'.format(movie.id, movie.title))
            logger.warning('{} - "{}" ({})'.format('NOT FOUND',
                                                   movie.id,
                                                   movie.title))
            movie.errors = True

        if DEBUG:
            print(movie.__dict__)

        try:
            movie.checked = True
            db.add(movie)
            db.flush()
        except Exception as e:
            print('There was an error in DB commit: ', e)
            logger.error('{} :: "{}" :: {}'.format(movie.id, movie.title, e))
            db.rollback()
        else:
            print('{}: Success (DB update)'.format(movie.id))
        finally:
            db.commit()


def walker():

    while True:
        q = db.query(Movie).filter(Movie.checked == False).limit(QUERY_LIMIT)

        if not q.count():
            break

        tasks = [work_item(i) for i in q]
        logger.info('Updating {} items now.'.format(len(tasks)))
        loop.run_until_complete(asyncio.gather(*tasks))


def exit(*args):
    logger.info('EXITING NOW.')
    loop.stop()
    session.close()
    loop.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    walker()
    exit()
