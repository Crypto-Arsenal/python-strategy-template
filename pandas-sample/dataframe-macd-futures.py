class Strategy(StrategyBase):
    def __init__(self):
        # strategy attributes
        self.period =30 * 60
        self.subscribed_books = {}
        self.options = {}
        self.data = {'open': [],'high': [],'low': [],'close': [],'std':[]}
        self.dataframe = pd.DataFrame(self.data)
        # define your attributes here
        self.count=0
        self.last_type = 'none'
        prefetch_period = 500
        history_candles = CA.get_history_candles(prefetch_period, self.period)
        exchange, pair, base, quote = CA.get_exchange_pair()
        if history_candles:     
            for candle in history_candles[exchange][pair]:
                self.dataframe=self.dataframe.append({'open': self.count}, ignore_index=True)
                self.dataframe.open.loc[self.count] = candle['open']  
                self.dataframe.high.loc[self.count] = candle['high']
                self.dataframe.low.loc[self.count] = candle['low']
                self.dataframe.close.loc[self.count] = candle['close']
                self.count += 1
    def on_order_state_change(self,  order):
        pass

    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        candle = candles[exchange][pair][0]

        #DIY pandas 
        self.dataframe=self.dataframe.append({'open': self.count}, ignore_index=True)
        self.dataframe.open.loc[self.count]=candle['open']
        self.dataframe.high.loc[self.count]=candle['high']
        self.dataframe.low.loc[self.count]=candle['low']
        self.dataframe.close.loc[self.count]=candle['close']
        self.count+=1        

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available
        
        exchange, pair, base, quote = CA.get_exchange_pair()

        long_position = CA.get_position(exchange, pair, CA.PositionSide.LONG)
        available_long_position_size = 0
        if long_position:
            available_long_position_size = long_position.available_size
            total_long_position_size = long_position.total_size
        short_position = CA.get_position(exchange, pair, CA.PositionSide.SHORT)
        available_short_position_size = 0
        if short_position:
            available_short_position_size = short_position.available_size
            total_short_position_size = short_position.total_size

        self.dataframe['EMA_12'] = self.dataframe.close.ewm(span=12).mean()
        self.dataframe['EMA_26'] = self.dataframe.close.ewm(span=26).mean()
        self.dataframe['DIF'] =  self.dataframe['EMA_12'] -  self.dataframe['EMA_26']
        self.dataframe['DEM'] =  self.dataframe['DIF'].ewm(span=9).mean()
        self.dataframe['OSC'] =  self.dataframe['DIF'] -  self.dataframe['DEM']

        curr_macd =  self.dataframe['OSC'].values[-1]
        prev_macd = self.dataframe['OSC'].values[-2]

        signal = 0
        # MACD crosses the zero line from below - buy signal
        if prev_macd < 0 and curr_macd > 0:
            signal = 1
        
        # MACD crosses the zero line from above - sell signal
        elif prev_macd > 0 and curr_macd < 0:
            signal = -1

        # place buy order
        if signal == 1:
            if self.last_type == 'none': 
                self.last_type = 'buy'
                CA.place_order(exchange, pair, action='open_long', percent=90)
            elif self.last_type == 'sell': 
                self.last_type = 'buy'
                CA.place_order(exchange, pair, action='close_short', conditional_order_type='OTO', child_conditional_orders=[{ 'action': 'open_long'}])        
           
        # place sell order
        elif signal == -1:
            if self.last_type == 'none': 
                self.last_type = 'sell'
                CA.place_order(exchange, pair, action='open_short', percent=90)
            if self.last_type == 'buy':
                self.last_type = 'sell'
                CA.place_order(exchange, pair, action='close_long', conditional_order_type='OTO', child_conditional_orders=[{ 'action': 'open_short'}])        
        
        return
