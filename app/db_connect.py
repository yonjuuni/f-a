from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Float
from sqlalchemy import Enum
from sqlalchemy import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from .config import DB_DRIVER
from .config import DB_USER
from .config import DB_PASSWORD
from .config import DB_HOST
from .config import DB_NAME
from .config import APP_DEBUG
from .helper_functions import get_logger


logger = get_logger(__file__)
Base = declarative_base()


movies_actors = Table('movies_actors', Base.metadata,
                      Column('movie_id', Integer,
                             ForeignKey('movie.movie_id')),
                      Column('actor_id', Integer,
                             ForeignKey('actor.actor_id')))

movies_genres = Table('movies_genres', Base.metadata,
                      Column('movie_id', Integer,
                             ForeignKey('movie.movie_id')),
                      Column('genre_id', Integer,
                             ForeignKey('genre.genre_id')))


class Movie(Base):

    __tablename__ = 'movie'

    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    plot = Column(String)
    imdb_rating = Column(Float)
    movie_type = Column(Enum('movie', 'series', 'episode'))
    imdb_id = Column(String)
    poster_url = Column(String)
    checked = Column(Boolean)
    errors = Column(Boolean)

    actors = relationship('Actor',
                          secondary=movies_actors,
                          back_populates='movies')

    genres = relationship('Genre',
                          secondary=movies_genres,
                          back_populates='movies')

    def __init__(self, title, year):
        self.title = title
        self.year = year


class Actor(Base):

    __tablename__ = 'actor'

    actor_id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship('Movie',
                          secondary=movies_actors,
                          back_populates='actors')

    def __init__(self, name):
        self.name = name


class Genre(Base):

    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship('Movie',
                          secondary=movies_genres,
                          back_populates='genres')

    def __init__(self, name):
            self.name = name


def get_session():
    try:
        engine = create_engine("{}:///{}".format(DB_DRIVER,
                                                 DB_NAME),
                               echo=APP_DEBUG)
        session = sessionmaker(bind=engine)
        session().query(Genre).first()
    except Exception as e:
        logger.critical('Unable to connect to database. '
                        'Details:\n{}'.format(e))
        raise e
    else:
        return session()


db = get_session()
