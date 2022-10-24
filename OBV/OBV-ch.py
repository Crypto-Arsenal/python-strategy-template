class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 60 分鐘
        self.period = 60 * 60
        self.options = {}

        self.last_type = 'sell'
        self.divide_quote = 0
        self.proportion = 0.2

    def on_order_state_change(self,  order):
        pass

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

        if len(close_price_history) < 5 :
            return []

        obv = talib.OBV(close_price_history, trade_volume_history)
        obv_five = obv[-4:]
        last_v = obv[-1]
        third_v = obv[-2]
        second_v = obv[-3]
        first_v = obv[-4]
        
        five_max = max(obv_five, default = 0)
        five_min = min(obv_five, default = close_price)
        
        curr_price = close_price_history[-1]
        prev_price = close_price_history[-2]

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # 用2成資產計算amount
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        signal = 0 
        # OBV最高點，且價格上漲(加入N字型動態)
        if five_max == last_v and (second_v > first_v and second_v > third_v):
            if curr_price > prev_price:
                signal = 1

        # 最低點，且價格下降(加入N字型動態)
        if five_min == last_v and (second_v < first_v and second_v < third_v):
            if curr_price < prev_price and available_base_amount > 0:
                signal = -1
                
        # 送出訂單 - 買
        if self.last_type == 'sell' and signal == 1:
            if available_quote_amount >= self.divide_quote:
                CA.log('買入 ' + base)
                self.last_type = 'buy'
                CA.buy(exchange, pair, self.divide_quote/high_price, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif self.last_type == 'buy' and signal == -1:
            if available_base_amount > 0.0001:
                CA.log('賣出 ' + base)
                self.last_type = 'sell'
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
                self.divide_quote = 0

        return
