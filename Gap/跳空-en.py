class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 15 * 60
        self.options = {}

        self.jump_percent = 0
        self.fetch_records = 2
        self.stop_loss = 0.05
        self.base = 0
        self.accumulate = 0
        self.limit_no = 1
        self.proportion = 0.2
        self.divide_quote = 0

    def on_order_state_change(self,  order):
        pass

    # called every self.period
    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        open_price_history = [candle['open'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        trade_volume_history = [candle['volume'] for candle in candles[exchange][pair]]

        # convert to chronological order for talib
        close_price_history.reverse()
        open_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        trade_volume_history.reverse()

        # convert np.array
        close_price_history = np.array(close_price_history)
        open_price_history = np.array(open_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        trade_volume_history = np.array(trade_volume_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        if len(close_price_history) < self.fetch_records :
            return []

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # calculate amount with 20% of available asset
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        high_base = high_price_history[-2]
        high_jump = high_base * self.jump_percent
        low_base = low_price_history[-2]
        low_jump = low_base * self.jump_percent

        signal = 0
       # not holding any position
        if available_base_amount < self.divide_quote/high_price and available_base_amount > (-1 * self.divide_quote/high_price):
           
           # buy
            if open_price_history[-1] > (high_base + high_jump):
               signal = 1
               self.base = high_base

            # short
            elif open_price_history[-1] < (low_base - low_jump):
                signal = -1
                self.base = low_base

        # holding long positions
        elif available_base_amount > self.amount:
            
            # current close price is lower than that of in previous timestamp (accumulated x times)
            if close_price_history[-1] < close_price_history[-2]:
                self.accumulate = self.accumulate + 1

            if self.accumulate == self.limit_no:
                signal = 2
                self.accumulate = 0

            # stop loss
            elif close_price_history[-1] < self.base * (1 - self.stop_loss):
                signal = 2
                self.accumulate = 0

        # holding short positions
        elif available_base_amount < -self.amount:

            # current close price is higher than that of in previous timestamp (accumulated x times)
            if close_price_history[-1] > close_price_history[-2]:
                self.accumulate = self.accumulate + 1

            if self.accumulate == self.limit_no:
                signal = -2
                self.accumulate = 0
                
            # stop loss
            elif close_price_history[-1] > self.base * (1 + self.stop_loss):
                signal = -2
                self.accumulate = 0
      
        # Sell short
        if signal == -1:
            self['is_shorting'] = 'true'
            amount = -self.divide_quote/high_price * 1.1
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
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            
        # place sell order
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.divide_quote = 0
            CA.log('Sell ' + base)
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
