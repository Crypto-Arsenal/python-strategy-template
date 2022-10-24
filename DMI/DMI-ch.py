class Strategy(StrategyBase):

    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 30 分鐘
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        self.time_period = 14
        self.adx_bound = 25
        self.proportion = 0.9

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
        
        # 正DI
        pdi = talib.PLUS_DI(high_price_history, low_price_history, close_price_history, timeperiod=self.time_period)
        # 負DI
        mdi = talib.MINUS_DI(high_price_history, low_price_history, close_price_history, timeperiod=self.time_period)
        # 趨向平均線 (ADX)
        adx = talib.ADX(high_price_history, low_price_history, close_price_history, timeperiod=self.time_period)

        if len(pdi) < 2:
            return

        # 最新指標
        curr_pdi = pdi[-1]
        curr_mdi =mdi[-1]
        curr_adx = adx[-1]

        # 上一個時間點的指標
        prev_pdi = pdi[-2]
        prev_mdi = mdi[-2]

        # signal = 1 則買, signal = -1 則賣
        signal = 0

        if curr_adx > self.adx_bound:
            if curr_pdi > curr_mdi and prev_pdi < prev_mdi:
                signal = 1

            if curr_pdi < curr_mdi and prev_pdi > prev_mdi:
                signal = -1

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # 送出訂單 - 買
        if self.last_type == 'sell' and signal == 1:
            amount = np.around((available_quote_amount /  close_price_history[-1]) * self.proportion, 3)
            if available_quote_amount >= amount * close_price_history[-1]:
                self.last_type = 'buy'
                CA.buy(exchange, pair, amount, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif self.last_type == 'buy' and signal == -1:
            if available_base_amount > 0:
                self.last_type = 'sell'
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
        
        return
