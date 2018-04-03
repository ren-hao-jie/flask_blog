#! /env python
# _*_ coding:utf8 _*_
# @author:Ren

from ...form import *
from ...models import *
from . import blog_blueprint

from flask import current_app, redirect, flash, url_for, request, render_template, Blueprint, g
from flask_login import login_required, logout_user, login_user, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity


@blog_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = request.args.get('next')

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        user = Users.query.filter_by(email=email).one()
        login_user(user, remember)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        flash(u"登录成功！", category='success')
        return redirect(next_url or url_for('.setting') or url_for('blog.index'))

    return render_template('blog.login.html', form=form)


# 登出
@blog_blueprint.route('/logout')
@login_required
def logout():
    next_url = request.args.get('next')
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash(u"注销成功！", category="success")
    return redirect(next_url or url_for('blog.index'))


# 注册
@blog_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('blog.register.html')


# 设置
@blog_blueprint.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template('blog.profile.html')