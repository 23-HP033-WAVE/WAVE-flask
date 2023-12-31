from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, FileField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    username=StringField('아이디',validators=[DataRequired(),Length(min=3, max=25)])
    password1=PasswordField('비밀번호',validators=[DataRequired(),EqualTo('password2','비밀번호가 일치하지 않습니다.')])
    password2=PasswordField('비밀번호확인',validators=[DataRequired()])
    email=EmailField('이메일',[DataRequired(),Email()])
    pnum=StringField('전화번호',validators=[DataRequired()])
    admin = IntegerField('관리자', validators=[DataRequired()])


class UserLoginForm(FlaskForm):
    username=StringField('아이디',validators=[DataRequired(),Length(min=3,max=25)])
    password=PasswordField('비밀번호',validators=[DataRequired()])


class UserModifyForm(FlaskForm): #회원 정보 수정 form
    username=StringField('이름',validators=[DataRequired(),Length(min=3,max=25)])
    email=EmailField('이메일',[DataRequired(),Email()])
    pnum=StringField('전화번호',validators=[DataRequired()])
    location=StringField('주활동지역',validators=[DataRequired()])


class PostForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    image = FileField('사진')
    address = StringField('위치')

