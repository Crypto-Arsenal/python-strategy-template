class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 60 分鐘
        self.period = 60 * 60
        self.options = {}

        self.last_type = 'sell'
        self.interval = 5
        self.bound = 0.01
        self.open_price = 0
        self.accumulate = 0
        self.hold_vol = 2
        self.accu_limit = 3
        self.stop_less = 0.02
        self.hold_limit = 0.5
        self.divide_quote = 0
        self.proportion = 0.2

    def on_order_state_change(self,  order):
        self.open_price = order['price']

    def fourierExtrapolation(self, x, n_predict, n_harm):
        """傅立葉外推法

        以傅立葉轉換配合一點迴歸模型來進行預測。
        params:
            x: 時間序列。
            n_predict: 預測幾期。
            n_harm: 逆轉換時，僅保留前n_harm個頻率(正負皆保留)，以消除雜訊。
        return:
            (包含預測結果的)消除雜訊的時間序列。

        """
        n = x.size
        t = np.arange(0, n)

        # 藉由迴歸排除趨勢
        p = np.polyfit(t, x, 1)         
        # numpy 的多項式擬合函式
        # 擬合一次多項式可視為進行簡易迴歸
        x_notrend = x - p[0] * t

        # 傅立葉轉換
        x_freqdom = np.fft.fft(x_notrend)  # 將排除趨勢後的資料轉換至frequency domain
        f = np.fft.fftfreq(n)              # frequencies (frequency domain的x軸)
        indexes = list(range(n))
        # 依頻率之絕對值排列index(由小到大)，以利之後逆轉換
        indexes.sort(key = lambda i: np.absolute(f[i]))

        # 預測
        t = np.arange(0, n + n_predict)
        restored_sig = np.zeros(t.size)
        for i in indexes[:1 + n_harm * 2]:          # 只對前n_harm個低頻進行逆轉換，其餘當成雜訊捨棄
            ampli = np.absolute(x_freqdom[i]) / n   # amplitude
            phase = np.angle(x_freqdom[i])          # phase
            restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
        return restored_sig + p[0] * t

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

        if len(close_price_history) < 2:
            return []

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available
        
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
            
        # 預測價格
        predict = self.fourierExtrapolation(close_price_history, self.interval, 10)[-self.interval: ]
  
        signal = 0
        # 手上無部位
        if available_base_amount < self.divide_quote/high_price and available_base_amount > -self.divide_quote/high_price:
            # 預測價格大於今日價格買進
            if max(predict) > close_price * (1 + self.bound):
                signal = 1

            # 預測價格小於今日價格賣出
            elif min(predict) < close_price * (1 - self.bound):
                signal = -1

        # 手上有多頭部位,只考慮空頭平倉
        elif available_base_amount > self.divide_quote/high_price:
            # 今日收盤低於昨日收盤 (累積Ｘ次)
            if close_price_history[-1] < close_price_history[-2]:
                self.accumulate = self.accumulate + 1
            # 達累積次數，停利
            if self.accumulate == self.accu_limit:
                signal = 2
            # 停損
            elif close_price_history[-1] < self.open_price * (1 - self.stop_less):
                signal = 2
                self.accumulate = 0

        # 手上有空頭部位,只考慮多頭平倉
        elif available_base_amount < -self.divide_quote/high_price:
            # 今日收盤高於昨日收盤 (累積Ｘ次)
            if close_price_history[-1] > close_price_history[-2]:
                self.accumulate = self.accumulate + 1
            # 達累積次數，停利
            if self.accumulate == self.accu_limit:
                signal = -2
             # 停損
            elif close_price_history[-1] > self.open_price * (1 + self.stop_less):
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
            self.last_type = 'buy'
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            
        # 送出訂單 - 賣
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.last_type = 'sell'
            self.divide_quote = 0
            CA.log('賣出 ' + base)
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
