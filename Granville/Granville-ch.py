class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 30 分鐘
        self.period = 30 * 60
        self.options = {}

        self.last_type = 'sell'
        # 乖離率
        self.bias_rate = 0.5
        self.ema_period = 20
        self.proportion = 0.9


    def on_order_state_change(self,  order):
        pass
        
    def get_signal(self, c_last, c_mid, c_tail, e_last, e_mid, e_tail, cline_new, cline_old, eline_new, eline_old):
        signal = 0
        rate = self.bias_rate 
        # 葛蘭碧八大法則 Granville Rules
        # 葛氏利用股價與移動平均線兩者間的變化，包括相互的關係性、股價穿越均線的方式、兩者乖離的大小等各種情況，歸納出八種不同的情形，作為進出的依據：

        # 1.當移動平均線從下降趨勢逐漸轉變為水平盤整或呈現上昇跡象時，若價位線從下方穿破移動平均線往上昇-買進
        if eline_old == -1 and e_last >= e_mid:
            if c_mid < e_mid and c_last > e_last:
                signal = 1
        # 2.當價位線的趨勢走在移動平均線之上，價位線下跌但卻未跌破移動平均線便再度反彈上昇-買進
        if c_tail > e_tail and c_mid > e_mid:
            if cline_old == -1 and c_last > e_last:
                signal = 1
        # 3.當價位線往上急漲，不僅穿破移動平均線，而且高高地遠離於移動平均線上，開始反轉下降又趨向於移動平均線-賣出
        if cline_old == 1 and c_mid > e_mid and np.absolute(c_mid-e_mid) > (e_mid*rate) and np.absolute(c_last - e_last) < (e_last*rate):
            signal == -1
        # 4.雖然價位線往下跌破移動平均線，但隨即又回昇到移動平均線之上，且此時移動平均線依然呈現上昇的走勢-買進
        if cline_old == -1 and c_mid < e_mid and c_last > e_last and eline_new == 1:
            signal = 1
        # 5.當移動平均線從上昇趨勢逐漸轉變成水平盤局或呈現下跌跡象時，若價位線從上方跌破移動平均線往下降時-賣出
        if eline_old == 1 and e_last <= e_mid and c_last < e_last:
            signal = -1
        # 6.當價位線往下急跌，不僅跌破移動平均線，而且深深地遠離於移動平均線下，開始反彈上昇又趨向於移動平均線-買進
        # (e_mid * rate) 價格的3%
        if cline_old == -1 and c_mid < e_mid and np.absolute(e_mid - c_mid) > (e_mid * rate):
            if cline_new == 1 and np.absolute(c_last-e_last) < np.absolute(e_last*rate):
                signal = 1
        # 7.雖然價位線往上昇穿破移動平均線，但隨即又回跌到移動平均線之下，且此時移動平均線依然呈現下跌的走勢-賣出
        if cline_old == 1 and c_mid > e_mid and c_last < e_last and eline_new == -1:
            signal = -1
        # 8.當價位線的趨勢走在移動平均線之下，價位線上昇但卻未能穿破移動平均線便再度反轉下跌-賣出
        if e_tail > c_tail and e_mid > c_mid and cline_old == 1 and cline_new == -1:
            signal = -1

        return signal

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

        # 指數移動平均值
        ema = talib.EMA(close_price_history, self.ema_period)

        if len(ema) < 3:
            return []

        # 收盤價
        c_last = float(close_price_history[-1])
        c_mid = float(close_price_history[-2])
        c_tail = float(close_price_history[-3])

        # 指數移動平均值
        e_last = float(ema[-1])
        e_mid = float(ema[-2])
        e_tail = float(ema[-3])

        # 價格線的趨勢，1為上漲，-1為下跌
        cline_old = 1 if c_mid > c_tail else -1
        cline_new = 1 if c_last > c_mid else -1
        # 指數平均線的趨勢，1為上漲，-1為下跌
        eline_old = 1 if e_mid > e_tail else -1
        eline_new = 1 if e_last > e_mid else -1

        # signal = 1 則買, signal = -1 則賣
        trade_signal = 0
        # 買賣判定
        trade_signal = self.get_signal(c_last, c_mid, c_tail, e_last, e_mid,
                        e_tail, cline_new, cline_old, eline_new, eline_old)
        
        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        # 送出訂單 - 買
        if self.last_type == 'sell' and trade_signal == 1:
            amount = np.around((available_quote_amount /  close_price_history[-1]) * self.proportion, 5)
            if available_quote_amount >= amount * close_price_history[-1]:
                CA.log('買入 ' + base)
                self.last_type = 'buy'
                CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
        
        # 送出訂單 - 賣
        elif self.last_type == 'buy' and trade_signal == -1:
            if available_base_amount > 0:
                CA.log('賣出 ' + base)
                self.last_type = 'sell'
                CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)
        
        return

    
