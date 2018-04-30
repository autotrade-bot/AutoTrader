import json
import subprocess
import logging
import hashlib
import os

class MovingAverageStrategy:
    __short_term = 30
    __long_term = 120
    __rate = 0.007

    def __init__(self, conf):
        self.logger = logging.getLogger(__name__)
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s: %(message)s')
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)
        self.logger.setLevel(20)
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

        # ログ
        self.logger.info('Short Slope: %f, Long Slope: %f' % (short_slope, long_slope))
        self.logger.info('Distance from intersection: %f' % abs(close_time - intersection))
        self.logger.info('Close Price: %d' % close_price)

        if abs(close_time - intersection) < short_term * 60 * UNIT:
            # 買い
            if short_slope > long_slope and short_slope > 0:
                self.logger.info('Golden Cross')
                if (close_price - short_ma) / short_ma < self.__rate:
                    # 建玉なし
                    if btc == 0:
                        return 'buy', round(jpy / close_price, 4)
                    # 売りの建玉あり
                    elif btc < 0:
                        return 'buy', -btc
            # 売り
            elif short_slope < long_slope and short_slope < 0:
                self.logger.info('Dead Cross')
                if (short_ma - close_price) / short_ma < self.__rate:
                    # 建玉なし
                    if btc == 0:
                        return 'sell', round(jpy / close_price, 4)
                    # 買いの建玉あり
                    if btc > 0:
                        return 'sell', btc

        return 'nothing', 0

    def get_next_action(self, api_driver):
        p = subprocess.Popen('curl https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=60', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        self.chart = json.loads(p.stdout.read().decode('utf-8'))['result']['60']
        result = {}
        balance = api_driver.get_balance()
        result['action'], result['amount'] = self.calc_next_action(balance['JPY'], balance['BTC'])
        self.logger.info('Result: %s' % str(result))
        return result

    def get_revision(self):
        sha256 = hashlib.sha256()
        with open(os.path.abspath(__file__), 'r') as f:
            while True:
                buf = f.read(2047)
                if not buf: break
                sha256.update(buf.encode('utf-8'))
        return sha256.hexdigest()[:15]
