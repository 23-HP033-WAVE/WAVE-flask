from flask import Blueprint, request, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from pybo import db

from pybo.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=['POST'])
def signup():
    params = request.get_json()
    username = params['username']
    password = generate_password_hash(params['password'])
    email = params['email']
    pnum = params['pnum']

    admin = params['admin']
    user_img = params['user_img']

    location = params['location']
    user = User(username=username, password=password,
                location=location, email=email, pnum=pnum, admin=admin, user_img=user_img)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())
    # return 200


@bp.route('/login/', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'message': '존재하지 않는 사용자입니다.'}), 404

        if not check_password_hash(user.password, password):
            return jsonify({'message': '비밀번호가 올바르지 않습니다.'}), 401

        session.clear()
        session['user_id'] = user.id

        return jsonify({'message': '로그인에 성공했습니다.'})

    except Exception as e:
        return jsonify({'message': str(e)})


@bp.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return jsonify({'message': '로그아웃에 성공했습니다.'})


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


