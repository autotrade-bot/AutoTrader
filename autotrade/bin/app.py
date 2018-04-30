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

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
