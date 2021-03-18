from iexfinance.stocks import Stock

# Enter your API Token here
token = 'pk_3d9e9a93df64463bbd5fb7fabdae81f7'

def fetch_current_price(stock_ticker):

    a = Stock(stock_ticker, token=token)
    return a.get_quote()['latestPrice'][0]
