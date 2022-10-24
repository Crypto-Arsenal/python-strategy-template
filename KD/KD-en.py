class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.kd_bound = 50
        self.divide_quote = 0
        self.target_amount = 0
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

        slowk, slowd = talib.STOCH(high_price_history, low_price_history, close_price_history)

        if len(slowk) < 2 or len(slowd) < 2:
            return

        curr_k = slowk[-1]
        curr_d = slowd[-1]

        prev_k = slowk[-2]
        prev_d = slowd[-2]

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
        
        # initialize signal to be 0
        signal = 0
        if available_base_amount< self.divide_quote/high_price  and available_base_amount > -self.divide_quote/high_price :
            # up trend
            if curr_k > self.kd_bound:
                # open long position
                # %K line crosses above %D line
                if curr_k > curr_d and prev_k < prev_d:
                    signal = 1
            # down trend
            else:
                # open short position
                # %D line crosses above %K ling
                if curr_k < curr_d and prev_k > prev_d:
                    signal = -1

        # holding long position
        elif available_base_amount > self.divide_quote/high_price :
            # %D line crosses above %K ling
            if curr_k < curr_d and prev_k > prev_d:
                signal = 2

        # holding short position
        elif available_base_amount < -self.divide_quote/high_price:
            # %K line crosses above %D line
            if curr_k > curr_d and prev_k < prev_d:
                signal = -2


        # Sell short
        if signal == -1:
            amount = -self.divide_quote/high_price * 1.1
            self['is_shorting'] = 'true'
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
            amount = -available_base_amount
            self['is_shorting'] = 'true'
            self.divide_quote = 0
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
            amount = self.divide_quote/high_price * 1.1
            self['is_shorting'] = 'false'
            CA.log('Buy ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            
        # place sell order
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.divide_quote = 0
            CA.log('Sell ' + base)
            self.last_type = 'sell'
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
