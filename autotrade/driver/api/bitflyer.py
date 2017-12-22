import pybitflyer
import os

class BitflyerFxApiDriver():

    def get_balance(self):
        api = pybitflyer.API(api_key=os.environ['API_KEY'], api_secret=os.environ['API_SECRET'])
        result = {}
        positions = api.getpositions(product_code="FX_BTC_JPY")
        collateral = api.getcollateral()
        if len(positions) > 0:
            pos = positions.pop()
            result["BTC"] = pos['size']
            result["JPY"] = 0.0
        else:
            result["BTC"] = 0.0
            result["JPY"] = collateral['collateral']
        return result

    def execute(self, strategy_result):
        return getattr(self, strategy_result.get('action'))(strategy_result.get('amount'))
    
    def buy(self, amount):
        api = pybitflyer.API(api_key=os.env['API_KEY'], api_secret=os.env['API_SECRET'])
        r = api.sendchildorder(product_code="FX_BTC_JPY",
                       child_order_type="MARKET",
                       side="BUY",
                       size=self.jpy_to_size("FX_BTC", amount),
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return r.status_code
    
    def sell(self, amount):
        api = pybitflyer.API(api_key=os.env['API_KEY'], api_secret=os.env['API_SECRET'])
        r = api.sendchildorder(product_code="FX_BTC_JPY",
                       child_order_type="MARKET",
                       side="SELL",
                       size=amount,
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return r.status_code

    def nothing(self):
        print("nothing")
        return 200
    
    def jpy_to_size(self, currency, price):
        api = pybitflyer.API()
        ticker =  api.ticker(product_code="%s_JPY" % currency)
        return price / ticker['best_bid']

class BitflyerApiDriver():

    def get_balance(self):
        api = pybitflyer.API(api_key=os.environ['API_KEY'], api_secret=os.environ['API_SECRET'])
        result = {}
        for balance in api.getbalance():
            result[balance.get("currency_code")] = balance.get("available")
        return result

    def execute(self, strategy_result):
        return getattr(self, strategy_result.get('action'))(strategy_result.get('amount'))
    
    def buy(self, amount):
        api = pybitflyer.API(api_key=os.env['API_KEY'], api_secret=os.env['API_SECRET'])
        r = api.sendchildorder(product_code="FX_BTC_JPY",
                       child_order_type="MARKET",
                       side="BUY",
                       size=self.jpy_to_size("FX_BTC", amount),
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return r.status_code
    
    def sell(self, amount):
        api = pybitflyer.API(api_key=os.env['API_KEY'], api_secret=os.env['API_SECRET'])
        r = api.sendchildorder(product_code="FX_BTC_JPY",
                       child_order_type="MARKET",
                       side="SELL",
                       size=amount,
                       minute_to_expire=10000,
                       time_in_force="GTC"
                       )
        return r.status_code

    def nothing(self):
        print("nothing")
        return 200
    
    def jpy_to_size(self, currency, price):
        api = pybitflyer.API()
        ticker =  api.ticker(product_code="%s_JPY" % currency)
        return price / ticker['best_bid']
