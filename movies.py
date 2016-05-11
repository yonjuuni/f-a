import asyncio
import aiohttp
import sys
import signal
import os
from helper_functions import get_logger
from db_connect import db
from db_connect import Movie
from db_connect import Genre
from db_connect import Actor
from pprint import pprint
from config import APP_DEBUG
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

    if APP_DEBUG:
        pprint(data)

    return data


async def check_movie(movie):
    print('{}: Working'.format(movie.movie_id))
    try:
        data = await omdb_get(movie)
    except:
        logger.error('{} :: "{}" :: {}'.format(movie.movie_id, movie.title,
                                               sys.exc_info()))
        data = {}
        data['errors'] = True
    else:
        return data


def push_to_db(obj):
    db.add(obj)
    db.commit()


db_genres = [genre.name for genre in db.query(Genre).all()]
db_actors = [actor.name for actor in db.query(Actor).all()]


def parse_response(data, movie):
    if data.get('Type') in ['movie', 'series', 'episode']:
        movie.movie_type = data.get('Type')

    movie.imdb_id = data.get('imdbID')

    if data.get('Poster') != 'N/A':
        movie.poster_url = data.get('Poster')

    if data.get('imdbRating') != 'N/A':
        movie.imdb_rating = float(data.get('imdbRating'))

    if data.get('Genre') != 'N/A':
        # db_genres = [genre.name for genre in db.query(Genre).all()]
        for genre in [g.strip(' ,').lower() for g
                      in data.get('Genre').split()]:

            if genre not in db_genres:
                db_genres.append(genre)
                push_to_db(Genre(name=genre))

            if genre not in [g.name for g in movie.genres]:
                movie.genres.append(db.query(Genre).
                                    filter(Genre.name == genre).one())

    if data.get('Actors') != 'N/A':
        for actor in [actor.strip() for actor
                      in data.get('Actors').split(',')]:

            if actor not in db_actors:
                db_actors.append(actor)
                push_to_db(Actor(name=actor))

            if actor not in [actor.name for actor in movie.actors]:
                movie.actors.append(db.query(Actor).
                                    filter(Actor.name == actor).one())

    if data.get('Plot') != 'N/A':
        movie.plot = data.get('Plot')

    return movie


async def work_item(movie):
    data = await check_movie(movie)

    if data:
        if data.get('Response', 0) == 'True':
            movie = parse_response(data, movie)

        else:
            print('{}: Not found ({})'.format(movie.movie_id, movie.title))
            logger.warning('{} - "{}" ({})'.format('NOT FOUND', movie.movie_id,
                                                   movie.title))
            movie.errors = True

        if APP_DEBUG:
            print(movie.__dict__)

        try:
            movie.checked = True
            push_to_db(movie)
        except Exception as e:
            print('There was an error in DB commit: ', e)
            logger.error('{} :: "{}" :: {}'.format(movie.movie_id,
                                                   movie.title, e))
            db.rollback()
        else:
            print('{}: Success (DB update)'.format(movie.movie_id))


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
