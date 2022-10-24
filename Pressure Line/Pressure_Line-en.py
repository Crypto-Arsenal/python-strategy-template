class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 60 * 60
        self.options = {}

        self.last_type = 'sell'
        self.buy_price = 0
        self.region = 10
        self.collect_region = 10
        self.volumes = {-0.01 : 1}
        self.record_num = 10
        self.pressure_line = []
        self.up_pline = None
        self.down_pline = None
        self.multiplier = 80
        self.amount = 0
        self.proportion = 0.2

    def on_order_state_change(self,  order):
        pass

    def compress(self, line_list, interval):
        """merge pressure lines

        if the distance between two pressure line is smaller than interval, then merge them into one
        continue to merge till distances between any two pressure lines are greater than interval

        """
        circle = 1
        # pressure lines are already sorted 
        # check distance between any two and merge them if smaller than interval
        while(circle==1):
            new_line_list = []
            append = 0
            circle = 0
            # if the circle variable is not triggered, then it'll jump out of the while loop after the for loop finishes
            for i in range(len(line_list)-1):
                if np.absolute(line_list[i]-line_list[i+1]) <= interval:
                    new_line_list.append((line_list[i] + line_list[i+1]) / 2)
                    append = 1
                    circle = 1          # trggers merge
                else:
                    if append==1:
                        append = 0
                    else:
                        new_line_list.append(line_list[i])
            if append==0:
                new_line_list.append(line_list[-1])
            line_list = new_line_list
        return new_line_list

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

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if len(close_price_history) < self.record_num :
            return []

        # calculate amount with 20% of available asset
        if self.amount == 0:
            self.amount = np.round((available_quote_amount / close_price) * self.proportion, 5)
        
        record_price = close_price_history[-1] // (self.collect_region * self.collect_region)
        if record_price in self.volumes:
            self.volumes[record_price] = self.volumes[record_price] + trade_volume_history[-1]
        else:
            self.volumes[record_price] = trade_volume_history[-1]

        sort_dict = sorted(self.volumes.items(), key = lambda v: v[1])
        max_volume = sort_dict[-1][1]
        self.pressure_line = [k+(self.collect_region/2) for k, v in self.volumes.items() if v >= max_volume * 0.8]
        
        if len(self.pressure_line) == 0:
            return []
        
        self.pressure_line.sort()
        self.pressure_line = self.compress(self.pressure_line, self.collect_region)
        current_price = close_price_history[-1]
        
        # determine between which two pressure lines the current price is located at
        for i in range(len(self.pressure_line)):
            if current_price <= self.pressure_line[i] * self.multiplier:
                if i == 0:
                    # located below the min pressure line
                    self.up_pline = self.pressure_line[i]* self.multiplier
                    self.down_pline = None
                else:
                    self.up_pline = self.pressure_line[i]* self.multiplier
                    self.down_pline = self.pressure_line[i-1]* self.multiplier
                break
            
            else:
                # located above the mac pressure line
                self.up_pline = None
                self.down_pline = self.pressure_line[i]* self.multiplier

        # take profit -- half of the distance between two pressure lines
        # stop loss -- a quarter of the distance between two pressure lines
        if self.up_pline and self.down_pline:       # both pressure lines exist
            
            # distance between the two pressure lines is too small
            distance = np.absolute(self.up_pline - self.down_pline)
            if distance < self.region * 2:
                return []
            else:
                self.distance = distance
        
        # one pressure line is None
        else:
            self.distance = 50  
        
        signal = 0
        prev_price = close_price_history[-2]
        
        # not holding any positions 
        if self.buy_price == 0:
            
            # for upper pressure line, determine 1. whether previous price is within the region and 2. whether current price crosses the region
            if self.up_pline:
                if (self.up_pline - self.region) < prev_price <(self.up_pline + self.region):
                    # enters the region and crosses downward and does not break through upper pressure line
                    if current_price <= (self.up_pline - self.region):
                        signal = -1
                    # enters the region and crosses above the upper pressure line
                    elif current_price >= (self.up_pline + self.region):
                        signal = 1
            
            # for lower pressure line, determine 1. whether previous price is within the region and 2. whether current price crosses the region
            if self.down_pline:
                if (self.down_pline - self.region) < prev_price < (self.down_pline + self.region):
                    # enters the region and crosses below the lower pressure line
                    if current_price <= (self.down_pline - self.region):
                        signal = -1
                    # enters the region and crosses above the upper pressure line
                    elif current_price >= (self.down_pline + self.region):
                        signal = 1
        
        # holding positions 
        # determine whether to take profit or stop loss
        else:
            # calculate profit
            if available_base_amount > 0.5:
                profit = current_price - self.buy_price
            else:
                profit = self.buy_price - current_price

            if profit > (self.distance/2) or profit < -(self.distance/4):
                signal = -1 + 2 * (1 - (available_base_amount > 0.5))

        # place buy order
        if signal == 1 and available_quote_amount > (close_price * self.amount):
            self.last_type = 'buy'
            CA.log('Buy ' + base)
            self.buy_price = close_price
            CA.buy(exchange, pair, self.amount, CA.OrderType.MARKET)

        # place sell order
        elif signal == -1 and available_base_amount > 0:
            self.last_type = 'sell'
            CA.log('Sell ' + base)
            CA.sell(exchange, pair, self.amount * 0.999, CA.OrderType.MARKET)
        
        return
