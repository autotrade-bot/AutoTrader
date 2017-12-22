import pybitflyer
import os

class NoopApiDriver():

    def get_balance(self):
        api = pybitflyer.API(api_key=os.environ['API_KEY'], api_secret=os.environ['API_SECRET'])
        result = {}
        for balance in api.getbalance():
            result[balance.get("currency_code")] = balance.get("available")
        return result

    def execute(self, strategy_result):
        print(strategy_result)
        return 200
    
    def nothing(self):
        print("nothing")
        return 200
