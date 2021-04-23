import yfinance as yf
import requests
from googlesearch import search

NAME = 'longName'
SHORT_NAME = 'shortName'
SECTOR = 'sector'
SUMMARY = 'longBusinessSummary'
CITY = 'city'
COUNTRY = 'country'
WEBSITE = 'website'
INDUSTRY = 'industry'
CURRENCY = 'currency'
AVERAGE50 = 'fiftyDayAverage'
OPEN = 'open'
DAYLOW = 'dayLow'
DAYHIGH = 'dayHigh'
ASK = 'ask'
BID = 'bid'
MARKETCAP = 'marketCap'
YEARHIGH = 'fiftyTwoWeekHigh'
YEARLOW = 'fiftyTwoWeekLow'
TIMEZONE = 'exchangeTimezoneName'
ENTERPRISE_TO_REVENUE = 'enterpriseToRevenue'
SHARES_OUTSTANDING = 'sharesOutstanding'
LOGO = 'logo_url'
PRICE = 'regularMarketPrice'


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.chart = self._download_chart()
        self._download_logo()
        self.news = self._search_news()

    def _download_logo(self):
        # save logo to folder static
        logo_url = self.info[LOGO]
        response = requests.get(logo_url)
        image_name = './static/' + self.ticker + '.png'

        with open(image_name, 'wb') as f:
            f.write(response.content)

    def _download_chart(self):
        raw_data = yf.download(
            tickers=self.ticker,
            period="6mo",
            interval="1d",
            group_by='ticker',
            auto_adjust=True,
            prepost=True,
            threads=True,
            proxy=None
        )
        values = list(raw_data['Open'])
        values = [float("{:.2f}".format(v)) for v in values]

        #labels = [x.astype(str) for x in list(raw_data.index.values)]
        #labels = [l[:10] for l in labels]
        labels = [x for x in range(len(values))]

        print(labels)
        print(values)
        return labels, values

    def stock_data(self):
        info = self.info

        return {
            NAME: info[NAME],
            SUMMARY: info[SUMMARY],
            INDUSTRY: info[INDUSTRY],
            'location': info[CITY] + ', ' + info[COUNTRY],
            WEBSITE: info[WEBSITE],
            PRICE: info[CURRENCY] + ' ' + str(info[PRICE]),
            MARKETCAP: info[CURRENCY] + ' ' + str(info[MARKETCAP]),
            YEARHIGH: info[CURRENCY] + ' ' + str(info[YEARHIGH]),
            YEARLOW: info[CURRENCY] + ' ' + str(info[YEARLOW]),
            'logo': self.ticker + '.png',
            'chart': self.chart,
            'news': self.news
        }

    def _search_news(self):
        query = 'News today ' + self.info[NAME]
        results = []

        for result in search(query, num_results=7):
            results.append(result)

        return results







"""
print(stock.recommendations)
# show major holders
print(stock.major_holders)
print(stock.institutional_holders)
data = stock.info

x = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = "EH",

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "5d",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "30m",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )
print(x)


options: {
            scales: {
                xAxes: [{
                    display: true,
                    type: 'string',
                    time: {
                        parser: 'YYYY-MM-DD',
                        tooltipFormat: 'DD.MM.YYYY',
                        unit: 'day',
                        unitStepSize: 3,
                        displayFormats: {
                            'day': 'DD.MM.YYYY'
                        }
                    }
                }]
            }
        }
"""
