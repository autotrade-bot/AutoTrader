from oslo_utils import importutils
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
        action_json = self.drivers['strategy'].get_next_action(self.drivers['api'])
        import pdb; pdb.set_trace()
        self.drivers['api'].execute(json.loads(action_json))

worker = AutotradeWorker()
worker.execute()
