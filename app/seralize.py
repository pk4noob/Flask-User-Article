from flask import Flask
from extensions.extensions import ma,db
from marshmallow import validate,fields
from app.model import User,Article

#UserSchema
class UserSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    surname = fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    password = fields.String(required=True,validate=[validate.Length(min=8,max=20)])
    class Meta(ma.Schema):
        model = User
        load_instance=True

#UpdateUserSchema
class UpdateUserSchema(ma.Schema):
    name = fields.String()
    surname = fields.String()
    password = fields.String()


#ArticleSchema
class ArticleSchema(ma.SQLAlchemyAutoSchema):
    title = fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    content = fields.String(required=True,validate=[validate.Length(min=2,max=20)])

    class Meta():
        model = Article
        load_instance=True



#UpdateArticleSchema
class UpdateArticleSchema(ma.Schema):
    title = fields.String()
    content = fields.String()