class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 60 * 60
        self.options = {}
        self.range_val = 21
        self.first_max = 0
        self.first_min = 0
        self.neckline = 0
        self.double_bottom = False
        self.base_price = 0
        self.divide_quote = 0
        self.proportion = 0.9
        self.profit_gain = 0.01 # gain 1%


    def check_value(self, data, midValue, compare):
        data = np.array(data)
        p1 = data[0 : len(data) // 2]
        p2 = data[len(data) // 2 + 1: ]

        if compare == '>':
            if len([i for i in p1 if midValue < i]) > 0: # compare with the in front of mid meaning it's not the max
                return False
            if len([i for i in p2 if midValue <= i]) > 0: # compare with the ones after mid meaning it's not the max
                return False
        else:
            if len([i for i in p1 if midValue > i]) > 0: # compare with the in front of mid meaning it's not the min
                return False
            if len([i for i in p2 if midValue >= i]) > 0: # compare with the in front of mid meaning it's not the min
                return False

        return True


    def on_order_state_change(self,  order):
        self.base_price = order["price"]

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
        if len(close_price_history) < (self.range_val):
            return []

        high_window = high_price_history[-self.range_val:]
        low_window = low_price_history[-self.range_val:]

        max_high = high_window[self.range_val // 2]
        min_low = low_window[self.range_val // 2]
        
        if self.double_bottom == False:
            if self.check_value(high_window, max_high, '>'):

                # the first high point
                if self.first_max == 0:
                    self.first_max = max_high
                    
                # if the original high point is not the max, then no w pattern
                elif self.first_max < max_high:
                    self.first_max = max_high
                    self.first_min = 0
                    self.neckline = 0

                # the first high point already exists and the new high point <= the first high point. set this as the neckline value
                else:
                    self.neckline = max_high

            if self.check_value(low_window, min_low, '<') and self.first_max != 0:

                # high points already exist, set the low point
                if self.first_min == 0:
                    self.first_min = min_low
                elif self.neckline == 0:
                    if self.first_min <= min_low:
                        self.first_min = min_low

                # if the original low point is not the min, then no w pattern
                elif min_low < self.first_min:
                    self.first_max = 0
                    self.first_min = 0
                    self.neckline = 0
                
                # low point, neckline value all exist and new low point >= the first low point
                else:
                    self.double_bottom = True
                    
        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # signal = 1 then buy, signal = -1 then sell
        signal = 0        
        if self.double_bottom:
            curr_close = close_price_history[-1]
            # price goes above neckline
            if curr_close > self.neckline:
                # open position
                if available_base_amount >= -0.0001 and available_base_amount <= 0.0001: 
                    signal = 1

                # already holding position
                elif available_base_amount > 0.0001:
                    if self.base_price != 0:
                        # sell if the profit is over 1%
                        if (curr_close - self.base_price) / self.base_price > self.profit_gain:
                            signal = -1
                        else:
                            signal = 1
           
            # price goes below neckline
            else:
                self.double_bottom = False
                if available_base_amount > 0.0001:
                    signal = -1

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        # place buy order
        if signal == 1:
            if available_quote_amount >= self.divide_quote:
                CA.log('Buy ' + base)
                CA.buy(exchange, pair, self.divide_quote/high_price, CA.OrderType.MARKET)

        # place sell order
        elif signal == -1:
            if available_base_amount > 0.0001:
                CA.log('Sell ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
                self.divide_quote = 0
                self.double_bottom = False
                self.first_max = 0
                self.first_min = 0
                self.neckline = 0
        return
