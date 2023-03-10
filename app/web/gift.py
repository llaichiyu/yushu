#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2023/1/7 13:43
# @Author  : paulinelee
# @Site    : https://github.com/llaichiyu/
# @File    : gift.py
# @Software: PyCharm
from flask import current_app, flash, render_template, redirect, url_for

from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.view_models.trade import MyTrades
from app.web import web
from flask_login import login_required, current_user
from app.models.base import db
from app.models.gift import Gift


@web.route('/my/gifts')
@login_required
def my_gifts():
    """
    1.current_user.id
    2.当前用户的赠送清单 Gift
    3.求赠送清单的总数 Gift.total
    4.每本书的详情 book.detail
    5.每本书对应的几个人想要  gift.isbn == wish.isbn
    :return:
    """
    uid = current_user.id
    my_gift_list = Gift.get_user_gift_list(uid=uid)
    isbn_list = [gift.isbn for gift in my_gift_list]
    wishes_list = Gift.get_wishs_count(isbn_list=isbn_list)
    view_model_gifts = MyTrades(trades_of_mine=my_gift_list, trade_count_list=wishes_list)
    return render_template('my_gifts.html', gifts=view_model_gifts.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)

    else:
        flash('这本书已添加到你的赠送清单或心愿清单，请不要重复添加')
    return redirect(url_for(endpoint='web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    dirft = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.waiting).first()
    if dirft:
        flash("您的这个礼物正处于交易状态，请先前往鱼漂完成交易")
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
