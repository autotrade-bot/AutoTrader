import pybitflyer
import os

class NoopApiDriver():

    def get_balance(self):
        api = pybitflyer.API(api_key=os.environ['API_KEY'], api_secret=os.environ['API_SECRET'])
        result = {}
        positions = api.getpositions(product_code="FX_BTC_JPY")
        collateral = api.getcollateral()
        print(positions)
        if len(positions) > 0:
            pos = positions.pop()
            result["BTC"] = pos['size']
            result["JPY"] = 0.0
        else:
            result["BTC"] = 0.0
            result["JPY"] = collateral['collateral']
        print(result)
        return result

    def execute(self, strategy_result):
        print(strategy_result)
        return 200
    
    def nothing(self):
        print("nothing")
        return 200
