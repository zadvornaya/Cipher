from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_manager
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Непарвильный логин или пароль')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title="Вход", form=form)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        if form.role.data:  # Установить уровень доступа преподавателя, если опция была выбрана
            user.set_teacher_role()
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрировались!')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', title='Регистрация', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
