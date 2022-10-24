class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 15 分鐘
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

    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        open_price_history = [candle['open'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        trade_volume_history = [candle['volume'] for candle in candles[exchange][pair]]

        # 將資料由舊到新排列
        close_price_history.reverse()
        open_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        trade_volume_history.reverse()

        # 轉換為 np.array
        close_price_history = np.array(close_price_history)
        open_price_history = np.array(open_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        trade_volume_history = np.array(trade_volume_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        if len(close_price_history) < self.fetch_records :
            return []

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # 用2成資產計算amount
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        high_base = high_price_history[-2]
        high_jump = high_base * self.jump_percent
        low_base = low_price_history[-2]
        low_jump = low_base * self.jump_percent

        signal = 0
       # 手上無部位
        if available_base_amount < self.divide_quote/high_price and available_base_amount > (-1 * self.divide_quote/high_price):
           
           # 今日開盤跳多,買進
            if open_price_history[-1] > (high_base + high_jump):
               signal = 1
               self.base = high_base

            # 今日開盤跳空,放空
            elif open_price_history[-1] < (low_base - low_jump):
                signal = -1
                self.base = low_base

        # 手上有多頭部位,只考慮空頭平倉
        elif available_base_amount > self.amount:
            
            # 今日收盤低於昨日收盤 (累積Ｘ次)
            if close_price_history[-1] < close_price_history[-2]:
                self.accumulate = self.accumulate + 1

            if self.accumulate == self.limit_no:
                signal = 2
                self.accumulate = 0

            # 停損
            elif close_price_history[-1] < self.base * (1 - self.stop_loss):
                signal = 2
                self.accumulate = 0

        # 手上有空頭部位,只考慮多頭平倉
        elif available_base_amount < -self.amount:

            # 今日收盤高於昨日收盤 (累積Ｘ次)
            if close_price_history[-1] > close_price_history[-2]:
                self.accumulate = self.accumulate + 1

            if self.accumulate == self.limit_no:
                signal = -2
                self.accumulate = 0
                
            # 停損
            elif close_price_history[-1] > self.base * (1 + self.stop_loss):
                signal = -2
                self.accumulate = 0
      
        # 送出訂單 - 賣空
        if signal == -1:
            self['is_shorting'] = 'true'
            amount = -self.divide_quote/high_price * 1.1
            CA.log('賣空 ' + str(base))
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

        # 送出訂單 - 空單回補
        elif signal == -2:
            amount = -available_base_amount
            self['is_shorting'] = 'true'
            self.divide_quote = 0
            CA.log('空單回補 ' + str(base))
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

         
        # 送出訂單 - 買
        elif signal == 1:
            amount = self.divide_quote/high_price * 1.1
            self['is_shorting'] = 'false'
            CA.log('買入 ' + base)
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            
        # 送出訂單 - 賣
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.divide_quote = 0
            CA.log('賣出 ' + base)
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
