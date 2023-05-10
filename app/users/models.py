from app.database import BaseModel
from app.extentions import db
from flask_login import UserMixin
from app.extentions import login_manager


@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user  

class User(BaseModel,UserMixin):

    username=db.Column(db.String(40),unique=True)
    password=db.Column(db.String(60))
    phone=db.Column(db.String(13))
    login_attempt=db.Column(db.Integer,default=0)
    private=db.Column(db.Boolean,default=False)
    phone_show=db.Column(db.Boolean,default=False)
    email=db.Column(db.String(60))

    post=db.relationship('Post',backref='author',lazy=True)


    def __repr__(self):
        return f'{self.__class__.__name__}({self.id},{self.phone})'
    

class Code(BaseModel):

    number=db.Column(db.Integer,nullable=False)
    expire=db.Column(db.DateTime,nullable=False)
    phone=db.Column(db.String(13))
    email=db.Column(db.String(60))
    user_id=db.Column(db.Integer)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.phone},{self.number})' 


class Follow(BaseModel):

    follower=db.Column(db.Integer,nullable=False)
    followed=db.Column(db.Integer,nullable=False )
    accept=db.Column(db.Boolean,default=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.follower},{self.followed})'
    