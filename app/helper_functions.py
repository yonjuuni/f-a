import logging
import os
import requests
import smtplib
import sys
import tmdbsimple as tmdb
from email.mime.text import MIMEText
from base64 import b64encode
from base64 import b64decode
from random import randrange
from .config import BASE_DIR
from .config import LOG_FILE
from .config import API_KEY
from .db_connect import Movie


tmdb.API_KEY = API_KEY


def get_logger(name):
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.DEBUG,
                        format=('%(asctime)s :: %(name)s :: %(levelname)s :: '
                                '%(message)s'),
                        datefmt='%m/%d/%Y %H:%M:%S')

    return logging.getLogger(name)


logger = get_logger(__file__)


def get_trailers_by_title(title, limit=5):
    r = requests.get("http://trailersapi.com/trailers.json?movie={}&"
                     "limit={}&width=640".format(title, limit))

    if r.json():
        res = []
        for item in r.json():
            res.append([x[4:] for x in item['code'].split()
                        if x.startswith('src')][0])
        return res


def get_trailers(limit, db):
    trailers = []
    for title in [movie.title for movie in
                  [db.query(Movie).get(randrange(0, db.query(Movie).count()))
                   for _ in range(limit)]]:
        title_trailers = get_trailers_by_title(title)
        if title_trailers:
            trailers.extend(title_trailers)
    return trailers


def send_email(subject, text, _to='alex@s1ck.org', _from='info@s1ck.org'):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = _to

    try:
        smtp_conn = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtp_conn.starttls()
        smtp_conn.login('info@s1ck.org', get_email_password())
    except SMTPHeloError:
        logger.error('Unable to initiate SMTP connection.')
    except SMTPAuthenticationError:
        logger.error('Wrong username/password for SMTP authentication.')
    except SMTPNotSupportedError:
        logger.error('The AUTH command is not supported by the server.')
    except SMTPException:
        logger.error('No suitable authentication method was found.')
    else:
        try:
            smtp_conn.send_message(msg)
        except Exception as e:
            logger.error('Unable to send email. Error details: {}'.format(e))
        else:
            logger.info('Sent an email to {}, subject: "{}"'.format(_to,
                                                                    subject))
    finally:
        smtp_conn.quit()


def set_email_password():
    pwd_file = os.path.join(BASE_DIR, '.pwd')
    temp = input('Enter your email account password: ')
    f = open(pwd_file, 'wb')
    f.write(b64encode(temp.encode()))
    f.close()
    print('Password was successfully set up.')


def get_email_password():
    pwd_file = os.path.join(BASE_DIR, '.pwd')
    if os.path.exists(pwd_file):
        f = open(pwd_file, 'rb')
        email_pwd = b64decode(f.read().strip()).decode()
        f.close()
        return email_pwd
    else:
        print("Password doesn't exist, store it by running 'python helper_fun"
              "ctions.py --set-email-password'")
        return ''


def get_movies(_type):
    movies = tmdb.Movies(_type)
    request = movies.info()
    results = []
    for i, movie in enumerate(movies.results):
        for genre in movie['genre_ids']:
            if movies.results[i].get('genres'):
                movies.results[i]['genres'].append(map_genre(genre))
            else:
                movies.results[i]['genres'] = [map_genre(genre), ]
    return movies.results


def get_movie_by_id(_id):
    return tmdb.Movies(_id).info()


def map_genre(_id):
    g = {28: 'Action',
         12: 'Adventure',
         16: 'Animation',
         35: 'Comedy',
         80: 'Crime',
         99: 'Documentary',
         18: 'Drama',
         10751: 'Family',
         14: 'Fantasy',
         10769: 'Foreign',
         36: 'History',
         27: 'Horror',
         10402: 'Music',
         9648: 'Mystery',
         10749: 'Romance',
         878: 'Science Fiction',
         10770: 'TV Movie',
         53: 'Thriller',
         10752: 'War',
         37: 'Western'}
    return g[_id]
