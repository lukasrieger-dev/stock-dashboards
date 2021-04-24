from flask import Flask, render_template, jsonify
from Stock import Stock

app = Flask(__name__, template_folder='./templates')

stocks = dict()
depots = list()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/<string:ticker>')
def dashboard(ticker=None):
    if ticker not in stocks:
        stocks[ticker] = Stock(ticker)

    stock = stocks[ticker]
    stock_data = stock.stock_data()
    return render_template('dashboard.html', data=stock_data)

@app.route('/newdepot/<string:name>')
def new_depot(name=None):
    if not name:
        return jsonify('Enter a name'), 422
    else:
        return jsonify(f'New depot {name} was created.'), 200



if __name__ == '__main__':
    app.run()
