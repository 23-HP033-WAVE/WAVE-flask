from flask import Flask, Blueprint, redirect, url_for, request, jsonify
from pybo.s3_helper import save_to_s3
from datetime import datetime

from pybo import db
from pybo.models import Post, User, Badge
from pybo.views.auth_views import login_required

bp = Blueprint('post', __name__, url_prefix='/posts')
app = Flask(__name__)


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
#
#


@bp.route('/create/', methods=['POST'])
def create():
    params = request.get_json()
    subject = params['subject']
    content = params['content']
    image = params['image']
    address = params['address']
    # user = User.query.get(g.user.id)
    user_id = params['user_id']
    if image:
        image_key = save_to_s3(image, app.config['AWS_BUCKET_NAME'])
    else:
        image_key = None

    created_date = datetime.now()

    post = Post(subject=subject, content=content, created_date=created_date,
                address=address, image_key=image_key, reporter_id=user_id)
    db.session.add(post)
    db.session.commit()

    post_list = Post.query.order_by(Post.created_date.desc())
    user = User.query.get(user_id)
    user_post_list = post_list.filter(Post.reporter == user)
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


@login_required
@bp.route('/delete/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # if g.user.id != post.reporter_id:
    #     return "권한이 없습니다", 403
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
    image = params['image']
    if image:
        image_key = save_to_s3(image, app.config['AWS_BUCKET_NAME'])
        post.image_key = image_key
    db.session.commit()
    result = jsonify([post.serialize()])
    return result

