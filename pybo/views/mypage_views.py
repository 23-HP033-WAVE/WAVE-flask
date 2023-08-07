from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserModifyForm
from pybo.models import User

bp=Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/modify/<int:userid>/',methods=('GET','POST'))
def modify_user(userid): #회원정보 수정
    user = User.query.get_or_404(userid)
    if g.user != user:
        flash('수정권한이 없습니다.')
        return '%s %s' %(g.user.id, user.id)
    if request.method == 'POST':
        form = UserModifyForm()
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            return '%s %s' %(user.username,user.email)
    else:
        form=UserModifyForm(obj=user)
    return render_template('mypage/mypage_edit.html', form=form)

@bp.route('/delete/<int:userid>/')
def delete_user(userid): #회원 탈퇴
    user=User.query.get_or_404(userid)
    if g.user!=user:
        flash('탈퇴권한이 없습니다.')
        return redirect(url_for('main.index'))
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get(user_id)