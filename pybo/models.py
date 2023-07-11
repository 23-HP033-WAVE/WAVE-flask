from pybo import db


report_post = db.Table(
    'report_post',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), primary_key=True)
)

process_post = db.Table(
    'process_post',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), primary_key=True)
)

get_badge = db.Table(
    'get_badge',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey(
        'badge.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pnum = db.Column(db.String(13), unique=True, nullable=False)
    location = db.Column(db.String(30), nullable=True)
    admin = db.Column(db.Boolean, default=False)
    report = db.relationship('User', secondary=report_post, backref=db.backref('report_post_set'))
    process = db.relationship('User', secondary=process_post, backref=db.backref('process_post_set'))
    badges = db.relationship('Badge', secondary=get_badge, backref=db.backref('badges_set'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    modified_date = db.Column(db.DateTime(), nullable=True)
    address = db.Column(db.String(100), nullable=False)


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badgename = db.Column(db.String(120), nullable=False)

