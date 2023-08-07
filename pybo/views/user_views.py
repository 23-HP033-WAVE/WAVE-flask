from flask import Blueprint, render_template

from pybo.models import Post, User

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/<int:user_id>')
def read_report(user_id):
    user = User.query.get_or_404(user_id)
    report_list = user.post_set
    return render_template('user/mypost_list.html', post_list=report_list)


# @bp.route('/users/<int:user_id>')
# def read_badge(user_id):
#     user = User.Query.get_or_404(user_id)
#     return
