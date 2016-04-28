from flask import Flask, render_template, request, session
from db_connect import db
from helper_functions import get_trailers


app = Flask('filmadvisor')
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index(trailers=None):
    query = request.form.get('query')
    trailers = get_trailers()
    if not session.get('queries', 0):
        session['queries'] = []
    if query is not None and query not in session['queries']:
        session['queries'].append(query)
    return render_template('index.html',
                           queries=session['queries'][-5:][::-1],
                           trailers=trailers[:10])

if __name__ == '__main__':
    app.run()
