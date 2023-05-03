from app.extentions import db



class BaseModel(db.Model):
    __abstract__=True

    id=db.Column(db.Integer,primary_key=True)
    create_at=db.Column(db.DateTime,default=db.func.current_timestamp())
    update_at=db.Column(db.DateTime,default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())