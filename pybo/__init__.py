from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
import os
import pymysql #pip install pymysql


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app(test_config = None):
    app = Flask(__name__)
    # app.config.from_object(config)
    # app.config['UPLOAD_FOLDER'] = os.getcwd() + '/'
    app.config.from_envvar('APP_CONFIG_FILE')
    app.config['JSON_AS_ASCII'] = False

    pymysql.install_as_MySQLdb()

    # MySQL 데이터베이스 URL 설정
    # app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        app.config.from_pyfile("../config.py")
    else:
        app.config.update(test_config)


# 블루 프린트
    from .views import main_views, auth_views, post_views, admin_views, mypage_views, detect_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(post_views.bp)
    app.register_blueprint(admin_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(detect_views.bp)

    return app


if __name__ == '__main__':
    app = create_app()  # 애플리케이션을 생성합니다.
    app.run(host='0.0.0.0', port=80)  # 0.0.0.0 주소에서 80 포트로 애플리케이션을 실행합니다.
