
from flask import Blueprint, render_template, redirect
from sqlalchemy import text
from apps.main.forms import Search
from apps.models import Post
from extends import db

search_bp =Blueprint("Search",__name__)

@search_bp.route("/SearchPost",endpoint="PostResult",methods=["GET","POST"])
def Result():
    QueryForm =Search()
    if QueryForm.validate_on_submit():
        KeyWords =QueryForm.goal.data
        PostResult =Post.query.filter(Post.fts.match(KeyWords)).all()
        return render_template("/Search/PostSearch.html",Keyword =KeyWords,posts =PostResult)
    return render_template("/Search/PostSearch.html")

