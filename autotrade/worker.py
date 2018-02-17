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
        trade_id, price, positions, profit = self.drivers['api'].collect_data()
        self.drivers['store'].put_trade_history(trade_id, action_json.get("action"), price, positions, datetime.datetime.now())
        return self.drivers['api'].execute(action_json)

    def test(self):
        action_json = '{"action": "buy", "amount": "5000"}'
        self.drivers['api'].execute(json.loads(action_json))

worker = AutotradeWorker()
print(worker.execute())
