from flask import Flask, request, render_template, jsonify
from Stock import Stock

app = Flask(__name__, template_folder='./templates')

stocks = dict()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/<ticker>')
def dashboard(ticker=None):
    if ticker not in stocks:
        stocks[ticker] = Stock(ticker)

    stock = stocks[ticker]
    stock_data = stock.stock_data()
    return render_template('dashboard.html', data=stock_data)


if __name__ == '__main__':
    app.run()
