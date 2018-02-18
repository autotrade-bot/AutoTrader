from autotrade.utils import Utils
import datetime
import json
class AutotradeWorker():
    def __init__(self):
        self.utils = Utils()
        self.conf = self.utils.load_conf('conf.json')
        self.drivers = self.utils.load_driver(self.conf)

    def execute(self):
        action_json = json.loads(self.drivers['strategy'].get_next_action(self.drivers['api']))
        trade_id, price, positions, profit, require_collateral = self.drivers['api'].collect_data()
        self.drivers['store'].put_trade_history(trade_id, action_json.get("action"), price, positions, profit, datetime.datetime.now())
        return self.drivers['api'].execute(action_json)


worker = AutotradeWorker()
print(worker.execute())
