class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.fast_period = 12
        self.slow_period = 26
        self.signal_period = 9
        self.proportion = 0.9
 

    def on_order_state_change(self,  order):
        pass

    # called every self.period
    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]

        # convert to chronological order for talib
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()

        # convert np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)

        if len(close_price_history) < 2:
            return []

        # get macd from talib
        macd, macdsignal, macdhist = talib.MACD(close_price_history, fastperiod=self.fast_period, slowperiod=self.slow_period, signalperiod=self.signal_period)
        
        curr_macd = macdhist[-1]
        prev_macd = macdhist[-2]

        macd_now = macd[-1]
        signal_now = macdsignal[-1]

        signal = 0
        # MACD crosses the zero line from below - buy signal
        if prev_macd < 0 and curr_macd > 0:
            signal = 1
        
        # MACD crosses the zero line from above - sell signal
        elif prev_macd > 0 and curr_macd < 0:
            signal = -1

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # place buy order
        if self.last_type == 'sell' and signal == 1:
            amount = np.around((available_quote_amount /  close_price_history[-1]) * self.proportion, 5)
            CA.log('Buy ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
           
        # place sell order
        elif self.last_type == 'buy' and signal == -1:
            CA.log('Sell ' + base)
            self.last_type = 'sell'
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
        
        return
