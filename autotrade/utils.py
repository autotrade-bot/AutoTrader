import json
from oslo_utils import importutils

class Utils():

    def load_driver(self, conf):
        drivers = {}
        driver_info = conf['driver']
        for key, val in driver_info.items():
            drivers[key] = importutils.import_class(val)(conf)
        self.drivers = drivers
        return drivers

    def load_conf(self, conf_path):
        self.conf = json.load(open(conf_path))
        return self.conf

    def check_limit_close(self, action_json):
        trade_data = self.drivers['api'].collect_data()
        profit = trade_data.get("profit")
        positions = trade_data.get("positions")
        require_collateral = trade_data.get("require_collateral")
        if positions is not None and len(positions) != 0:
            profit_rate = profit / require_collateral
            if profit and (profit_rate >= 0.03 or profit <= -0.01):
                amount = 0.0
                action = positions[0].get('side').lower()
                for p in positions:
                    amount += float(p.get('size'))
                result = {'action': self.reverse_action(action), 'amount': round(amount, 4), 'limit': True}
                return result
        return action_json

    def reverse_action(self, action):
        if action == 'buy':
            return 'sell'
        elif action == 'sell':
            return 'buy'
        else:
            return 'nothing'
