class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 60 分鐘
        self.period = 60 * 60
        self.options = {}

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

        # 將資料由舊到新排列
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        trade_volume_history.reverse()

        # 轉換為 np.array
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

        # 成交量最高、或者次高的幾個價格，就是壓力價或者支撐價
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
        
        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available
        
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
        
        signal = 0
        prev_close_price = close_price_history[-2]
        hold = available_base_amount > 0.1
        # 今日收盤價<昨日收盤價及跌破支撐線時
        if close_price < support and close_price < prev_close_price:
            # 如果有部位且跌下支撐線，全賣
            if hold:
                signal = -1

        # 今日收盤價>昨日收盤且衝破壓力線時
        if close_price > resistance and close_price > prev_close_price:
            if hold:
                if self.cost_basis != 0:
                    # 獲利達標，平倉
                    if ((close_price - self.cost_basis) / self.cost_basis) > self.take_profit:
                        signal = -1
                    # 未達標，繼續建倉
                    else:
                        signal = 1
            else:
                signal = 1

        # 送出訂單 - 買
        if self.last_type == 'sell' and signal == 1:
            if available_quote_amount >= self.divide_quote:
                CA.log('買入 ' + base)
                self.last_type = 'buy'
                CA.buy(exchange, pair, self.divide_quote/high_price, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif self.last_type == 'buy' and signal == -1:
            if available_base_amount > 0:
                self.last_type = 'sell'
                self.divide_quote = 0
                CA.log('賣出 ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return
