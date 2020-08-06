from flask import Flask, request, jsonify
from app_init.app_factory import createAp
from flask import jsonify, current_app, request
from flask import Flask, jsonify, request
from http import HTTPStatus
from werkzeug.security import generate_password_hash
import os
import warnings
from app.seralize import UserSchema,UpdateUserSchema,ArticleSchema,UpdateArticleSchema
from app.model import User,Article
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,create_refresh_token,jwt_refresh_token_required,
    get_jwt_identity
)
import jwt

warnings.simplefilter("ignore")
settings_name = os.getenv("settings")
app = createAp(settings_name)


#USER POST METHODS
@app.route("/user",methods=["POST"])
def createUser():
    data = request.get_json()
    try:
        user = UserSchema().load(data)
        user.set_password()
        user.savedb()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return UserSchema(exclude=["password"]).jsonify(user),HTTPStatus.OK

#USER GET METHODS
@app.route("/users",methods=["GET"])
def UserGetAllMethods():
    data = User.query.all()
    return UserSchema().jsonify(data,many=True),HTTPStatus.OK

#USER ALL GET METHODS
@app.route("/user",methods=["GET"])
@jwt_required
def UserGetMethods():

    #tokeni headerden elnen alib onu decode eleyelerek biz userin identity  elde eleiyirik asigidaki methodla

    # token =  request.headers.get("Authorization").split()[1]
    # print(token)

    # decode = jwt.decode(token, "salam","HS256")
    # print(decode)
    identity =get_jwt_identity()

    data = User.query.filter_by(id=identity).first()
    if data:
        return UserSchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg="error")

#USER UPDATE METHODS
@app.route("/user",methods=["PUT"])
@jwt_required
def UpdateMethods():
    identity=get_jwt_identity()
    data = User.query.filter_by(id=identity).first()
    if data:
        user = request.get_json()
        userdata=UpdateUserSchema().load(user)
        data.update(**userdata)
        return UpdateUserSchema().jsonify(userdata),HTTPStatus.OK
    return jsonify(msg="Update olunmadi"),HTTPStatus.NOT_FOUND

#USER DELETE METHODS
@app.route("/user",methods=["DELETE"])
@jwt_required
def UserDelete():
    identity=get_jwt_identity()
    data = User.query.filter_by(id=identity).first()
    if data:
        data.deletedb()
        return jsonify(msg="Silindi"),HTTPStatus.OK
    return jsonify(msg="silinmedi"),HTTPStatus.NOT_FOUND

@app.route("/user/article",methods=["POST"])
@jwt_required
def CreateArticle():
    identity=get_jwt_identity()
    data = request.get_json()
    try:
        user = User.query.get(identity)
        if user:
            art=ArticleSchema().load(data)
            art.user_id=user.id
            art.savedb()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.NOT_FOUND
    return ArticleSchema().jsonify(art),HTTPStatus.OK
            
@app.route("/user/<int:id>/article",methods=["GET"])
@jwt_required
def UserArticleGetMethods(id):
    identity=get_jwt_identity()
    data = Article.query.filter_by(user_id=identity,id =id).first()
    if data:
        return ArticleSchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg = "Not Found Get Methods"),HTTPStatus.NOT_FOUND

@app.route("/user/article",methods=["GET"])
@jwt_required
def UserArticleGetAllMethods():
    identity=get_jwt_identity()
    data = Article.query.filter_by(user_id=identity).all()
    return ArticleSchema().jsonify(data,many=True),HTTPStatus.OK

@app.route("/user/<int:id>/article",methods=["PUT"])
@jwt_required
def UserArticleUpdateMethods(id):
    identity=get_jwt_identity()
    data = Article.query.filter_by(user_id=identity,id = id).first()
    if data:
        user = request.get_json()
        user1 = UpdateArticleSchema().load(user)
        data.update(**user1)
        return UpdateArticleSchema().jsonify(user1),HTTPStatus.OK
    return jsonify(msg="UPDATE OLUNMADI")

@app.route("/user/<int:id>/article",methods=["Delete"])
@jwt_required
def UserArticleDeleteMethods(id):
    identity = get_jwt_identity()
    data = Article.query.filter_by(user_id=identity,id =id).first()
    if data:
        data.deletedb()
        return jsonify(msg = "SILINDI"),HTTPStatus.OK
    return jsonify(msg="Silinmedi"),HTTPStatus.NOT_FOUND


#User - Login - Create - Methods
@app.route("/user/login",methods=["POST"])
def Login():
    print(request.get_json())
    name = request.json.get("name")
    password = request.json.get("password")

    if not name:
        return jsonify(msg="Wrong Name"),HTTPStatus.BAD_REQUEST
    if not password:
        return jsonify(msg="Wrong Password"),HTTPStatus.BAD_REQUEST
    user = User.query.filter_by(name=name).first()
    # scema = UserSchema().dump(user)
    
    if user:
        if user.check_password(password):
            token = {
                    'access_token': create_access_token(identity=user.id),
                    'refresh_token': create_refresh_token(identity=user.id)
                }
            # scema.pop("password")
            # token.update(user_data=scema)
            return jsonify(token),HTTPStatus.OK
        return jsonify(msg="User not founded"),HTTPStatus.NOT_FOUND

@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    print(user)
    if user:
        access_token= create_access_token(identity=user)
        return jsonify({"Access Token:":access_token}),HTTPStatus.OK
    return jsonify(msg="ERROR"),HTTPStatus.NOT_FOUND
