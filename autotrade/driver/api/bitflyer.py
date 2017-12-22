import pybitflyer
import os

class BitflyerApiDriver():

    def execute(self, strategy_result):
        getattr(self, strategy_result.get('action'))(strategy_result.get('amount'))
    
    def buy(self, amount):
        currency = "BTC"
        api = pybitflyer.API(api_key=os.env['BITFLYER_API_KEY'], api_secret=os.env['BITFLYER_API_SECRET'])
        api.sendchildorder(product_code="%s_JPY" % currency,
                       child_order_type="MARKET",
                       side="BUY",
                       size=self.jpy_to_size(currency, amount),
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return
    
    def sell(self, amount):
        currency = "BTC"
        api = pybitflyer.API(api_key=os.env['BITFLYER_API_KEY'], api_secret=os.env['BITFLYER_API_SECRET'])
        api.sendchildorder(product_code="%s_JPY" % currency,
                       child_order_type="MARKET",
                       side="SELL",
                       size=amount,
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return

    def nothing(self):
        pass
    
    def jpy_to_size(self, currency, price):
        api = pybitflyer.API()
        ticker =  api.ticker(product_code="%s_JPY" % currency)
        return price / ticker['best_bid']
