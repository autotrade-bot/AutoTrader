import sqlalchemy as sa
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime, and_
from sqlalchemy.orm import create_session
from datetime import datetime
from pytz import timezone

Base = declarative_base()

class TradeHistory(Base):
    __tablename__ = "trade_history"
    id = Column(Integer, primary_key=True)
    trade_id = Column(String(64))
    side = Column(String(64)) # buy or sell
    price = Column(Integer)
    position_status = Column(String(64)) # open or close
    profit = Column(Integer)
    collateral = Column(Float)
    created_at = Column(DateTime, unique=True)

class Profit(Base):
    __tablename__ = 'profits'
    trade_id = Column('trade_id', String(64),primary_key=True, unique=True)
    position_status = Column('position_status', String(64)) # open or close
    profit = Column('profit', Integer)
    collateral = Column('collateral', Float)
    created_at = Column('created_at', DateTime)
    closed_at = Column('closed_at', DateTime)

class SQLiteStoreDriver():
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:password@mysql/autotrade?charset=utf8', echo=True)
        metadata = MetaData()
        metadata.bind = engine
        self.session = create_session(bind=engine)
        metadata.create_all()

    def put_trade_history(self, trade_id, side, price, positions, profit, created_at):
        collateral = 0.0
        if positions is None or len(positions) == 0:
            position_status = 'close'
        else:
            for p in positions:
                collateral += float(p.get('require_collateral'))
            position_status = positions.pop().get('side')
        with self.session.begin():
           th = TradeHistory(
                    trade_id=trade_id,
                    side=side,
                    price=price,
                    position_status=position_status,
                    collateral=collateral,
                    profit=profit,
                    created_at=created_at.astimezone(timezone('Asia/Tokyo')))
           self.session.add(th)
           if collateral == 0:
               return
           prof = self.session.query(Profit).filter_by(trade_id=trade_id).one_or_none()
           if not prof:
               prof = Profit(trade_id=trade_id, position_status=position_status, profit=profit, collateral=collateral, created_at=datetime.now())
               self.session.add(prof)
           prof.profit = profit
           prof.closed_at = datetime.now()
        return

    def get_all(self):
        return self.TradeHistory.select().execute().fetchall()

    def get_yesterday(self):
        now = datetime.now()
        return self.get_by_day(now.replace(day=now.day-1))

    def get_by_day(self, day):
        from_date = day.replace(hour=0, minute=0)
        to_date = day.replace(hour=23, minute=59)
        return self.TradeHistory.select().where(from_date <= self.TradeHistory.c.created_at <= to_date).execute().fetchall()
