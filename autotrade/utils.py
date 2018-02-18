import json
from oslo_utils import importutils
from dateutil.parser import parse

class Utils():

    def load_driver(self, conf):
        drivers = {}
        driver_info = conf['driver']
        for key, val in driver_info.items():
            drivers[key] = importutils.import_class(val)()
        return drivers

    def load_conf(self, conf_path):
        return json.load(open(conf_path))

    def limit_close():
       trade_id, price, positions, profit, require_collateral = api_driver.collect_data()
       if positions is not None and len(positions) != 0:
           if profit and (profit >= self.__limit_profit or profit <= self.__limit_loss):
               amount = 0.0
               action = positions[0].get('side').lower()
               for p in positions:
                   amount += float(p.get('size'))
               if action == 'sell':
                   action = 'buy'
               elif action == 'buy':
                   action = 'sell'
               result = {'action': action, 'amount': round(amount, 4)}
               return json.dumps(result)
