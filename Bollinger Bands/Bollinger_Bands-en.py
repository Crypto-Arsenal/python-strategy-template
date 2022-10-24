class Strategy(StrategyBase):

    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.ma_period = 20
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

        upper, middle, lower = talib.BBANDS(close_price_history)
        ma = talib.SMA(close_price_history, self.ma_period)

        if len(ma) < 2 or len(upper) < 2:
            return []

        # moving average
        ma_curr = ma[-1]
        ma_prev = ma[-2]

        # bollinger band upper band
        upper_curr = upper[-1]
        upper_prev = upper[-2]

        # bollinger band lower band
        lower_curr = lower[-1]
        lower_prev = lower[-2]

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        # buy if signal is 1, sell if it's 2, sell short if it's -1, buy to cover if it's -2
        signal = 0
        amount = self.divide_quote/high_price

        # up trend
        if ma_curr > ma_prev and upper_curr > upper_prev and lower_curr > lower_prev:
            
            # open long position
            if available_base_amount< amount and available_base_amount > -amount:
                signal = 1

        # exceeds upper bound -- close position
        elif high_price_history[-1] > upper_curr:
            if available_base_amount > amount:
                signal = 2
                amount = available_base_amount
        
        # down trend
        elif ma_curr < ma_prev and upper_curr < upper_prev and lower_curr < lower_prev:
            
            # open short position
            if available_base_amount < amount and available_base_amount > -amount:
                signal = -1
            
            # if holding long position, sell one unit
            elif available_base_amount > amount:
                signal = 2
                if available_base_amount < amount:
                    amount = available_base_amount
        
        # drops below lower bound -- close position
        elif low_price_history[-1] < lower_curr:
            if available_base_amount < -amount:
                signal = -2
                amount = -available_base_amount
        
        # Sell short
        if signal == -1:
            self['is_shorting'] = 'true'
            amount = -amount * 1.1
            self.divide_quote = 0
            CA.log('Sell short ' + str(base))
            return [
                {
                    'exchange': exchange,
                    'amount': amount,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                    'margin': True,
                }
            ]

        # Buy to cover
        elif signal == -2:
            self['is_shorting'] = 'true'
            CA.log('Buy to cover ' + str(base))
            return [
                {
                    'exchange': exchange,
                    'amount': amount,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                    'margin': True,
                }
            ]

         
        # place buy order
        elif signal == 1:
            amount = amount * 1.1
            self['is_shorting'] = 'false'
            CA.log('Buy ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            
        # place sell order
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.last_type = 'sell'
            self.divide_quote = 0
            CA.log('Sell ' + base)
            CA.sell(exchange, pair, amount, CA.OrderType.MARKET)

        return 
