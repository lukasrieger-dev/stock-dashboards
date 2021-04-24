


class Depot:
    def __init__(self, name):
        self.name = name
        self.stocks = dict()

    def buy_stock(self, ticker, price, count):
        # if there are already stocks for this ticker, update the average price
        if ticker in self.stocks:
            old_avg_price, old_total = self.stocks[ticker]
            new_avg_price = (old_total*old_avg_price + count*price) / (old_total + count)
            new_total = old_total + count
            price = new_avg_price
            count = new_total
        self.stocks[ticker] = (price, count)

    def sell_stock(self, ticker, price, count):
        if ticker not in self.stocks or self.stocks[ticker] == 0:
            return False
        average_price, total_count = self.stocks[ticker]

        if count > total_count:
            return False
        new_total = total_count - count

        if new_total == 0:
            del self.stocks[ticker]
        else:
            self.stocks[ticker] = (average_price, new_total)

        return True

    def list_stocks(self):
        stock_list = list(self.stocks.items())
        return  stock_list




