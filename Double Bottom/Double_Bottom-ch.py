class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
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
            if len([i for i in p1 if midValue < i]) > 0: #往前比代表目前值不是最大
                return False
            if len([i for i in p2 if midValue <= i]) > 0: #往後比代表目前值不是最大,後續還有更大
                return False
        else:
            if len([i for i in p1 if midValue > i]) > 0: #往前比代表目前值不是最小
                return False
            if len([i for i in p2 if midValue >= i]) > 0: #往後比代表目前值不是最小,後續還有更小
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
        if len(close_price_history) < (self.range_val):
            return []

        high_window = high_price_history[-self.range_val:]
        low_window = low_price_history[-self.range_val:]

        max_high = high_window[self.range_val // 2]
        min_low = low_window[self.range_val // 2]
        
        if self.double_bottom == False:
            if self.check_value(high_window, max_high, '>'):

                #先取第一點高點
                if self.first_max == 0:
                    self.first_max = max_high
                    
                # 假如原高點不是最高點則表示W型態失敗
                elif self.first_max < max_high:
                    self.first_max = max_high
                    self.first_min = 0
                    self.neckline = 0

                # 已有第一高點，且新的高點<=第一高點，設定此高點為瓶頸值
                else:
                    self.neckline = max_high

            if self.check_value(low_window, min_low, '<') and self.first_max != 0:

                # 已建立高點情況下 ，設定第一個低點
                if self.first_min == 0:
                    self.first_min = min_low
                elif self.neckline == 0:
                    if self.first_min <= min_low:
                        self.first_min = min_low

                # 假如原低點不是最低點則表示W型態失敗
                elif min_low < self.first_min:
                    self.first_max = 0
                    self.first_min = 0
                    self.neckline = 0
                
                # 已有最低點、瓶頸值，且新的低點值>=第一個低點
                else:
                    self.double_bottom = True
                    
        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # signal = 1 則買, signal = -1 則賣
        signal = 0        
        if self.double_bottom:
            curr_close = close_price_history[-1]
            # 價格衝破neckline
            if curr_close > self.neckline:
                # 尚未建倉，進行買進開倉
                if available_base_amount >= -0.0001 and available_base_amount <= 0.0001: 
                    signal = 1
                # 已建倉
                elif available_base_amount > 0.0001:
                    if self.base_price != 0:
                        # 獲利1% 就全賣
                        if (curr_close - self.base_price) / self.base_price > self.profit_gain:
                            signal = -1
                        else:
                            signal = 1
            # 價格跌破neckline
            else:
                self.double_bottom = False
                if available_base_amount > 0.0001:
                    signal = -1

        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        # 送出訂單 - 買
        if signal == 1:
            if available_quote_amount >= self.divide_quote:
                CA.log('買入 ' + base)
                CA.buy(exchange, pair, self.divide_quote/high_price, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif signal == -1:
            if available_base_amount > 0.0001:
                CA.log('賣出 ' + base)
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
                self.divide_quote = 0
                self.double_bottom = False
                self.first_max = 0
                self.first_min = 0
                self.neckline = 0
        return
