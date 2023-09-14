from flask import Flask, Blueprint, render_template, redirect, url_for, g, request, jsonify
from pybo.s3_helper import save_to_s3
from pybo.forms import PostForm
from datetime import datetime

from pybo import db
from pybo.models import Post, User, Badge
from pybo.views.auth_views import login_required

bp = Blueprint('post', __name__, url_prefix='/posts')
app=Flask(__name__)
@bp.route('/list/', methods=['GET'])
def read_posts():
    post_list = Post.query.all()
    result = jsonify([post.serialize() for post in post_list])
    # return render_template('post/post_list.html', post_list=post_list)
    return result

@bp.route('/create/', methods=['POST'])
def create():
    subject = request.json['subject']
    content = request.json['content']
    image = request.json['image']
    address = request.json['address']
    user = 1
    if image:
        image_key = save_to_s3(image, app.config['AWS_BUCKET_NAME'])
    else:
        image_key = None
    post = Post(subject=subject, content=content, image_key=image_key, address=address,
                reporter_id=user, created_date=datetime.now())
    db.session.add(post)
    db.session.commit()

    return jsonify(post.serialize())
# app = Flask(__name__)
#
# @bp.route('/list/')
# def read_posts():
#     post_list = Post.query.order_by(Post.created_date.desc())
#     return render_template('post/post_list.html', post_list=post_list)
#
#
# @bp.route('/<int:post_id>/')
# def read_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post/post_detail.html', post=post)
#
#
# @login_required
# @bp.route('/create', methods=['GET', 'POST'])
# def create():
#     form = PostForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         subject = form.subject.data
#         content = form.content.data
#         image = form.image.data
#         address = form.address.data
#         user = g.user
#
#         if image:
#             image_key = save_to_s3(image, app.config['AWS_BUCKET_NAME'])
#         else:
#             image_key = None
#
#         post = Post(subject=subject, content=content, image_key=image_key, address=address,
#                     reporter_id=user.id, created_date=datetime.now())
#         db.session.add(post)
#         db.session.commit()
#         post_list = Post.query.order_by(Post.created_date.desc())
#         return render_template('post/post_list.html', post_list=post_list)
#
#     return render_template('post/create.html', form=form)
#
#
# @bp.route('/edit/<int:post_id>/', methods=['GET', 'POST'])
# def edit(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = PostForm(obj=post)
#     if request.method == 'POST' and form.validate_on_submit():
#         post.subject = form.subject.data
#         post.content = form.content.data
#         image = form.image.data
#         post.address = form.address.data
#
#         if image:
#             image_key = save_to_s3(image, app.config['AWS_BUCKET_NAME'])
#             post.image_key = image_key
#
#         db.session.commit()
#         return render_template('post/post_detail.html', post=post)
#
#     return render_template('post/edit.html', form=form, post=post)
#
#
#
