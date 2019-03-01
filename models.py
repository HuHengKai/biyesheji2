from flask_sqlalchemy import SQLAlchemy
from  datetime import datetime
db=SQLAlchemy()
class Users(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # 我们新增了一个avatar_path字段来存用户头像图片文件的路径
    avatar_path = db.Column(db.String(256), nullable=False, default='image/touxiang.jpg')
    def __index__(self):
        self.username=Users.username
        self.password=Users.password

class Questions(db.Model):
    __tablename__='question_info'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.TEXT,nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    author = db.relationship('Users', backref=db.backref('questions', order_by=create_time.desc()))

class Device(db.Model):
    __tablename__='device_info'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.TEXT,nullable=False)
    #author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    #create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # author = db.relationship('Users', backref=db.backref('questions', order_by=create_time.desc()))
