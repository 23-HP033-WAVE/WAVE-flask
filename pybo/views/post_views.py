from flask import Blueprint

from pybo.models import Post, User

bp = Blueprint('post', __name__, url_prefix='/posts')


@bp.route('/')
def read_posts():
    unprocessed_post_list = Post.query.filter_by(admin=True)\
        .order_by(Post.created_date.desc()).all()
    return


@bp.route('/<int:post_id>')
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    return
