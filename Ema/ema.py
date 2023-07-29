"""
Contributed by BCA_Daniel @BCA_Quantrade / Crypto-Arsenal & Alan Wu @Crypto-Arsenal
-
Superposition EMAs are designed to smooth out EMAs and reduce noise interference.
This strategy utilizes four EMAs and uses the output of the previous EMA as the input for the next EMA.

Strategy designer: BCA_Daniel 2023.07.16
"""
class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
        self.period = 60  *  30 
        self.options = {}
        self.last_type = 'sell'

        ### fast / slow ema period
        self.fast_period = 14
        self.sp1_period = 14
        self.sp2_period =14
        self.slow_period = 14
    
        self.divide_quote = 0
        self.proportion = 0.2

    def on_order_state_change(self,  order):
        pass

    # called every self.period
    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        ca_position = self.get_ca_position()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]

        # convert to chronological order for talib
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()

        # convert np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)

        close_price = close_price_history[0]
        high_price = high_price_history[0]

        #ema fast / slow create
        #np.nan_to_num used to refilled nan to 0 for output array
        EMA_fast = talib.EMA(close_price_history, timeperiod=self.fast_period)
        EMA_fast_filled = np.nan_to_num(EMA_fast, nan=0)
        EMA_superposition_1 = talib.EMA(EMA_fast_filled, timeperiod=self.sp1_period)
        EMA_superposition_1_filled =  np.nan_to_num(EMA_superposition_1, nan=0)
        EMA_superposition_2 = talib.EMA(EMA_superposition_1_filled,self.sp2_period)
        EMA_superposition_2_filled = np.nan_to_num(EMA_superposition_2, nan=0)
        EMA_slow = talib.EMA(EMA_superposition_2_filled, self.slow_period)
        
        if len(close_price_history) < self.slow_period + 1:
            return []
        
        # current ema fast / slow
        curr_ema_fast = EMA_fast[-1]
        curr_ema_slow = EMA_slow[-1]

        # previous time stamp ema
        prev_ema_fast = EMA_fast[-2]
        prev_ema_slow = EMA_slow[-2]

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)

        # initialize signal to be 0
        signal = 0
        if available_base_amount< self.divide_quote/high_price and available_base_amount > -self.divide_quote/high_price:
            # open long position
            if curr_ema_fast > curr_ema_slow and prev_ema_fast < prev_ema_slow:
                signal = 1
            # open short position
            if curr_ema_fast < curr_ema_slow and prev_ema_fast > prev_ema_slow:
                signal = -1
          
        # Sell short
        if signal == -1:
            self['is_shorting'] = 'true'
            CA.log('Sell short ' + str(base))
            if ca_position:
                CA.place_order(exchange, pair, action='close_long', conditional_order_type='OTO', child_conditional_orders=[{'action': 'open_short', 'percent':80}])
            else:
                CA.place_order(exchange, pair, action='open_short',  percent=80)

        # Buy long
        if signal == 1:
            self['is_shorting'] = 'false'
            CA.log('Buy ' + str(base))
            if ca_position:
                CA.place_order(exchange, pair, action='close_short', conditional_order_type='OTO', child_conditional_orders=[{'action': 'open_long', 'percent':80}])
            else:
                CA.place_order(exchange, pair, action='open_long',  percent=80)

        
        # return current total position: -n 0, +n  where n is number of contracts
    def get_ca_position(self):
        exchange, pair, base, quote = CA.get_exchange_pair()

        long_position = CA.get_position(exchange, pair, CA.PositionSide.LONG)
        if long_position:
            return abs(long_position.total_size)

        short_position = CA.get_position(exchange, pair, CA.PositionSide.SHORT)
        if short_position:
            return -1 * abs(short_position.total_size)

        return  0
