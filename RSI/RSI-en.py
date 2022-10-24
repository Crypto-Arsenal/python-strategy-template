class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.short_period = 5
        self.long_period = 10
        self.divide_quote = 0
        self.proportion = 0.2

        self.rsi_upper_band = 80
        self.rsi_lower_band = 20


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

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        rsi_short = talib.RSI(close_price_history, self.short_period)
        rsi_long = talib.RSI(close_price_history, self.long_period)
        
        if len(close_price_history) < self.long_period + 1:
            return []
        
        # current rsi, short and long period respectively
        curr_rsi_short = rsi_short[-1]
        curr_rsi_long = rsi_long[-1]

        # previous time stamp rsi
        prev_rsi_short = rsi_short[-2]
        prev_rsi_long = rsi_long[-2]

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        # initialize signal to be 0
        signal = 0
        if available_base_amount< self.divide_quote/high_price and available_base_amount > -self.divide_quote/high_price:
            # open long position
            if curr_rsi_short > curr_rsi_long and prev_rsi_short < prev_rsi_long:
                signal = 1
            # open short position
            if curr_rsi_short < curr_rsi_long and prev_rsi_short > prev_rsi_long:
                signal = -1

        # holding long position 
        elif available_base_amount > self.divide_quote/high_price:
            if curr_rsi_short < curr_rsi_long and prev_rsi_short > prev_rsi_long:
                signal = 2
            if curr_rsi_short >  self.rsi_upper_band:
                signal = 2

        # holding short position
        elif available_base_amount < -self.divide_quote/high_price:
            if curr_rsi_short > curr_rsi_long and prev_rsi_short < prev_rsi_long:
                signal = -2
            if curr_rsi_short < self.rsi_lower_band:
                signal = -2
            
        # Sell short
        if signal == -1:
            self['is_shorting'] = 'true'
            CA.log('Sell short ' + str(base))
            return [
                {
                    'exchange': exchange,
                    'amount': -self.divide_quote/high_price*1.1,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                    'margin': True,
                }
            ]

        # Buy to cover
        elif signal == -2:
            amount = -available_base_amount
            self['is_shorting'] = 'true'
            self.divide_quote = 0
            CA.log('Buy to cover ' + str(base))
            return [
                {
                    'exchange': exchange,
                    'amount': -available_base_amount,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                    'margin': True,
                }
            ]

        # place buy order
        elif signal == 1:
            self['is_shorting'] = 'false'
            CA.log('Buy ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, self.divide_quote/high_price*1.1, CA.OrderType.MARKET)
            
        # place sell order
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.divide_quote = 0
            CA.log('Sell ' + base)
            self.last_type = 'sell'
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
