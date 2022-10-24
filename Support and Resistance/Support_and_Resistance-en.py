class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 60 * 60
        self.options = {}

        # user defined class attribute
        self.last_type = 'sell'

        self.close_price_trace = np.array([])
        self.high_price_trace = np.array([])
        self.low_price_trace = np.array([])
        self.trade_volume_trace = np.array([])

        self.long_period = 10
        self.take_profit = 0.03
        self.divide_quote = 0
        self.proportion = 0.2
        self.cost_basis = 0


    def on_order_state_change(self,  order):
        if self.cost_basis == 0:
            self.cost_basis = order['price']
        if order['amount'] < 0:
            self.cost_basis = 0

    # called every self.period
    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        trade_volume_history = [candle['volume'] for candle in candles[exchange][pair]]

        # convert to chronological order for talib
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        trade_volume_history.reverse()

        # convert np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        trade_volume_history = np.array(trade_volume_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        if len(close_price_history) < self.long_period :
            return []

        volume_recent = trade_volume_history[-self.long_period: ]
        close_price_recent = close_price_history[-self.long_period: ]

        # the prices with the highest and second highest trade volume are the support or resistance level
        max_index = np.argmax(volume_recent)
        res1 = close_price_recent[max_index]
        
        volume_recent = np.delete(volume_recent, max_index)
        close_price_recent = np.delete(close_price_recent, max_index)
        max_index = np.argmax(volume_recent)
        res2 = close_price_recent[max_index]

        if res1 < res2:
            resistance = res2
            support = res1
        else:
            resistance = res1
            support = res2
        
        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available
        
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
        
        signal = 0
        prev_close_price = close_price_history[-2]
        hold = available_base_amount > 0.1
        # current close price is lower than previous close price and it drops below the support line
        if close_price < support and close_price < prev_close_price:
            # if holding positions, sell all positions
            if hold:
                signal = -1

        # current close price is higher than previous close price and it breaks through the pressure line
        if close_price > resistance and close_price > prev_close_price:
            if hold:
                if self.cost_basis != 0:
                    # reaches the take profit point
                    if ((close_price - self.cost_basis) / self.cost_basis) > self.take_profit:
                        signal = -1
                    # haven't reached the take profit point
                    else:
                        signal = 1
            else:
                signal = 1

        # place buy order
        if self.last_type == 'sell' and signal == 1:
            if available_quote_amount >= self.divide_quote:
                CA.log('Buy ' + base)
                self.last_type = 'buy'
                CA.buy(exchange, pair, self.divide_quote/high_price, CA.OrderType.MARKET)

        # place sell order
        elif self.last_type == 'buy' and signal == -1:
            if available_base_amount > 0:
                self.last_type = 'sell'
                self.divide_quote = 0
                CA.log('Sell ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return
