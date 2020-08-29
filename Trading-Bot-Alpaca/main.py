import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
from config import *

api = tradeapi.REST(API_KEY, API_SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Check if the market is open now.
clock = api.get_clock()
print('The market is {}'.format('open.' if clock.is_open else 'closed.'))

# Check when the market opens and close today.
date = datetime.now()
calendar = api.get_calendar(start=date, end=date)[0]
market_open = datetime(2000, 1, 1, calendar.open.hour, calendar.open.minute, calendar.open.second) + timedelta(hours=6)         #Y, M, D is a dummy
market_close = datetime(2000, 1, 1, calendar.close.hour, calendar.close.minute, calendar.close.second) + timedelta(hours=6)
time_format = "%H:%M:%S"
print('Market open at {} and close at {} on {}.'.format(market_open.strftime(time_format), market_close.strftime(time_format), date.date()))


class TradingBot:
    def __init__(self):
        pass
    
    def run(self):
        pass


def create_order(symbol, qty, order_type, time_in_force):
    print('Buying {} qty of {} shares!'.format(qty, symbol))
    api.submit_order(
        symbol = symbol,
        qty = qty,
        side = 'buy',
        type = order_type,
        time_in_force = time_in_force
    )
#create_order('MSFT', 1, 'market', 'gtc')

def sell_order(symbol, qty, order_type, time_in_force):
    print('Selling {} qty of {} shares!'.format(qty, symbol))
    api.submit_order(
        symbol = symbol,
        qty = qty,
        side = 'sell',
        type = order_type,
        time_in_force = time_in_force
    )
#sell_order('MSFT', 1, 'market', 'opg')

def view_open_orders():
    open_orders_list = api.list_orders(
        status='open',
        limit=None,
        nested=True  # show nested multi-leg orders
    )
    open_orders = [o for o in open_orders_list]
    print(open_orders)
#view_open_orders()
