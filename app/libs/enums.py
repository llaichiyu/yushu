#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: pauline.lee
@contact: Pauline.Y.Li@outlook.com
@site: https://github.com/llaichiyu/
@file: enums.py
@time: 2023/2/2 10:17

"""
from enum import Enum


class PendingStatus(Enum):
    waiting = 1
    success = 2
    reject = 3
    redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {cls.waiting: {'requester': '等待对方邮寄', 'gifter': '等待你邮寄'},
                   cls.reject: {'requester': '对方已拒绝', 'gifter': '你已拒绝'},
                   cls.redraw: {'requester': '你已撤销', 'gifter': '对方已撤销'},
                   cls.success: {'requester': '对方已邮寄', 'gifter': '你已邮寄，交易完成'}}
        return key_map[status][key]
