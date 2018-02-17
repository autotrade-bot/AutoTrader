from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime, and_
from datetime import datetime
from pytz import timezone


class SQLiteStoreDriver():
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:password@mysql/autotrade?charset=utf8', echo=True)
        metadata = MetaData()
        metadata.bind = engine

        # menuテーブルの定義
        self.TradeHistory = Table(
          'trade_history', metadata,
          Column('id', Integer, primary_key=True),
          Column('trade_id', String(64)),
          Column('side', String(64)), # buy or sell
          Column('price', Integer),
          Column('position_status', String(64)), # open or close
          Column('profit', Integer),
          Column('collateral', Float),
          Column('created_at', DateTime, unique=True),
        )
        metadata.create_all()

    def put_trade_history(self, trade_id, side, price, positions, created_at):
        collateral = 0.0
        profit = 0.0
        if positions is None or len(positions) == 0:
            position_status = 'close'
        else:
            for p in positions:
                collateral += float(p.get('require_collateral'))
                profit += float(p.get('pnl'))
            position_status = positions.pop().get('side')
        self.TradeHistory.insert().execute(
                trade_id=trade_id,
                side=side,
                price=price,
                position_status=position_status,
                collateral=collateral,
                profit=profit,
                created_at=created_at.astimezone(timezone('Asia/Tokyo')))

    def get_all(self):
        return self.TradeHistory.select().execute().fetchall()

    def get_yesterday(self):
        now = datetime.now()
        return self.get_by_day(now.replace(day=now.day-1))

    def get_by_day(self, day):
        from_date = day.replace(hour=0, minute=0)
        to_date = day.replace(hour=23, minute=59)
        return self.TradeHistory.select().where(from_date <= self.TradeHistory.c.created_at <= to_date).execute().fetchall()
