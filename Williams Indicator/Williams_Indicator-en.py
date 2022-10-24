class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.trade_rate = 0
        self.trade_volume = 0
        self.volume_rate_value = 0.5
        self.williams_period = 14
        self.sma_period = 5
        self.williams_upper = 80
        self.williams_lower = 20
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

        trade_volume = candles[exchange][pair][0]['volume']

        # get williams indicator        
        willr = talib.WILLR(high_price_history, low_price_history, close_price_history, timeperiod = self.williams_period)
        # get simple moving average
        ma_short = talib.SMA(close_price_history, self.sma_period)
       
        if len(ma_short) < 2:
            return []
        
        wr = -1 * willr[-1]
        ma = ma_short[-2]
        volume_rate = trade_volume / ma
        
        # buy, signal = 1, sell, signal = -1
        signal = 0

        if wr > self.williams_upper and volume_rate > self.volume_rate_value:
            signal = 1
            
        elif wr < self.williams_lower and volume_rate > self.volume_rate_value:
            signal = -1
        
         # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        amount = np.around((available_quote_amount /  close_price_history[-1]) * self.proportion, 2)

        # place buy order
        if self.last_type == 'sell' and signal == 1:
            CA.log('Buy ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)

        # place sell order
        elif self.last_type == 'buy' and signal == -1:
            CA.log('Sell ' + base)
            self.last_type = 'sell'
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return
