from app.database import BaseModel
from app.extentions import db


class Post(BaseModel):

    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

 

    def __repr__(self):
        return f'{self.__class__.__name__}({self.author},{self.title[:30]})'
    
