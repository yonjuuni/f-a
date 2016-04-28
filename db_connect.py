from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from redis import Redis
from config import REDIS_SETTINGS


def get_redis_conn():
    try:
        r = Redis(**REDIS_SETTINGS).ping()
    except Exception as e:
        print('Unable to connect to Redis.\nError:', e)
    else:
        return r


def get_session():
    try:
        engine = create_engine("{}://{}:{}@{}/{}".format(DB_DRIVER,
                                                         DB_USER,
                                                         DB_PASSWORD,
                                                         DB_HOST,
                                                         DB_NAME), echo=True)
    except Exception as e:
        print('Unable to connect to database.\n'
              'Details:\n{}'.format(e))
    else:
        session = sessionmaker(bind=engine)
        return session()


r = get_redis_conn()
Base = declarative_base()
db = get_session()


movies_actors = Table('movies_actors', Base.metadata,
                      Column('movie_id', Integer, ForeignKey('movie.id')),
                      Column('actor_id', Integer, ForeignKey('actor.id')))


class Movie(Base):

    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    genre = Column(String)
    description = Column(String)

    actors = relationship('Actor',
                          secondary=movies_actors,
                          back_populates='movies')


class Actor(Base):

    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)

    movies = relationship('Movie',
                          secondary=movies_actors,
                          back_populates='actors')
