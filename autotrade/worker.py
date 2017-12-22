from oslo_utils import importutils
import json
class AutotradeWorker():
    def __init__(self):
        pass

    def load_driver(self, conf):
        drivers = {}
        driver_info = conf['driver']
        for key, val in driver_info.items():
            drivers[key] = importutils.import_module(val)
        return drivers

    def start(self):
        conf = self.load_conf('conf.json')
        drivers = self.load_driver(conf)
        print(drivers)

    def load_conf(self, conf_path):
        return json.load(open(conf_path))


worker = AutotradeWorker()
worker.start()
