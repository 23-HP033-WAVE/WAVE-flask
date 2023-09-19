#관리자 관련 api
from datetime import datetime
from flask import Blueprint, render_template, flash, g

from pybo import db
from pybo.models import Post

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/<int:post_id>/')
def process(post_id):
    post = Post.query.get_or_404(post_id)
    if g.user.admin != 1:
        flash('수정권한이 없습니다.')
    else:
        post.processed_date = datetime.now()
        g.user.process.append(post)
        db.session.commit()
    return render_template('post/post_detail.html', post=post)
