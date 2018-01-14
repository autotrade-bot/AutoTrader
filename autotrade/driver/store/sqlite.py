from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_
from datetime import datetime


class SQLiteStoreDriver():
    def __init__(self):
        engine = create_engine('sqlite:///trade_history.db', echo=True)
        metadata = MetaData()
        metadata.bind = engine
        
        # menuテーブルの定義
        self.TradeHistory = Table(
          'trade_history', metadata,
          Column('id', Integer, primary_key=True),
          Column('side', String), # buy or sell
          Column('price', Integer),
          Column('position_status', String), # open or close
          Column('profit', Integer),
          Column('created_at', DateTime),
        )
        metadata.create_all()

    def put_trade_history(self, side, position_status, profit, created_at):
       # self.TradeHistory.insert().execute(
       #         side=side, 
       #         position_status=position_status,
       #         profit=profit,
       #         created_at=created_at)
        with open('/mnt/history.csv', 'a') as f:
            f.write('{0},{1},{2},{3},\n'.format(side, position_status, profit, created_at))

    def get_all(self):
        return self.TradeHistory.select().execute().fetchall()

    def get_yesterday(self):
        now = datetime.now()
        return self.get_by_day(now.replace(day=now.day-1))

    def get_by_day(self, day):
        from_date = day.replace(hour=0, minute=0)
        to_date = day.replace(hour=23, minute=59)
        return self.TradeHistory.select().where(from_date <= self.TradeHistory.c.created_at <= to_date).execute().fetchall()

