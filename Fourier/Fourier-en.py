class Strategy(StrategyBase):
    def __init__(self):
        # strategy property
        self.subscribed_books = {}
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
        """ Fourier extrapolation
        Fourier transformation + regression model make predictions
        params:
            x: time series
            n_predict: predict how many phases
            n_harm: keep only top n_harm frequencies (both positive and negative) to minimize noise during inverse Fourier transform
        return:
            time series with predictions and without noise

        """
        n = x.size
        t = np.arange(0, n)

        # regression
        p = np.polyfit(t, x, 1)         
        x_notrend = x - p[0] * t

        # Fourier transform
        x_freqdom = np.fft.fft(x_notrend)  # convert to frequency domain
        f = np.fft.fftfreq(n)              # frequencies (the x axis in frequency domain)
        indexes = list(range(n))
        # sort according to the absolute value of the frequencies
        indexes.sort(key = lambda i: np.absolute(f[i]))

        # predictions
        t = np.arange(0, n + n_predict)
        restored_sig = np.zeros(t.size) 
        for i in indexes[:1 + n_harm * 2]:          # inverse transform only the top n_harm frequencies while others will be regarded as noise
            ampli = np.absolute(x_freqdom[i]) / n   # amplitude
            phase = np.angle(x_freqdom[i])          # phase
            restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
        return restored_sig + p[0] * t

    # called every self.period
    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        trade_volume_history = [candle['volume'] for candle in candles[exchange][pair]]

        # convert to chronological order for talib
        close_price_history.reverse()
        high_price_history.reverse()
        low_price_history.reverse()
        trade_volume_history.reverse()

        # convert to np.array
        close_price_history = np.array(close_price_history)
        high_price_history = np.array(high_price_history)
        low_price_history = np.array(low_price_history)
        trade_volume_history = np.array(trade_volume_history)

        close_price = close_price_history[-1]
        high_price = high_price_history[-1]

        if len(close_price_history) < 2:
            return []

        # get available balance
        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available
        
        if self.divide_quote == 0:
            self.divide_quote = np.round(available_quote_amount* self.proportion, 5)
            
        # predict price
        predict = self.fourierExtrapolation(close_price_history, self.interval, 10)[-self.interval: ]
  
        signal = 0
        if available_base_amount < self.divide_quote/high_price and available_base_amount > -self.divide_quote/high_price:
            # predicted price is larger than the actual price
            # open long position
            if max(predict) > close_price * (1 + self.bound):
                signal = 1

            # predicted price is smaller than the actual price
            # open short position
            elif min(predict) < close_price * (1 - self.bound):
                signal = -1

        # holding long position 
        elif available_base_amount > self.divide_quote/high_price:
            # current close price is lower than the one at previous timestamp (accumulated x times)
            if close_price_history[-1] < close_price_history[-2]:
                self.accumulate = self.accumulate + 1
            # reaches the limit then take profit
            if self.accumulate == self.accu_limit:
                signal = 2
            # stop loss
            elif close_price_history[-1] < self.open_price * (1 - self.stop_less):
                signal = 2
                self.accumulate = 0

        # holding short position
        elif available_base_amount < -self.divide_quote/high_price:
            # current close price is higher than the one at previous timestamp (accumulated x times)
            if close_price_history[-1] > close_price_history[-2]:
                self.accumulate = self.accumulate + 1
            # reaches the limit then take profit
            if self.accumulate == self.accu_limit:
                signal = -2
            # stop loss
            elif close_price_history[-1] > self.open_price * (1 + self.stop_less):
                signal = -2
                self.accumulate = 0

        # sell short
        if signal == -1:
            self['is_shorting'] = 'true'
            amount = -self.divide_quote/high_price * 1.1
            CA.log('Sell short ' + str(base))
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

        # buy to cover
        elif signal == -2:
            amount = -available_base_amount
            self.divide_quote = 0
            self['is_shorting'] = 'true'
            CA.log('Buy to cover ' + str(base))
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
         
        # place buy order
        elif signal == 1:
            amount = self.divide_quote/high_price  * 1.1
            self['is_shorting'] = 'false'
            CA.log('Buy ' + base)
            self.last_type = 'buy'
            CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            
        # place sell order
        elif signal == 2:
            self['is_shorting'] = 'false'
            self.last_type = 'sell'
            self.divide_quote = 0
            CA.log('Sell ' + base)
            CA.sell(exchange, pair, available_base_amount, CA.OrderType.MARKET)

        return 
