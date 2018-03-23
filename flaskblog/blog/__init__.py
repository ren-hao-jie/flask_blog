#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2018/3/22.10:57

from flask import (Blueprint,render_template,redirect,
                   request,flash,url_for,session,current_app,g)
from flask_login import login_user,logout_user,current_user,login_required
from ..models.db import db

# 定义蓝图
blog_blueprint = Blueprint('blog',  __name__,template_folder='templates',static_folder='static',url_prefix='/blog')

@blog_blueprint.before_request
def before_request():
    g.user = current_user
    g.db = db

@blog_blueprint.after_request
def after_request(response):
    return response

@blog_blueprint.teardown_request
def teardown_request(excetption):
    g.db.session.romove()

@blog_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('blog.404.html'),404

@blog_blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('blog.500.html'),500