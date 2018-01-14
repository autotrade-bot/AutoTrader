from pubnub.callbacks import SubscribeCallback
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_
from datetime import datetime
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from pubnub.pnconfiguration import PNReconnectionPolicy

config = PNConfiguration()
config.subscribe_key = 'sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f'
config.reconnect_policy = PNReconnectionPolicy.LINEAR
pubnub = PubNubTornado(config)

from tornado import gen
from dateutil.parser import parse
from pytz import timezone
class SQLiteStoreDriver():
    def __init__(self):
        engine = create_engine('sqlite:///ohlc.db', echo=True)
        metadata = MetaData()
        metadata.bind = engine
        
        # menuテーブルの定義
        self.OHLC = Table(
          'ohlc', metadata,
          Column('id', Integer, primary_key=True),
          Column('open', String), # buy or sell
          Column('high', Integer),
          Column('low', String), # open or close
          Column('close', Integer),
          Column('created_at', DateTime),
        )
        metadata.create_all()

    def put(self, op, high, low, cl, created_at):
        self.OHLC.insert().execute(
                open=op, 
                high=high,
                low=low,
                close=cl,
                created_at=created_at)



@gen.coroutine
def main(channels):
    sqlite = SQLiteStoreDriver()
    class BitflyerSubscriberCallback(SubscribeCallback):
        price_list = []
        pre_d = None
        def presence(self, pubnub, presence):
            pass  # handle incoming presence data

        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass  # This event happens when radio / connectivity is lost

            elif status.category == PNStatusCategory.PNConnectedCategory:
                # Connect event. You can do stuff like publish, and know you'll get it.
                # Or just use the connected event to confirm you are subscribed for
                # UI / internal notifications, etc
                pass
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # Happens as part of our regular operation. This event happens when
                # radio / connectivity is lost, then regained.
            elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
                pass
                # Handle message decryption error. Probably client configured to
                # encrypt messages and on live data feed it received plain text.

        def message(self, pubnub, message):
            # Handle new message stored in message.message
            # メインの処理はここで書きます
            # 登録したチャンネルからメッセージ(価格の変化など)がくるたび、この関数が呼ばれます
            # {'id': 113370452, 'side': 'SELL', 'price': 1922595.0, 'size': 0.1, 'exec_date': '2018-01-14T13:41:19.0924133Z', 'buy_child_order_acceptance_id': 'JRF20180114-224113-653741', 'sell_child_order_acceptance_id': 'JRF20180114-134118-859029'}
            for m in message.message:
                d = parse(m.get('exec_date')).astimezone(timezone('Asia/Tokyo'))
                # print('{0},{1},{2}'.format(d, m.get('side'), m.get('price')))
                if self.pre_d is not None and self.pre_d.minute < d.minute:
                    sqlite.put(self.price_list[0], max(self.price_list), min(self.price_list), self.price_list[-1], self.pre_d)
                    print(self.price_list[0], max(self.price_list), min(self.price_list), self.price_list[-1])
                    self.price_list = []
                else:
                    self.price_list.append(m.get('price'))
                self.pre_d = d


    listener = BitflyerSubscriberCallback()
    pubnub.add_listener(listener)
    pubnub.subscribe().channels(channels).execute()

if __name__ == '__main__':
    channels = [
        'lightning_executions_FX_BTC_JPY',
    ]
    main(channels)
    pubnub.start()
