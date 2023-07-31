from flask import Blueprint, render_template

from pybo.models import Post

bp = Blueprint('post', __name__, url_prefix='/posts')


@bp.route('/list/')
def read_posts():
    post_list = Post.query.order_by(Post.created_date.desc())
    return render_template('post/post_list.html', post_list=post_list)


@bp.route('/<int:post_id>/')
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/post_detail.html', post=post)


