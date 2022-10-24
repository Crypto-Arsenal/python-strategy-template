class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 60 * 60
        self.options = {}

        self.divide_quote = 0
        self.proportion = 0.2


    def on_order_state_change(self,  order):
        pass

    # called every self.period
    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        open_price_history = [candle['open'] for candle in candles[exchange][pair]]

        # convert to chronological order for talib
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        open_price_history.reverse()

        # convert to np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        open_price_history = np.array(open_price_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        hammer = talib.CDLHAMMER(open_price_history, high_price_history, low_price_history, close_price_history)[-1]
        hangingman = talib.CDLHANGINGMAN(open_price_history, high_price_history, low_price_history, close_price_history)[-1]

        signal = 0
        # hammer candlestick pattern
        if hammer > 0:
            signal = 1
        
        # hangingman candle stick pattern
        if hangingman < 0:
            signal = -1

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
        
        # place buy order
        if signal == 1:
            amount = self.divide_quote/high_price 
            if available_quote_amount >= amount * close_price:
                CA.log('Buy ' + base)
                CA.buy(exchange, pair, amount, CA.OrderType.MARKET)

        # place sell order
        elif signal == -1:
            if available_base_amount > 0.00001:
                self.divide_quote = 0
                CA.log('Sell ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return
