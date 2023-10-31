from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField,TextAreaField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from apps.models import User


class LoginForms(FlaskForm):#用户登录表单
    UserEmail =StringField(validators=[Email(),DataRequired(),Length(1,64)])
    UserPassword =PasswordField(validators=[DataRequired()])
    VerifyCode =StringField(validators=[DataRequired()])
    remember_me =BooleanField("记住我")
    submit=SubmitField("登录")


class RegisterForms(FlaskForm):#用户注册表单
    UserName =StringField(validators=[DataRequired(),Length(1,20)])
    UserEmail =StringField(validators=[Email(),Length(1,64),DataRequired()])
    PassWord =PasswordField(validators=[DataRequired(),EqualTo('configPassword',message="两次密码必须相同")])
    configPassword =PasswordField(validators=[DataRequired()])
    UserPhone =StringField(validators=[DataRequired()])
    submit =SubmitField("注册")

    def validate_username(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError("用户已经存在")


class EditProfile(FlaskForm):#用户修改资料表单
    avatarSubmit =FileField("选择文件")
    username = StringField("Real name",validators=[DataRequired(),Length(0,64)])
    userphone =StringField(validators=[DataRequired(),Length(0,64)])
    datasub =SubmitField("提交")

class changePWD(FlaskForm):#用户找回密码表单
    userEmail =StringField(validators=[DataRequired(),Email(),Length(1,64)])
    submit =SubmitField("提交")

class ResetPWD(FlaskForm):#重置密码表单
    NewPassword =PasswordField(validators=[DataRequired(),EqualTo("configPWD",message="两次密码必须相同")])
    configPWD=PasswordField(validators=[DataRequired()])
    submit =SubmitField("重置密码")

class EditPost(FlaskForm):
    Title =StringField(validators=[DataRequired(),Length(1,20)])
    body = TextAreaField("写点东西吧！",validators=[DataRequired()])
    submit =SubmitField("提交")

class Search(FlaskForm):
    goal =StringField(validators=[DataRequired()])
    ToSearch =SubmitField("搜索")
