
import os

class Config():

    BASE_DIR=os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED=True
    CSRF_SESSION_KEY='90e870092297aed48750f0c4cac0462283bd98a9208a9c220d7f9afe3aca5fbd'
    SECRET_KEY='c2c3d625fb5fffed9802a2c60d1fccc0e94dd6c62efe844b15ac56d209e6a72c'

    MAIL_SERVER=  "smtp.googlemail.com" 
    MAIL_PORT= 587                             
    MAIL_USERNAME='rezadarehshoori@gmail.com' 
    MAIL_PASSWORD= 'tttt'
    MAIL_USE_TLS= True
    MAIL_USE_SSL= False
    



class ProdConfig(Config):

    DEBUG=False
    SQLALCHEMY_DATABASE_URI=...


class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(Config.BASE_DIR,'app.db')



