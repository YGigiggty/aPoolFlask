import io
from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file, make_response, session
from flask_login import login_user, login_required, current_user, logout_user

from apps.IdentifyingCode.Generate import get_verify_code
from apps.email import send_email
from apps.main.forms import RegisterForms, LoginForms, EditProfile, changePWD, ResetPWD, Search
from apps.models import User, Permission
import base64
from extends import db
from devtools import debug

user_bp = Blueprint("user",__name__)
@user_bp.route("/",endpoint="first_index")#首页
def first_looking():
    SearchForm =Search()
    return render_template("index.html",form =SearchForm)

@user_bp.route("/login",endpoint="user_login",methods=['GET','POST'])#用户登录
def user_login():
    loginForm =LoginForms()
    if loginForm.validate_on_submit():
            user_login = User.query.filter_by( user_email=loginForm.UserEmail.data).first()
            if session.get("image").lower() !=loginForm.VerifyCode.data.lower():
                flash("验证码出错！")
                return redirect(url_for("user.user_login"))
            if user_login is not None and user_login.verify_password(loginForm.UserPassword.data):
                login_user(user_login)
                next =request.args.get("next")
                if next is None or not next.startswith("/"):
                    next = url_for("user.first_index")
                return redirect(next)
            flash("邮箱或者密码出现错误！")
    return render_template("loogin.html",form =loginForm)

@user_bp.route("/code",endpoint="IDCode")#返回验证码图片
def generate_identifyCode():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = io.BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code

    return response

@user_bp.route("/register",endpoint="user_register",methods=['GET','POST'])#用户注册
def user_register():
    form =RegisterForms()
    if form.validate_on_submit():
            user_info =User(user_name=form.UserName.data,password =form.PassWord.data,user_email =form.UserEmail.data,user_phone =form.UserPhone.data)
            db.session.add(user_info)
            db.session.commit()
            token =user_info.generate_confirmation_token()
            send_email(user_info.user_email,"Confirm YOur Account","emailTxt/confirm",token =token,user =user_info)
            flash("请在确认账户后登录了")
            return redirect(url_for("user.user_login"))
    else:
        flash("请按正确格式填写！")
        redirect(url_for("user.user_register"))
    return  render_template('resi.html',form = form)


@user_bp.route("/space/<username>",methods=["POST","GET"])#用户中心
@login_required
def user_space(username):
    user = User.query.filter_by(user_name=username).first_or_404()
    return render_template("space.html",user =user)

@user_bp.route("/logout")#用户登出
@login_required
def user_out():
    logout_user()
    SearchForm = Search()
    return render_template("index.html",form=SearchForm)

@user_bp.route("/edit",methods=['POST','GET'],endpoint="userEdit")#用户修改资料
@login_required
def user_edit():
    editForm =EditProfile()
    if editForm.validate_on_submit():
        userName_exist =User.query.filter_by(user_name =editForm.username.data).first()
        if(userName_exist):
            flash("用户已经存在!")
            return redirect(url_for("user.userEdit"))
        current_user.user_name =editForm.username.data
        current_user.user_phone =editForm.userphone.data
        file =request.files["avatarSubmit"]
        if file and allowed_file(file.filename):#用户提交了非空文件并且文件合适
            fileData =file.read()
            current_user.avatar_type =file.mimetype
            current_user.avatar_bytea =fileData
        reset =current_user._get_current_object()
        db.session.add(reset)
        db.session.commit()
        return redirect(url_for("user.user_space",username =current_user.user_name))
    return render_template("editProfile.html",form=editForm,user=current_user)

@user_bp.route("/current-user-avatar",endpoint="returnIMG")#返回用户头像
def rend_IMG():
    user_avatar =io.BytesIO(current_user.avatar_bytea)
    avatar_types =current_user.avatar_type
    return send_file(path_or_file=user_avatar,mimetype=avatar_types)

def allowed_file(filename):#返回文件后缀
    ALLOWED_EXTENSIONS ={"gif","jpg","png","jpeg"}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def render_picture(data):#将图片进行base64编码
    render_pic = base64.b64encode(data).decode('utf-8')
    return render_pic
@user_bp.app_context_processor
def inject_permission():
    return dict(Permission =Permission)


@user_bp.route("/comfirm/<token>")#用户进行账户确认
@login_required
def user_confirm(token):
    if current_user.confirmed:
        return redirect("user.user_login")
    if current_user.confirm(token):
        db.session.commit()
        flash("您已经完成账户确认")
    else:
        flash("您的账户未完成确认，请重新确认！")
    return  redirect(url_for("user.user_login"))

@user_bp.before_app_request
def before_request():#对访问的路由进行限制，限制条件为是否进行账户确认
    if current_user.is_authenticated :
        if not current_user. confirmed\
                and request.path !="/unconfirmed" \
                and request.path !="/resend" \
                and  not request.full_path.startswith("/comfirm")\
                and request.path !="/logout"\
                and request.path !="/resetPwd":
                return redirect(url_for("user.user_unconfirm"))

@user_bp.route("/unconfirmed",endpoint="user_unconfirm")#未进行确认将返回的界面
def unconfirm():
    if current_user.confirmed or current_user.is_anonymous :
        return redirect(url_for("user.first_index"))
    return render_template("emailTxt/unconfirmed.html")

@user_bp.route("/resend",endpoint="reconfirmed")#重新发送确认邮件
def resend_email():
    token =current_user.generate_confirmation_token()
    send_email(current_user.user_email,"Confirm Your Account","emailTxt/confirm",user=current_user,token =token)
    flash("新邮件已经发送，请再次确认！")
    return redirect(url_for("user.user_login"))

@user_bp.route("/changePWD",endpoint="user_changePWD",methods =["POST","GET"])#用户找回密码
def change_password():
    change_form =changePWD()
    Exist=False
    if change_form.validate_on_submit():
        user=User.query.filter_by(user_email=change_form.userEmail.data).first()
        debug(type(change_form.userEmail.data))
        if  user is None:
            pass
        else:
            Exist=True
            token =user.generate_reset_token()
            send_email(user.user_email,"Reset Your Password","emailTxt/resetPWD",token =token)
    return render_template("/change/changePassword.html",form =change_form,Exist=Exist)

@user_bp.route("/resetPwd/<token>",methods=["GET","POST"],endpoint="reset_U_Password")#用户重置密码
def ResetPassword(token):
    ResetPWD_form=ResetPWD()
    if ResetPWD_form.validate_on_submit():
        if User.confirm_reset(reset_token=token,newPWD=ResetPWD_form.configPWD.data):
            db.session.commit()
            flash("密码重置完成")
            return  redirect(url_for("user.user_login"))
    return render_template("/change/resetPWD.html",form =ResetPWD_form)
