from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.datastructures import MultiDict

from app import db
from app.models import Post
from app.post import bp
from app.post.forms import PostCreateForm, PostEditForm


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostCreateForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(name=form.name.data).first()
        if post:
            flash('Пост с таким названием уже существует')
            return redirect(url_for('post.create'))
        post = Post(name=form.name.data, text=form.text.data)
        post.set_timestamp()  # Установка времени создания поста
        if current_user.role == 1:
            post.set_level(1)
        else:
            post.set_level(form.level.data)  # Установка уровня секретности для поста
        post.set_author(current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Пост создан!')
        return redirect(url_for('post.list'))
    return render_template('post/post_create.html', title='Новый пост', form=form, role=current_user.role)


@bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        flash('Пост не найден')
        return redirect(url_for('post.list'))

    if current_user.role != post.level:
        flash('Нет прав для редактирования')
        return redirect(url_for('post.list'))

    form = PostEditForm(MultiDict([('id', post.id), ('name', post.name), ('text', post.text)]))

    if request.form.get('name'):
            post.set_changed_status()
            post.set_name(request.form.get("name"))
            post.set_text(request.form.get("text"))

            db.session.commit()
            flash('Пост успешно изменен')
            return redirect(url_for('post.list'))
    return render_template('post/post_edit.html', title='Изменение поста', form=form, post=post, role=current_user.role)


@bp.route('/list')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    if current_user.role == 0:
        posts = Post.query.filter_by(level=0).order_by(Post.timestamp.desc()).paginate(page, 12, False)
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 12, False)
    next_url = url_for('post.list', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('post.list', page=posts.prev_num) if posts.has_prev else None
    return render_template('post/post_list.html', title='Список всех постов', posts=posts.items, next_url=next_url,
                           prev_url=prev_url, role=current_user.role)


@bp.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        flash('Пост не найден')
        return redirect(url_for('post.list'))

    if current_user.role != post.level:
        flash('Нет прав для удаления')
        return redirect(url_for('post.list'))

    db.session.delete(post)
    db.session.commit()
    flash('Пост успешно удален')
    return redirect(url_for('post.list'))
