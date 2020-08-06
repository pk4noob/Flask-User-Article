from flask import Flask
from werkzeug.security import check_password_hash,generate_password_hash
from extensions.extensions import ma,db

class User(db.Model):
    __tablename__="User"
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    surname = db.Column(db.String(),nullable=False)
    password = db.Column(db.String(),nullable=False)
    Article = db.relationship('Article')

    def set_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def savedb(self):
        db.session.add(self)
        db.session.commit()

    def deletedb(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        self.savedb()


class Article(db.Model):
    __tablename__="Article"
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(),nullable=False)
    content = db.Column(db.String(),nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey("User.id"),nullable=False)

    def savedb(self):
        db.session.add(self)
        db.session.commit()

    def deletedb(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,**kwargs):
        for key ,value in kwargs.items():
            setattr(self,key,value)
        self.savedb()