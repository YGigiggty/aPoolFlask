from datetime import datetime,timezone,timedelta
import jwt
from flask import current_app
from sqlalchemy import Index
from werkzeug.security import generate_password_hash, check_password_hash
from extends import db, TSVector, NameTsvector
from flask_login import UserMixin, AnonymousUserMixin
from apps import login_manager
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    __tablename__ ='users'
    id =db.Column(db.Integer,primary_key =True,autoincrement =True)
    user_name =db.Column(db.String(20),nullable = False,unique=True)
    password_hash =db.Column(db.String(125),nullable =False)
    user_email =db.Column(db.String(80),nullable =False,unique=True)
    user_phone =db.Column(db.String(300),nullable =False,unique=True)
    rdatetime =db.Column(db.DateTime,default = datetime.now)
    avatar_bytea = db.Column(db.LargeBinary(length=3600))
    avatar_type =db.Column(db.String(50),nullable=True)
    last_seen = db.Column(db.DateTime,default = datetime.utcnow)
    confirmed =db.Column(db.Boolean,default = False)
    role_id =db.Column(db.Integer,db.ForeignKey("roles.id"))
    posts =db.relationship('Post',backref="author",lazy="dynamic")



    def __init__(self,**kwargs) -> None:#赋予角色
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.user_email =="hongmingha886@gmial.com":
                self.role =Role.query.filter_by(name ='Administrator').first()
            if self.role is None:
                self.role =Role.query.filter_by(default =True).first()

    def generate_confirmation_token(self,expiration =3600):#生成令牌，时间为3600s
            confirm_token =jwt.encode({
                "confirm":self.id,
                "exp":datetime.now(tz=timezone.utc)+timedelta(seconds=expiration)
            },
                current_app.secret_key,
                algorithm="HS256"
            )
            return confirm_token

    def confirm(self,token):#确认令牌
        try:
            data =jwt.decode(
                token,
                current_app.secret_key,
                leeway=timedelta(seconds=100),
                algorithms=["HS256"]
            )
        except:
                return  False
        if data.get("confirm") !=self.id:
            return False
        self.confirmed =True
        db.session.add(self)
        return  True

    def generate_reset_token(self,expiration=3600):#生成重置密码令牌
        reset_token=jwt.encode({
            "reset":self.id,
            "exp":datetime.now(tz=timezone.utc)+timedelta(seconds=expiration),
        },
        current_app.secret_key,
            algorithm="HS256"
        )
        return  reset_token

    @staticmethod
    def confirm_reset(reset_token,newPWD):#确认重置令牌正确
        try:
            data=jwt.decode(
                reset_token,
                current_app.secret_key,
                leeway=timedelta(seconds=100),
                algorithms=["HS256"]
            )
        except:
            return  False
        # if data.get("reset") !=self.id:
        #     return  False
        # else:
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password=newPWD
        db.session.add(user)
        return True
    @property
    def password(self):#调用未加密密码将报警
        raise AttributeError("password is not a realable attribute")

    @password.setter
    def password(self,password: str):#密码加密
        self.password_hash =generate_password_hash(password)

    def verify_password(self,password):#密码验证
        return check_password_hash(self.password_hash,password)

    def can(self,perm):#
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):#检测是否为管理员
        return self.can(Permission.ADMIN)

    class AnonyMousUser(AnonymousUserMixin):
        def can(self,permission):
            return  False
        def is_admin(self):
            return  False
    login_manager.anonymous_user =AnonyMousUser


class Role(db.Model):
    __tablename__ ='roles'
    id =db.Column(db.Integer,primary_key =True,autoincrement =True)
    name =db.Column(db.String(20),unique =True)
    default =db.Column(db.Boolean,default =False,index =True)
    permissions =db.Column(db.Integer)
    users =db.relationship("User",backref="role",lazy='dynamic')
    
    def __int__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions =0

    def add_permission(self,perm):#添加权限
        if not self.has_permission(perm):
            self.permissions +=perm

    def remove_permission(self,perm):#移除权限
        if self.has_permission(perm):
            self.permissions -=perm

    def reset_permission(self):#重设权限
        self.permissions=0

    def has_permission(self,perm):#检查组合权限是否包含独立权限
        return self.permissions & perm ==perm
    
    @staticmethod
    def insert_roles():
        roles ={
            "User":[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE],
            "Moderator":[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE],
            "Administrator":[Permission.ADMIN,Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE]
        }
        default_Role ="User"
        for R in roles:
            role =Role.query.filter_by(name =R).first()
            if role is None:
                role =Role(name =R)
            role.reset_permission()
            for perm in roles[R]:
                role.add_permission(perm)
                role.default =(role.name ==default_Role)
                db.session.add(role)
        db.session.commit()

class Permission:
    FOLLOW =1#可关注其他用户
    COMMENT =2#可发表评论
    WRITE =4#可发布文章
    MODERATE =8#可增加其他用户权限
    ADMIN =16#可修改所以用户权限

def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector(exp)

class Post(db.Model):
    __tablename__ ='posts'

    id =db.Column(db.Integer,primary_key=True,autoincrement =True)
    body =db.Column(db.Text)
    auth_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    title =db.Column(db.String(20),nullable =False)
    timetamp =db.Column(db.DateTime,index =True,default =datetime.utcnow)
    fts = db.Column(TSVector(), db.Computed("to_tsvector(title)",persisted =True))
    __table_args__ = (Index('ix_post___ts_vector__',
                            fts, postgresql_using='gin'),)


