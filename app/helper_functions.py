import os
import requests
import smtplib
import logging
from email.mime.text import MIMEText
from base64 import b64encode
from base64 import b64decode
from config import LOG_FILE


def get_trailers_by_title(title, limit=5):
    r = requests.get("http://trailersapi.com/trailers.json?movie={}&"
                     "limit={}&width=640".format(title, limit))

    if r.json():
        res = []
        for item in r.json():
            res.append([x[4:] for x in item['code'].split()
                        if x.startswith('src')][0])
        return res


# TODO: remove hardcoded titles.
def get_trailers():
    trailers = []
    for title in ['Love Actually', 'Cloud Atlas']:
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
    except Exception as e:
        logger.error('Unable to connect to SMTP server. '
                     'Error details: {}'.format(e))
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
    basedir = os.path.abspath(os.path.dirname(__file__))
    pwd_file = os.path.join(basedir, '.pwd')
    temp = input('Enter your email account password: ')
    f = open(pwd_file, 'wb')
    f.write(b64encode(temp.encode()))
    f.close()
    print('Password was successfully set up.')


def get_email_password():
    basedir = os.path.abspath(os.path.dirname(__file__))
    pwd_file = os.path.join(basedir, '.pwd')
    if os.path.exists(pwd_file):
        f = open(pwd_file, 'rb')
        email_pwd = b64decode(f.read().strip()).decode()
        f.close()
        return email_pwd
    else:
        print("Password doesn't exist, store it by running 'python helper_fun"
              "ctions.py'")
        return ''


def get_logger(name):
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.DEBUG,
                        format=('%(asctime)s :: %(name)s :: %(levelname)s :: '
                                '%(message)s'),
                        datefmt='%m/%d/%Y %H:%M:%S')
    return logging.getLogger(name)


logger = get_logger(__file__)


if __name__ == '__main__':
    ans = input("Set email password? (y/n) ").lower()
    if ans == 'y':
        set_email_password()
