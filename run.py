from flask import Flask, escape, request, render_template, url_for
import requests
import os
app = Flask(__name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def index():
    return render_template('flash.html')

@app.route('/home')
def home():
    api = 'https://corona.lmao.ninja/countries'
    r = requests.get(api)
    countries = r.json()
    return render_template('index.html', countries=countries)

@app.route('/secondhome')
def secondhome():
    api_country = 'https://corona.lmao.ninja/countries'
    r = requests.get(api_country)
    countries = r.json()
    api_all = 'https://corona.lmao.ninja/all'
    r = requests.get(api_all)
    cases = r.json()
    return render_template('index.html', countries=countries, cases=cases)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print("Starting app on port %d" % port)
app.run(debug=False, port=port, host='0.0.0.0')