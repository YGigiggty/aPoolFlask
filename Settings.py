import os

class Configs:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/newprojet'
    # Project_ADMIN ="hongmingha886@gmial.com"
    MAIL_SERVER ="localhost"
    MAIL_PORT =2500
    SECRET_KEY= "The SecretKey cannot send"
    MAIL_USE_SSL =False
    MAIL_USERNAME ="yangyiliu6@163.com"
    MAIL_PASSWORD ="NYZPNMCLZFSISGZB"

class DevelopmentConfigs(Configs):
    ENV = "development"

class ProductConfigs(Configs):
    DEBUG = False
    ENV = "production"

