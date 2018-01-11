from oslo_utils import importutils
from dateutil.parser import parse
import datetime
import json
class AutotradeWorker():
    def __init__(self):
        self.conf = self.load_conf('conf.json')
        self.drivers = self.load_driver(self.conf)

    def load_driver(self, conf):
        drivers = {}
        driver_info = conf['driver']
        for key, val in driver_info.items():
            drivers[key] = importutils.import_class(val)()
        return drivers

    def load_conf(self, conf_path):
        return json.load(open(conf_path))

    def execute(self):
        action_json = json.loads(self.drivers['strategy'].get_next_action(self.drivers['api']))
        if action_json.get("action") != "nothing":
            action, price, position, profit = self.drivers['api'].collect_data(action_json)
            self.drivers['store'].put_trade_history(action, price, position, profit, datetime.now())
            self.drivers['notification'].post(action, price, position, profit)
        return self.drivers['api'].execute(action_json)

    def test(self):
        action_json = '{"action": "buy", "amount": "5000"}'
        self.drivers['api'].execute(json.loads(action_json))

worker = AutotradeWorker()
print(worker.execute())
