from flask import Blueprint

from pybo.models import Post, User

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/users/<int:user_id>')
def read_report(user_id):
    user = User.Query.get_or_404(user_id)
    report_list = user.report
    return


@bp.route('/users/<int:user_id>')
def read_badge(user_id):
    user = User.Query.get_or_404(user_id)
    return
