class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        self.period = 30 * 60
        self.options = {}

        self.divide_quote = 0
        self.proportion = 0.2
        self.mfi_period = 14
        self.overbought = 80
        self.oversold = 20

    def on_order_state_change(self,  order):
        pass

    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        open_price_history = [candle['open'] for candle in candles[exchange][pair]]
        trade_volume_history = [candle['volume'] for candle in candles[exchange][pair]]

        # 將資料由舊到新排列
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        open_price_history.reverse()
        trade_volume_history.reverse()
        
        # 轉換為 np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        open_price_history = np.array(open_price_history)
        trade_volume_history = np.array(trade_volume_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]
        MFI = talib.MFI(high_price_history, low_price_history, close_price_history, trade_volume_history, timeperiod=self.mfi_period)


        if len(MFI) < 2:
            return 

        signal = 0
        # MFI 資金流量指標 < 20 代表超賣
        if (MFI[-1] < self.oversold and MFI[-2] > self.oversold) : 
            signal = 1
        
        # MFI 資金流量指標 > 80 代表超買
        if (MFI[-1] > self.overbought and MFI[-2] < self.overbought) : 
            signal = -1

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
        
        # 送出訂單 - 買
        if signal == 1:
            if available_quote_amount >= self.divide_quote:
                CA.log('買入 ' + base)
                CA.buy(exchange, pair, self.divide_quote/high_price, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif signal == -1:
            if available_base_amount > 0.00001:
                CA.log('賣出 ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
                self.divide_quote = 0
        return
