class Strategy(StrategyBase):
    def __init__(self):
        # 策略屬性
        self.subscribed_books = {}
        # 60 分鐘
        self.period = 60 * 60
        self.options = {}

        self.last_type = 'sell'
        self.buy_price = 0
        self.region = 10
        self.collect_region = 10
        self.volumes = {-0.01 : 1}
        self.record_num = 10
        self.pressure_line = []
        self.up_pline = None
        self.down_pline = None
        self.multiplier = 80
        self.amount = 0
        self.proportion = 0.2

    def on_order_state_change(self,  order):
        pass

    def compress(self, line_list, interval):
        """壓力線整合

        若兩壓力線間距小於所設定之interval，則整併成一條，持續整併直到
        所有壓力線間的距離都大於設定之interval。

        """
        circle = 1
        # 壓力線已由小到大排序，依序檢查其與鄰近的壓力線是否過於靠近
        # 若過於靠近則整合，不斷重複此步驟直到某次迴圈內沒有觸發整合即跳出while
        while(circle==1):
            new_line_list = []
            append = 0
            circle = 0                  # 若迴圈皆無觸發整合，則迴圈結束時可跳出while
            for i in range(len(line_list)-1):
                if np.absolute(line_list[i]-line_list[i+1]) <= interval:
                    new_line_list.append((line_list[i] + line_list[i+1]) / 2)
                    append = 1
                    circle = 1          # 觸發整合，預約下次迴圈
                else:
                    if append==1:
                        append = 0
                    else:
                        new_line_list.append(line_list[i])
            if append==0:
                new_line_list.append(line_list[-1])
            line_list = new_line_list
        return new_line_list

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

        # 取得可用資產數量
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if len(close_price_history) < self.record_num :
            return []

        # 用2成資產計算amount
        if self.amount == 0:
            self.amount = np.round((available_quote_amount / close_price) * self.proportion, 5)
        
        record_price = close_price_history[-1] // (self.collect_region * self.collect_region)
        if record_price in self.volumes:
            self.volumes[record_price] = self.volumes[record_price] + trade_volume_history[-1]
        else:
            self.volumes[record_price] = trade_volume_history[-1]

        sort_dict = sorted(self.volumes.items(), key = lambda v: v[1])
        max_volume = sort_dict[-1][1]
        self.pressure_line = [k+(self.collect_region/2) for k, v in self.volumes.items() if v >= max_volume * 0.8]
        
        if len(self.pressure_line) == 0:
            return []
        
        self.pressure_line.sort()
        self.pressure_line = self.compress(self.pressure_line, self.collect_region)
        current_price = close_price_history[-1]
        
        # 計算目前價格位置處於哪兩交易線之間
        for i in range(len(self.pressure_line)):
            if current_price <= self.pressure_line[i] * self.multiplier:
                if i == 0:
                    # 處在最小的壓力線下方，僅有上壓力線
                    self.up_pline = self.pressure_line[i]* self.multiplier
                    self.down_pline = None
                else:
                    self.up_pline = self.pressure_line[i]* self.multiplier
                    self.down_pline = self.pressure_line[i-1]* self.multiplier
                break
            
            else:
                # 處在最大的壓力線之上，僅有下壓力線
                self.up_pline = None
                self.down_pline = self.pressure_line[i]* self.multiplier

        # 設定停利區間，以兩壓力線之距離的一半當作停利，四分之一當作停損
        if self.up_pline and self.down_pline:       # 兩壓力線皆存在
            
            # 兩壓力線相差太小先拒絕
            distance = np.absolute(self.up_pline - self.down_pline)
            if distance < self.region * 2:
                return []
            else:
                self.distance = distance
        
        # 其中一壓力線為None
        else:
            self.distance = 50  
        
        signal = 0
        prev_price = close_price_history[-2]
        
        # 若還未開倉
        if self.buy_price == 0:
            
            # 對上壓力線進行判斷: 1. 前一期是否處在區間範圍, 2. 當期是否穿越區間範圍
            if self.up_pline:
                if (self.up_pline - self.region) < prev_price <(self.up_pline + self.region):
                    # 進入區間後往下穿越，未突破上壓力線
                    if current_price <= (self.up_pline - self.region):
                        signal = -1
                    # 進入區間後繼續往上穿越，突破上壓力線
                    elif current_price >= (self.up_pline + self.region):
                        signal = 1
            
            # 對下壓力線進行判斷: 1. 前一期是否處在區間範圍, 2. 當期是否穿越區間範圍
            if self.down_pline:
                if (self.down_pline - self.region) < prev_price < (self.down_pline + self.region):
                    # 進入區間後繼續往下穿越，突破下壓力線
                    if current_price <= (self.down_pline - self.region):
                        signal = -1
                    # 進入區間後往上穿越，未突破下壓力線
                    elif current_price >= (self.down_pline + self.region):
                        signal = 1
        
        # 已開倉，進行停損停利判別
        else:
            # 計算目前獲利
            if available_base_amount > 0.5:
                profit = current_price - self.buy_price
            else:
                profit = self.buy_price - current_price
            # 依獲利進行停損停利，並計算獲勝與否
            if profit > (self.distance/2) or profit < -(self.distance/4):
                signal = -1 + 2 * (1 - (available_base_amount > 0.5))

        # 送出訂單 - 買
        if signal == 1 and available_quote_amount > (close_price * self.amount):
            self.last_type = 'buy'
            CA.log('買入 ' + base)
            self.buy_price = close_price
            CA.buy(exchange, pair, self.amount, CA.OrderType.MARKET)

        # 送出訂單 - 賣
        elif signal == -1 and available_base_amount > 0:
            self.last_type = 'sell'
            CA.log('賣出 ' + base)
            CA.sell(exchange, pair, self.amount * 0.999, CA.OrderType.MARKET)
        
        return
