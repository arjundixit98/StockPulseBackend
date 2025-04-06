import yfinance as yf


def get_stock_hist_data(ticker, timeframe="1y"):
    '''
    Returns stock data + historical data for the provided timeframe for a single ticker
    '''
    if timeframe.lower()[-1]=='m':
        timeframe=timeframe+'o'
        
    hist_data = []
    stock = yf.Ticker(ticker)
    last_year_hist = stock.history(period=timeframe.lower(), interval="1d")
    time_series_closes = last_year_hist['Close'].to_dict()
    for (ts,close) in time_series_closes.items():
        hist_data.append({'date': ts.isoformat().split('T')[0], 'price': close})

    print(timeframe)

    return  get_stock_data(ticker) | {"chartData" : hist_data}
  


def get_stocks_hist_data(tickers):
    '''
    Returns list of objects each having ticker, current_price and day % change in JSON when tickers are provided as list
    '''
    
    print(tickers)
    data = []
    for ticker in tickers:
        stock_data = get_stock_hist_data(ticker)
        data.append(stock_data)

    return data



def get_stock_data_from_object(ticker, stock):
    '''
    Returns ticker, current_price and day % change in JSON when ticker is passed as input
    '''

    latest_close = stock.info.get('regularMarketPrice',1)
    prev_close = stock.info.get('previousClose',1)
    percent_change = ((latest_close - prev_close) / prev_close) * 100


    return {
        "symbol": ticker,
        "currentPrice": round(latest_close,2),
        "prevClose": round(prev_close,2),
        "changePercentage": round(percent_change, 2),
        "name" : stock.info.get('longName',None) or ticker,
        "weekHigh52": round(stock.info.get('fiftyTwoWeekHigh',0),2),
        "weekLow52": round(stock.info.get('fiftyTwoWeekLow',0),2),
        "sector": stock.info.get('sector',None),
        "change": round(latest_close,2) - stock.info.get('previousClose',0),
        "pe": round(stock.info.get('forwardPE',0),2),
        "downFrom52WeekHigh": round(stock.info.get('fiftyTwoWeekHigh',0),2) -  round(latest_close,2),

    }

def get_stock_data(ticker):
    '''
    Returns ticker, current_price and day % change in JSON when ticker is passed as input
    '''
    stock = yf.Ticker(ticker)

    latest_close = stock.info.get('regularMarketPrice',1)
    prev_close = stock.info.get('previousClose',1)
    percent_change = ((latest_close - prev_close) / prev_close) * 100


    return {
        "symbol": ticker,
        "currentPrice": round(latest_close,2),
        "prevClose": round(prev_close,2),
        "changePercentage": round(percent_change, 2),
        "name" : stock.info.get('longName',None) or ticker,
        "weekHigh52": round(stock.info.get('fiftyTwoWeekHigh',0),2),
        "weekLow52": round(stock.info.get('fiftyTwoWeekLow',0),2),
        "sector": stock.info.get('sector',None),
        "change": round(latest_close,2) - stock.info.get('previousClose',0),
        "pe": round(stock.info.get('forwardPE',0),2),
        "downFrom52WeekHigh": round(stock.info.get('fiftyTwoWeekHigh',0),2) -  round(latest_close,2),
        

    }

def get_stocks_data(tickers_list):
    '''
    Returns list of objects each having ticker, current_price and day % change in JSON when tickers are provided as list
    '''
    
    print(tickers_list)
    data = []
    tickers_query = ' '.join(tickers_list)
    tickers = yf.Tickers(tickers_query)
    
    for ticker in tickers_list:
        tickerObj = tickers.tickers[ticker]
        data.append(get_stock_data_from_object(ticker, tickerObj))

    return data
    # data = []
    # for ticker in tickers:
    #     stock_data = get_stock_data(ticker)
    #     data.append(stock_data)

    # return data

#print(get_stock_data('TITAN.NS'))