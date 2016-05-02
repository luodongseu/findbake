# coding: UTF-8

import config


def get_todos():
    return config.db.select('fb_test', order='id')


def new_todo(text):
    config.db.insert('fb_test', test=text)


def del_todo(id):
    config.db.delete('fb_test', where="id=$id", vars=locals())
