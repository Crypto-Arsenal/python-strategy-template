class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
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

    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]

        # 將資料由舊到新排列
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()

        # 轉換為 np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        rsi_short = talib.RSI(close_price_history, self.short_period)
        rsi_long = talib.RSI(close_price_history, self.long_period)
        
        if len(close_price_history) < self.long_period + 1:
            return []
        
        # 短週期的RSI 
        curr_rsi_short = rsi_short[-1]
        # 長週期的RSI
        curr_rsi_long = rsi_long[-1]

        # 上一個時間點的短&長週期RSI
        prev_rsi_short = rsi_short[-2]
        prev_rsi_long = rsi_long[-2]

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        # signal = 1 則買, 2 則賣, -1 賣空, -2 空單回補
        signal = 0
        
        # 空倉建立部位
        if available_base_amount< self.divide_quote/high_price and available_base_amount > -self.divide_quote/high_price:
            if curr_rsi_short > curr_rsi_long and prev_rsi_short < prev_rsi_long:
                signal = 1
            if curr_rsi_short < curr_rsi_long and prev_rsi_short > prev_rsi_long:
                signal = -1

        # 持有多頭部位，空頭平倉
        elif available_base_amount > self.divide_quote/high_price:
            if curr_rsi_short < curr_rsi_long and prev_rsi_short > prev_rsi_long:
                signal = 2
            if curr_rsi_short >  self.rsi_upper_band:
                signal = 2

        # 持有空頭部位，多頭平倉
        elif available_base_amount < -self.divide_quote/high_price:
            if curr_rsi_short > curr_rsi_long and prev_rsi_short < prev_rsi_long:
                signal = -2
            if curr_rsi_short < self.rsi_lower_band:
                signal = -2
            
        # 送出訂單 - 賣空
        if signal == -1:
            self['is_shorting'] = 'true'
            CA.log('賣空 ' + str(base))
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

        # 送出訂單 - 空單回補
        elif signal == -2:
            self['is_shorting'] = 'true'
            self.divide_quote = 0
            CA.log('空單回補 ' + str(base))
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

         
        # 送出訂單 - 買
        elif signal == 1:
            self['is_shorting'] = 'false'
            CA.log('買入 ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, self.divide_quote/high_price*1.1, CA.OrderType.MARKET)
            
        # 送出訂單 - 賣
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.last_type = 'sell'
            self.divide_quote = 0
            CA.log('賣出 ' + base)
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
