import os

BASE_DIR = os.path.dirname(__file__)


db = {
    'user': 'root',
    'password': 'kjy1234',
    'host': 'localhost',
    'port': '3306',
    'database': 'wave'
}

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SECRET_KEY="wave"

AWS_SECRET_KEY = "boJ2/7lWNGMetzZhCoQmoFgkK6GgxHrg7qD2WmE9"
AWS_BUCKET_NAME = 'wave-project-bucket'
AWS_ACCESS_KEY='AKIA2CHQWMCAFWQAUM7Q'
AWS_REGION='ap-northeast-2'