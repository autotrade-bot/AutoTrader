from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_
from datetime import datetime
from time import sleep
import json
import subprocess


class SQLiteStoreDriver():
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:password@mysql/autotrade?charset=utf8', echo=True)
        metadata = MetaData()
        metadata.bind = engine
        
        # menuテーブルの定義
        self.OHLC = Table(
          'ohlc', metadata,
          Column('id', Integer, primary_key=True),
          Column('open', Integer), # buy or sell
          Column('high', Integer),
          Column('low', Integer), # open or close
          Column('close', Integer),
          Column('created_at', DateTime, unique=True),
        )
        metadata.create_all()

    def put(self, op, high, low, cl, created_at):
        self.OHLC.insert().execute(
                open=op, 
                high=high,
                low=low,
                close=cl,
                created_at=created_at)

def main():
    sqlite = SQLiteStoreDriver()
    p = subprocess.Popen('curl https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=60', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    last_chart = json.loads(p.stdout.read().decode('utf-8'))['result']['60'][-1]
    open_price = last_chart[1]
    high_price = last_chart[2]
    low_price = last_chart[3]
    close_price = last_chart[4]
    created_at = datetime.fromtimestamp(last_chart[0])
    sqlite.put(open_price, high_price, low_price, close_price, created_at)

if __name__ == '__main__':
    while True:
        main()
        sleep(60)


