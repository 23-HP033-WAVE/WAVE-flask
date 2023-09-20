from flask import Flask, Blueprint, request, current_app
from pybo.s3_helper import save_to_s3, download_file_from_s3

from pybo.models import Post


bp = Blueprint('image', __name__, url_prefix='/image')
app = Flask(__name__)


@bp.route('/', methods=['POST'])
def image_upload():

    image = request.files['File']
    if image:
        image_key = save_to_s3(image, current_app.config['AWS_BUCKET_NAME'])
    else:
        image_key = None

    return image_key


@bp.route('/read/<int:post_id>')
def image_read(post_id):
    post = Post.query.getOr404(post_id)
    image_key = post.image_key
    if image_key:
        return download_file_from_s3(image_key, current_app.config['AWS_BUCKET_NAME'])
    else:
        return None
