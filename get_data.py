import re
from db_connect import r


file_1 = '/home/alex/code/filmadvisor/sources/movies_filtered.txt'
file_2 = '/home/alex/code/filmadvisor/sources/movies.list'
file_3 = '/home/alex/code/filmadvisor/sources/movie-titles.txt'


def check_title(title):
    return r.hget('movies', title)


def clean(line):
    rx_title_year = re.compile(r"""(.*)\s+\((\d{4,}|\D{4,})\)\s[\s{]""")
    rx_episode = re.compile(r"""{(.*)}""")
    title_year = re.findall(rx_title_year, line)
    episode = re.findall(rx_episode, line)

    if title_year:
        title = title_year[0][0]
        if title.startswith('"') and title.endswith('"'):
            title = title[1:-1]
        year = title_year[0][1]
    else:
        title, year = None, None
    if episode:
        episode = episode[0]
    else:
        episode = None

    return title, year, episode


titles = set()
for movie in [item.strip() for item in open(file_1).readlines()]:
    titles.add(movie)

for line in [item.strip() for item in open(file_2, encoding='latin-1').readlines()]:
    movie = clean(line)[0]
    if movie:
        if not check_title(movie):
            r.hset('movies', movie, i)
            print('{}: {}'.format(i, movie))
print('{}: {}'.format(i, movie))
