from flask import Flask
import Settings
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()
login_manager =LoginManager()
login_manager.login_view ="user.user_login"

def create_app():
    app =Flask(__name__,template_folder='./templates',static_folder='./static')
    app.config.from_object(Settings.DevelopmentConfigs)
    # app.secret_key = "The SecretKey cannot send"
    from apps.main.views import user_bp
    from apps.article.view import post_bp
    from apps.SearchEngine.views import search_bp
    app.register_blueprint(search_bp,url_prefix="/SearchMap")
    app.register_blueprint(post_bp, url_prefix='/postes')
    app.register_blueprint(user_bp)
    login_manager.init_app(app)
    mail.init_app(app)
    return app