from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_
from autotrade.lib.utils import Utils
from datetime import datetime
from pytz import timezone
from time import sleep
import os
import json
import subprocess


class SQLiteStoreDriver():
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:password@mysql/autotrade?charset=utf8', echo=False)
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

def main(drivers):
    sqlite = SQLiteStoreDriver()

    price = drivers.get("api").get_price()
    open_price = price
    high_price = price
    low_price = price
    close_price = price
    created_at = datetime.now()
    sqlite.put(open_price, high_price, low_price, close_price, created_at)

if __name__ == '__main__':
    utils = Utils()
    conf = utils.load_conf(os.environ.get("CONF_PATH"))
    drivers = utils.load_driver(conf)
    while True:
        main(drivers)
        sleep(1)
