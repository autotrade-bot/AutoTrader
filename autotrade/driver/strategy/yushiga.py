import json
import subprocess

class MovingAverageStrategy:
    __short_term = 30
    __long_term = 120
    __rate = 0.007

    def __init__(self):
        return

    def calc_moving_average(self, index, range_minutes):
        res = 0
        close_price = 0
        for x in self.chart[index-range_minutes:index]:
            close_time, open_price, high_price, low_price, close_price, volume, _ = tuple(x)
            res += close_price

        res += close_price
        return res / (range_minutes + 1)

    def calc_straight_line(self, x1, y1, x2, y2):
        slope = (y2 - y1) / (x2 - x1)
        intercept = y2 - slope * x2
        return (slope, intercept)

    # timeのみ返す
    def calc_intersection(self, slope1, intercept1, slope2, intercept2):
        return (intercept1 - intercept2) / (slope2 - slope1)

    def calc_next_action(self, jpy, btc):
        UNIT = 1
        short_term = self.__short_term
        long_term = self.__long_term
        data_num = len(self.chart)
        close_time, open_price, high_price, low_price, close_price, volume, _ = tuple(self.chart[-1])

        # 移動平均計算
        short_ma = self.calc_moving_average(data_num, short_term)
        short_ma_pre = self.calc_moving_average(data_num - short_term, short_term)
        long_ma = self.calc_moving_average(data_num, long_term)
        long_ma_pre = self.calc_moving_average(data_num - long_term, long_term)

        # 移動平均線計算
        short_slope, short_intercept = self.calc_straight_line(close_time, short_ma, close_time - 60 * UNIT * short_term, short_ma_pre)
        long_slope, long_intercept = self.calc_straight_line(close_time, long_ma, close_time - 60 * UNIT * long_term, long_ma_pre)

        # 交点計算
        intersection = self.calc_intersection(short_slope, short_intercept, long_slope, long_intercept)

        if abs(close_time - intersection) < short_term * 60 * UNIT:
            if short_slope > long_slope and long_slope > 0:
                if (close_price - short_ma) / short_ma < self.__rate:
                    if btc * close_price < jpy :
                        return 'buy', jpy
            elif short_slope < long_slope:
                if (short_ma - close_price) / short_ma < self.__rate:
                    if btc * close_price > jpy:
                        return 'sell', btc

            return 'nothing', 0

    def get_next_action(self, api_dirver):
        p = subprocess.Popen('curl https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods=60', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        self.chart = json.loads(p.stdout.read().decode('utf-8'))['result']['60']
        result = {}
        balance = api_dirver.get_balance()
        result['action'], result['amount'] = self.calc_next_action(balance['JPY'], balance['BTC'])
        return json.dumps(result)
