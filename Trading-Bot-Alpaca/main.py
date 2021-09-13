# TODO-List:
#       - Recive real-time and/or historical data
#       - Analyse the data using a algoritme 
#           - Buy and sell
#       - Display trades, individual profit/loss, total daily profit/loss, all-time profit/loss

import alpaca_trade_api as tradeapi
from config import *
from datetime import datetime, timedelta

class TradingBot:
    def __init__(self):
        self.running = True
        self.api = tradeapi.REST(API_KEY, API_SECRET_KEY, base_url='https://paper-api.alpaca.markets')

        # Check if the market is open
        self.account = self.api.get_account()
        self.clock = self.api.get_clock()
        print('The market is {}'.format('open' if self.clock.is_open else 'closed'))

        """
        # Check when the market opens and close today
        self.date = datetime.now()
        self.calendar = self.api.get_calendar(start=self.date, end=self.date)[0]
        self.market_open = datetime(2000, 1, 1, self.calendar.open.hour, self.calendar.open.minute, self.calendar.open.second) + timedelta(hours=6)         #Y, M, D is a dummy
        self.market_close = datetime(2000, 1, 1, self.calendar.close.hour, self.calendar.close.minute, self.calendar.close.second) + timedelta(hours=6)
        self.time_format = "%H:%M:%S"
        print('Market open at {} and close at {} on {}'.format(self.market_open.strftime(self.time_format), self.market_close.strftime(self.time_format), self.date.date()))
        print('Next open: {}'.format(self.clock.next_open))
        print('Next close: {}'.format(self.clock.next_close))
        """

    def buy(self, symbol, qty, order_type, time_in_force):
        print('Buying {} qty of {} shares!'.format(qty, symbol))
        self.api.submit_order(
            symbol = symbol,
            qty = qty,
            side = 'buy',
            type = order_type,
            time_in_force = time_in_force
        )
        #buy('MSFT', 1, 'market', 'gtc')

    def sell(self, symbol, qty, order_type, time_in_force):
        print('Selling {} qty of {} shares!'.format(qty, symbol))
        self.api.submit_order(
            symbol = symbol,
            qty = qty,
            side = 'sell',
            type = order_type,
            time_in_force = time_in_force
        )
        #sell('MSFT', 1, 'market', 'opg')

    def viewOpenOrders(self):
        open_orders_list = self.api.list_orders(
            status='open',
            limit=None,
            nested=True  # show nested multi-leg orders
        )
        open_orders = [o for o in open_orders_list]
        print(open_orders)
        #viewOpenOrders()

    def run(self):
        #self.viewOpenOrders()
        #self.buy('AAPL', 1, 'market', 'gtc')

        # If the market is open
        if self.clock.is_open == True:
            pass
        

t = TradingBot()
while t.running:
    t.run()
