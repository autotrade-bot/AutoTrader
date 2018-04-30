import json
import subprocess

class BitflyerChartDriver():
    def __init__(self, conf):
        pass
    
    def get(self, minutes=1):
        periods = str(minutes * 60)
        p = subprocess.Popen('curl https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods={0}'.format(periods), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        chart = json.loads(p.stdout.read().decode('utf-8'))['result'][periods]
        return chart
