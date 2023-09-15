from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pybo.s3_helper import save_to_s3

from pybo import db
from pybo.models import User

bp = Blueprint('mypage', __name__, url_prefix='/mypage')
app = Flask(__name__)


@bp.route('/<int:user_id>/', methods=['GET'])
def read_report(user_id):
    user = User.query.get_or_404(user_id)
    report_list = user.post_set
    return jsonify([report.serialize() for report in report_list])


@bp.route('/modify/<int:userid>/', methods=['POST'])
def modify_user(userid): #회원정보 수정
    user = User.query.get_or_404(userid)
    params = request.get_json()
    # user.password = generate_password_hash(params['password'])
    user.location = params['location']
    user.username = params['username']
    user.email = params['email']
    user.pnum = params['pnum']
    image = params['image']
    if image:
        user_img = save_to_s3(image, app.config['AWS_BUCKET_NAME'])
        user.user_img = user_img
    db.session.commit()
    return jsonify([user.serialize()])


@bp.route('/delete/<int:userid>/', methods=['DELETE'])
def delete_user(userid): #회원 탈퇴
    user=User.query.get_or_404(userid)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '탈퇴 성공'}), 200


@bp.route('/badges/<int:user_id>/')
def read_badge(user_id):
    user = User.query.get_or_404(user_id)
    badge_list = user.badges
    return jsonify([badge.serialize() for badge in badge_list])