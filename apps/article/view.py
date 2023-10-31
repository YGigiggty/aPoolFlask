import io
import random
from doctest import debug
from flask import Blueprint, render_template, redirect, url_for, send_file, request, flash
from flask_login import current_user, login_required
from sqlalchemy import func
from apps.main.forms import EditPost
from apps.models import Post, User
from extends import db

post_bp =Blueprint("postes",__name__)

@post_bp.route("/",endpoint="post_index")
def MoreNews():
    RandomPosts =Post.query.order_by(func.random()).limit(5)
    return render_template("/Posts/MoreNews.html",posts =RandomPosts)

@post_bp.route("/Edit",endpoint="editPosts",methods=["GET","POST"])
def PostWrit():
    EditForm =EditPost()
    if EditForm.validate_on_submit():
        TheTitle =EditForm.Title.data
        ThePostExist =Post.query.join(User,Post.auth_id ==User.id).filter(Post.title==TheTitle).first()
        if(ThePostExist):
            flash("该标题您已编辑!")
            return redirect(url_for("postes.editPosts"))
        post =Post(
            body =EditForm.body.data,
            author =current_user._get_current_object(),
            title =EditForm.Title.data
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("postes.MyList"))
    return render_template("/Posts/PostsEdit.html",form =EditForm)

@login_required
@post_bp.route("/MyPost",endpoint="MyList")
def PostList(): 
    U =current_user
    page = request.args.get('page', 1, type=int)
    pagination =Post.query.filter_by(auth_id=U.id).order_by(Post.timetamp.desc()).paginate(
        page=page, per_page=3, error_out=False
    )
    Posts =pagination.items
    return render_template("/Posts/MyPosts.html",user=U,posts=Posts,pagination =pagination)

@login_required
@post_bp.route("/postDelete/<int:id>",endpoint ="ListDelete")  
def DeletePosts(id):
    PostId =id
    Deleted =Post.query.get(PostId)
    db.session.delete(Deleted)
    db.session.commit()
    return  redirect(url_for("postes.MyList"))

@post_bp.route("/ThePost/<int:id>",endpoint="AuthPost")
def ThePosts(id):
    Posts = Post.query.filter_by(id=id).first()
    AuthID =Posts.auth_id
    auth =User.query.filter_by(id =AuthID).first()
    return render_template("/Posts/Post.html",post=Posts,Auth=auth)

@post_bp.route("/AuthHead/<int:id>",endpoint="AuthHead")
def rend_head(id):
    U =User.query.filter_by(id =id).first()
    user_avatar = io.BytesIO(U.avatar_bytea)
    avatar_types = U.avatar_type
    return send_file(path_or_file=user_avatar,mimetype=avatar_types)

@post_bp.route("/AuthSpace/<int:id>",endpoint="Space")
def Authspace(id):
    page = request.args.get('page', 1, type=int)
    U =User.query.filter_by(id=id).first()
    postSum =Post.query.filter_by(auth_id =id).all()
    pagination =Post.query.filter_by(auth_id =id).order_by(Post.timetamp.desc()).paginate(
        page=page,per_page=3,error_out=False
    )
    posts =pagination.items
    i=0
    for p in postSum:
        i+=1
    return render_template("/Posts/ShowSpace.html",Auth =U,post =posts,sum=i,pagination =pagination)