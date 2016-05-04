from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,\
                       Table, Float, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects import postgresql
from redis import Redis
from config import DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME,\
                   REDIS_SETTINGS
from config import APP_DEBUG as DEBUG
from helper_functions import get_logger


logger = get_logger(__file__)
Base = declarative_base()


# movies_actors = Table('movies_actors', Base.metadata,
#                       Column('movie_id', Integer, ForeignKey('movie.id')),
#                       Column('actor_id', Integer, ForeignKey('actor.id')))


class Movie(Base):

    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    description = Column(String)
    imdb_rating = Column(Float)
    genres = Column(postgresql.ARRAY(Integer, dimensions=1))
    type = Column(Enum('movie', 'series', 'episode'))
    imdb_id = Column(String)
    poster_url = Column(String)
    checked = Column(Boolean)
    errors = Column(Boolean)

    # actors = relationship('Actor',
                          # secondary=movies_actors,
                          # back_populates='movies')


# class Actor(Base):

#     __tablename__ = 'actor'

#     id = Column(Integer, primary_key=True)

#     movies = relationship('Movie',
#                           secondary=movies_actors,
#                           back_populates='actors')


def get_redis_conn():
    try:
        r = Redis(**REDIS_SETTINGS)
        r.ping()
    except Exception as e:
        print('Unable to connect to Redis.\nError:', e)
    else:
        return r


def get_session():
    try:
        engine = create_engine("{}:///{}".format(DB_DRIVER,
                                                 DB_NAME), echo=DEBUG)
        session = sessionmaker(bind=engine)
        session().query(Movie).limit(1)
    except Exception as e:
        # print('Unable to connect to database.\n'
        #       'Details:\n{}'.format(e))
        logger.critical('Unable to connect to database. '
                        'Details:\n{}'.format(e))
        raise e
    else:
        return session()


db = get_session()
r = get_redis_conn()
