from flask import Blueprint, redirect, url_for, request, jsonify
from datetime import datetime
from pybo import db

from pybo.models import Post, User, Badge

bp = Blueprint('post', __name__, url_prefix='/posts')


@bp.route('/list/', methods=['GET'])
def read_posts():
    post_list = Post.query.all()
    result = jsonify([post.serialize() for post in post_list])
    return result


@bp.route('/<int:post_id>/')
def read_post(post_id):
    post = Post.query.get(post_id)
    result = jsonify([post.serialize()])
    return result


@bp.route('/create/', methods=['POST'])
def create():
    params = request.get_json()
    subject = params['subject']
    content = params['content']
    address = params['address']
    user_id = params['user_id']

    created_date = datetime.now()

    # 이미지 키를 json으로 전달받아야 함.
    image_key = params['image_key']

    post = Post(subject=subject, content=content, created_date=created_date,
                address=address, image_key=image_key, reporter_id=user_id)
    db.session.add(post)
    db.session.commit()

    post_list = Post.query.order_by(Post.created_date.desc())
    user = User.query.get(user_id)
    user_post_list = post_list.filter(Post.reporter_id == user_id)
    if user_post_list.count() == 1:
        badge = Badge.query.get_or_404(1)
        user.badges.append(badge)
        db.session.commit()
    elif user_post_list.count() == 3:
        badge = Badge.query.get_or_404(2)
        user.badges.append(badge)
        db.session.commit()
    elif user_post_list.count() == 5:
        badge = Badge.query.get_or_404(3)
        user.badges.append(badge)
        db.session.commit()

    return jsonify(post.serialize())


@bp.route('/delete/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post.read_posts'))


@bp.route('/edit/<int:post_id>/', methods=['POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    params = request.get_json()
    post.subject = params['subject']
    post.content = params['content']
    post.address = params['address']
    image_key = params['image_key']

    post.image_key = image_key
    db.session.commit()
    result = jsonify([post.serialize()])
    return result


@bp.route('/search/', methods=['POST'])
def search():
    keyword = request.get_json()['keyword']
    post_list = Post.query
    if keyword:
        kw = '%%{}%%'.format(keyword)
        post_list = post_list\
            .join(User, Post.reporter_id == User.id)\
            .filter(Post.subject.ilike(kw) |
                    Post.content.ilike(kw) |
                    Post.address.ilike(kw) |
                    User.username.ilike(kw)).distinct()
    return jsonify([post.serialize() for post in post_list])

