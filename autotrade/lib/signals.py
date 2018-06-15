from utils import Utils
class Signal():

    def __init__(self, chart):
        self.chart = chart
        self.utils = Utils()
        self.driver = self.utils.load_driver(self.utils.conf)

    # dpo
    # åˆ range = n
    # dpo(n) = close_price - (n/2 + 1)*(n days ago's sma(n))
    def dpo(self, created_at, calc_range):
        return chart[created_at].close_price - (calc_range/2+1) * sma(calc_range)[now - datetime.timedelta(days=calc_range)]

    def sma(self, calc_range):
        pass
