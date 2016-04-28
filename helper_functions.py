import os
import requests
import smtplib
from email.mime.text import MIMEText
from base64 import b64encode, b64decode


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
        t = get_trailers_by_title(title)
        if t:
            trailers.extend(t)
    return trailers


def send_email(subject, text, _to='alex@s1ck.org', _from='info@s1ck.org'):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = _to

    try:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('info@s1ck.org', get_email_password())
    except Exception as e:
        print('Unable to connect to SMPT server.\nError details:', e)
    else:
        try:
            s.send_message(msg)
        except Exception as e:
            print('Unable to send email.\nError details:', e)
    finally:
        s.quit()


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


if __name__ == '__main__':
    ans = input("Set email password? (y/n) ").lower()
    if ans == 'y':
        set_email_password()
