from autotrade.utils import Utils
import datetime
class AutotradeWorker():
    def __init__(self):
        self.utils = Utils()
        self.conf = self.utils.load_conf('conf.json')
        self.drivers = self.utils.load_driver(self.conf)

    def execute(self):
        #action_json = self.utils.check_limit_close(self.drivers['strategy'].get_next_action(self.drivers['api']))
        action_json = self.drivers['strategy'].get_next_action(self.drivers['api'])
        trade_data = self.drivers['api'].collect_data()
        self.drivers['store'].put_trade_history(
                trade_id=trade_data.get('trade_id'),
                side=action_json.get("action"),
                price=trade_data.get("price"),
                positions=trade_data.get("positions"),
                profit=trade_data.get("profit"),
                created_at=datetime.datetime.now())
        return self.drivers['api'].execute(action_json)


worker = AutotradeWorker()
print(worker.execute())
