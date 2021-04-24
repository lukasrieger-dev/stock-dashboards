from flask import Flask, render_template, jsonify
from Stock import Stock
from pymongo import MongoClient

app = Flask(__name__, template_folder='./templates')

stocks = dict()
depots = list()
settings = dict()
symbols = None
client = None
db = None
collection_depots = None


@app.route('/')
def index():
    return render_template('index.html', symbols=symbols), 200


@app.route('/dashboard/<string:ticker>')
def dashboard(ticker=None):
    if ticker not in stocks:
        stocks[ticker] = Stock(ticker)

    stock = stocks[ticker]
    stock_data = stock.stock_data()
    return render_template('dashboard.html', data=stock_data), 200


@app.route('/newdepot/<string:depot_name>')
def new_depot(depot_name=None):
    if not depot_name:
        return jsonify('Enter a name'), 422
    else:
        r = collection_depots.insert_one({
            'Name': depot_name
        })
        return render_template('depot.html', depot_name=depot_name), 200


def _init_app(file_name):
    sets = dict()
    symbs = dict()
    read_stocks = False

    with open(file_name, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if '#stocks' in line:
                read_stocks = True
            if '=' not in line:
                continue

            key, value = line.split('=')
            value = value.strip('\n')
            if read_stocks:
                symbs[key] = value
            else:
                sets[key] = value
    return sets, symbs


if __name__ == '__main__':
    settings, symbols = _init_app('settings.txt')

    connection_string = settings['url']
    dbname = settings['dbname']
    collection = settings['collection']

    client = MongoClient(connection_string)
    db = client[dbname]
    collection_depots = db[collection]
    app.run()
