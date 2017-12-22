import pybitflyer
import os

class BitflyerApiDriver():
    def buy(self, price=0):
        currency = "BTC"
        api = pybitflyer.API(api_key=os.env['BITFLYER_API_KEY'], api_secret=os.env['BITFLYER_API_SECRET'])
        api.sendchildorder(product_code="%s_JPY" % currency,
                       child_order_type="MARKET",
                       side="BUY",
                       size=self.jpy_to_size(currency, price),
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return
    
    def sell(self, size=0):
        currency = "BTC"
        api = pybitflyer.API(api_key=os.env['BITFLYER_API_KEY'], api_secret=os.env['BITFLYER_API_SECRET'])
        api.sendchildorder(product_code="%s_JPY" % currency,
                       child_order_type="MARKET",
                       side="SELL",
                       size=size,
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return
    
    
    def jpy_to_size(self, currency, price):
        api = pybitflyer.API()
        ticker =  api.ticker(product_code="%s_JPY" % currency)
        return price / ticker['best_bid']
