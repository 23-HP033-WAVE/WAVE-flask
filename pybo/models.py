from pybo import db

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
    process = db.relationship('Post', secondary=process_post, backref=db.backref('process_post_set'))
    badges = db.relationship('Badge', secondary=get_badge, backref=db.backref('badges_set'))
    user_img = db.Column(db.String(254), nullable=True) #유저 이미지 추가

    def serialize(self):  # 이것이 직렬화하여 json형태로 한것이다.
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'pnum': self.pnum,
            'location': self.location,
            'admin': self.admin,
            'process': [post.serialize() for post in self.process],
            'badges': [badge.serialize() for badge in self.badges],
            'user_img': self.user_img,
        }


    def serialize(self):  # 이것이 직렬화하여 json형태로 한것이다.
        return {
            'id': self.id,
            'username':self.username,
            'password': self.password,
            'email':self.email,
            'pnum':self.pnum,
            'location':self.location,
            'admin':self.admin,
            'process': [post.serialize() for post in self.process],
            'badges': [badge.serialize() for badge in self.badges],
            'user_img':self.user_img,
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=True)
    modified_date = db.Column(db.DateTime(), nullable=True)
    processed_date = db.Column(db.DateTime(), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    reporter = db.relationship('User', backref=db.backref('post_set'))
    image_key = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'content': self.content,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S') if self.created_date else None,
            'modified_date': self.modified_date.strftime('%Y-%m-%d %H:%M:%S') if self.modified_date else None,
            'processed_date': self.processed_date.strftime('%Y-%m-%d %H:%M:%S') if self.processed_date else None,
            'address': self.address,
            'reporter_id': self.reporter_id,
            'image_key': self.image_key,
        }


    def serialize(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'content': self.content,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S') if self.created_date else None,
            'modified_date': self.modified_date.strftime('%Y-%m-%d %H:%M:%S') if self.modified_date else None,
            'processed_date': self.processed_date.strftime('%Y-%m-%d %H:%M:%S') if self.processed_date else None,
            'address': self.address,
            'reporter_id': self.reporter_id,
            'image_key': self.image_key,
        }


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badgename = db.Column(db.String(120), nullable=False)


    def serialize(self):
        return {
            'id': self.id,
            'badgename':self.badgename,
        }
