from autotrade.utils import Utils
import os

class API():


    def __init__(self):
        self.utils = Utils()
        self.conf = self.utils.load_conf(os.environ.get('CONF_PATH'))
        self.drivers = self.utils.load_driver(self.conf)

    def instruct(self, ins_type):
        self.conf['instruct'] = ins_type
        self.utils.save_conf(self.conf)
    
    def free(self):
        if self.conf.get('instruct'):
            self.conf['instruct'] = None
            self.utils.save_conf(self.conf)

    def close(self):
        self.drivers['api'].close()

    def reverse(self):
        is_reverse = self.conf.get('is_reverse')
        if type(is_reverse) == bool:
            self.conf['is_reverse'] = not is_reverse
        else:
            self.conf['is_reverse'] = True
        self.utils.save_conf(self.conf)

