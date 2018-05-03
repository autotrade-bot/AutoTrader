# -*- coding:utf-8 -*-
from bottle import route, run
from autotrade.lib.api import API
api = API()

@route('/instruct/<ins_type>')
def instruct(ins_type):
    return api.instruct(ins_type)

@route('/reverse')
def reverse():
    return api.reverse()

@route('/free')
def free():
    return api.free()

@route('/close')
def close():
    return api.close()

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)
