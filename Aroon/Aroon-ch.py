class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        self.period = 45 * 60
        self.options = {}

        self.divide_quote = 0
        self.proportion = 0.2
        self.aroon_period = 14

    def on_order_state_change(self,  order):
        pass

    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        open_price_history = [candle['open'] for candle in candles[exchange][pair]]

        # 將資料由舊到新排列
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        open_price_history.reverse()

        # 轉換為 np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        open_price_history = np.array(open_price_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        aroondown, aroonup = talib.AROON(high_price_history, low_price_history, timeperiod=self.aroon_period)
        aroon_down = aroondown[-1]
        aroon_up = aroonup[-1]

        signal = 0
        # 阿隆上線大於 50，同時阿隆上線大於阿隆下線 -- 上漲趨勢
        if aroon_up > 50 and aroon_up > aroon_down:
            signal = 1

        # 阿隆下線大於 50，同時阿隆下線大於阿隆上線 -- 下跌趨勢
        elif aroon_down > 50 and aroon_down > aroon_up:
            signal = -1

        # 送出訂單 - 買
        if signal == 1:
            amount = self.divide_quote/high_price
            if available_quote_amount >= amount * close_price:
                CA.log('買入 ' + base)
                CA.buy(exchange, pair, amount, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif signal == -1:
            if available_base_amount > 0.00001:
                self.divide_quote = 0
                CA.log('賣出 ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
        return 
