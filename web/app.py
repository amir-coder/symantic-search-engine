from flask import Flask
from flask import render_template, redirect, request
import time
from sse import SSE


app = Flask(__name__)
sse = SSE(database_filename='wiki_movie_plots_deduped.csv')

@app.route('/', methods=['GET', 'POST'])

def home():
    #genres we take into consideration in the platform
    genres = ['western','comedy', 'short', 'short film', 'biographical', 'drama', 'adventure', 'short fantasy', 'sports', 'horror','crime']
    if request.method == 'GET':
        return render_template('home.html', genre_list=genres,
                                stat='start', plot = '')
    elif request.method == 'POST':
        print(request.form.get('plot'))
        #start timer
        start = time.perf_counter()
        #creating the filter
        filter = {
            'plot': request.form.get('plot'),
            'genre': request.form.get('genre'),
            'k': int(request.form.get('k')),
            'start-release-year': int(request.form.get('start-release-year')),
            'end-release-year': int(request.form.get('end-release-year')),
        }
        print(filter)
        #search
        results = sse.search(filter=filter)
        #end timer
        end = time.perf_counter()
        search_time = round(end - start, 4)
        print('results:')
        print(results)
        return render_template(
            'home.html', 
            genre_list=genres, 
            stat='done', 
            results=results, 
            search_time = search_time,
            plot=request.form.get('plot')
        )

if __name__ == '__main__':
    app.run(debug=True)