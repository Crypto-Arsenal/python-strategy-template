class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        # 30 min
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.bias_rate = 0.5
        self.ema_period = 20
        self.proportion = 0.9


    def on_order_state_change(self,  order):
        pass
        
    def get_signal(self, c_last, c_mid, c_tail, e_last, e_mid, e_tail, cline_new, cline_old, eline_new, eline_old):
        signal = 0
        rate = self.bias_rate 
        # Granville 8 Rules
        # 1.Breakout Buy – When the price rises from the bottom and breaks the MA of tendency level, it is a buying signal.
        if eline_old == -1 and e_last >= e_mid:
            if c_mid < e_mid and c_last > e_last:
                signal = 1
        # 2.Call-back Buy – When the price goes beyond the MA and the call-back does not fall below the MA can be considered as a buying signal.
        if c_tail > e_tail and c_mid > e_mid:
            if cline_old == -1 and c_last > e_last:
                signal = 1
        # 3.Off-sell – When the price keeps rising and accumulates certain increases and starts deviating from the MA, it is a selling signal.
        if cline_old == 1 and c_mid > e_mid and np.absolute(c_mid-e_mid) > (e_mid*rate) and np.absolute(c_last - e_last) < (e_last*rate):
            signal == -1
        # 4.Fake Breakout Buy – The price falls below the MA, however, if the MA is still rising and the short-term price goes back upon the MA, it is a buying signal.
        if cline_old == -1 and c_mid < e_mid and c_last > e_last and eline_new == 1:
            signal = 1
        # 5.Breakout Sell – When the price falls from above and breaks the MA of tendency level, it is a selling signal.
        if eline_old == 1 and e_last <= e_mid and c_last < e_last:
            signal = -1
        # 6.Off-buy – When the price keeps falling and accumulates certain declines, and it begins to deviate from the moving average, it is a buying signal.
        if cline_old == -1 and c_mid < e_mid and np.absolute(e_mid - c_mid) > (e_mid * rate):
            if cline_new == 1 and np.absolute(c_last-e_last) < np.absolute(e_last*rate):
                signal = 1
        # 7.Fake Breakout Sell – The price rises and breaks the MA, however, the MA is still falling and the short-term price falls again below the MA, it is a selling signal.
        if cline_old == 1 and c_mid > e_mid and c_last < e_last and eline_new == -1:
            signal = -1
        # 8.Bounce Sell – When the price goes below the MA and it rebounds but does not exceed the MA, it is a selling signal.
        if e_tail > c_tail and e_mid > c_mid and cline_old == 1 and cline_new == -1:
            signal = -1

        return signal

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

        # get exponential moving average
        ema = talib.EMA(close_price_history, self.ema_period)

        if len(ema) < 3:
            return []

        # close price
        c_last = float(close_price_history[-1])
        c_mid = float(close_price_history[-2])
        c_tail = float(close_price_history[-3])

        # ema 
        e_last = float(ema[-1])
        e_mid = float(ema[-2])
        e_tail = float(ema[-3])

        # price trend, uptrend --> 1, downtrend --> -1
        cline_old = 1 if c_mid > c_tail else -1
        cline_new = 1 if c_last > c_mid else -1
        # ema trend, uptrend --> 1, downtrend --> -1
        eline_old = 1 if e_mid > e_tail else -1
        eline_new = 1 if e_last > e_mid else -1

        #CA.log("c_last: " + str(c_last) + " c_mid: " + str(c_mid) + " c_tail: " + str(c_tail) + " e_last: " + str(e_last) + " e_mid: " + str(e_mid))
        #CA.log("e_tail: " + str(e_tail) +  " cline_new: " + str(cline_new) + " cline_old: " + str(cline_old) +  " eline_new: " + str(eline_new) + " eline_old: " + str(eline_old))

        # trade_signal == 1 -> buy, trade_signal == -1 -> sell
        trade_signal = 0
        trade_signal = self.get_signal(c_last, c_mid, c_tail, e_last, e_mid,
                        e_tail, cline_new, cline_old, eline_new, eline_old)
        
        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # place buy order
        if self.last_type == 'sell' and trade_signal == 1:
            amount = np.around((available_quote_amount /  close_price_history[-1]) * self.proportion, 5)
            if available_quote_amount >= amount * close_price_history[-1]:
                CA.log('Buy ' + base)
                self.last_type = 'buy'
                CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
       
        
        # place sell order
        elif self.last_type == 'buy' and trade_signal == -1:
            if available_base_amount > 0:
                CA.log('Sell ' + base)
                self.last_type = 'sell'
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
        
        return

    
