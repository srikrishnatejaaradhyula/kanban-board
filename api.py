from flask import Flask, render_template, request, redirect, make_response
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
from requests import delete
from werkzeug.exceptions import HTTPException, NotFound
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hello'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

app.app_context().push()


class Users(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))

class Lists(db.Model):
    __tablename__= 'lists'
    list_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    list_name = db.Column(db.String(120),unique=True)
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Cards(db.Model):
    __tablename__= 'cards'
    card_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    card_title=db.Column(db.String(120),unique=True)
    content=db.Column(db.String(1000))
    deadline=db.Column(db.Date)
    is_complete=db.Column(db.Integer)
    list_id=db.Column(db.Integer, db.ForeignKey('lists.list_id'))


class SchemaValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = { "error_code" : error_code, "error_message": error_message }
        self.response = make_response(json.dumps(data), status_code)


class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = { "error_code" : error_code, "error_message": error_message }
        self.response = make_response(json.dumps(data), status_code)

class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)  

user_fields ={
    "id" : fields.Integer,
    "name" : fields.String,
    "username" : fields.String,
    "password" : fields.String
}

list_fildes = {
    "list_id" : fields.Integer,
    "list_name" : fields.String,
    "description" : fields.String,
    "user_id" : fields.Integer
}

card_fildes = {
    "card_id ":fields.Integer,
    "card_title":fields.String,
    "content" : fields.String,
    "deadline" : fields.String,
    "is_complete" : fields.Integer,
    "list_id" : fields.Integer
}

update_user = reqparse.RequestParser()
update_user.add_argument("name")

create_user = reqparse.RequestParser()
create_user.add_argument("name")
create_user.add_argument("username")
create_user.add_argument("password")

update_list = reqparse.RequestParser()
update_list.add_argument("list_name")
update_list.add_argument("description")

create_list = reqparse.RequestParser()
create_list.add_argument("list_name")
create_list.add_argument("description")
create_list.add_argument("username")


update_card = reqparse.RequestParser()
update_card.add_argument("card_title")
update_card.add_argument("content")
update_card.add_argument("deadline")
update_card.add_argument("is_complete")
update_card.add_argument("list_name")


create_card = reqparse.RequestParser()
create_card.add_argument("card_title")
create_card.add_argument("content")
create_card.add_argument("deadline")
create_card.add_argument("is_complete")
create_card.add_argument("list_name")




class Users_api(Resource):
    @marshal_with(user_fields)
    def get(self,username):
        users = Users.query.filter(Users.username == username).scalar()
        if users:
            return users,200
        else:
            return "",404

    @marshal_with(user_fields)
    def put(self,username):
        users = Users.query.filter(Users.username == username).scalar()
        print(users)
        if users is None:
            print("user 400")
            return "",400
        
        args = update_user.parse_args()
        

        if (args['name'] is None) or (args['name'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "USER001",
                error_message= "User Name is required and should be string."                
            )
        
        users.name = args['name']
        db.session.commit()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = create_user.parse_args()
        name = args.get("name", None)
        username = args.get("username",None)
        password = args.get("password", None)

        users = Users.query.filter(Users.username == username).scalar()

        if users is not None:
            return "",409

        if (name is None) or (name.isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "USER001",
                error_message= "Users name is required and should be string."                
            )
        
        if (username is None) or (username.isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "USER002",
                error_message= "Users username is required and should be string."                
            )
        if password is None:
            raise BusinessValidationError(
                status_code= 400,
                error_code= "USER003",
                error_message= "Users password is required."                
            )
        
        users = Users(
            name=name,
            username = username,
            password = password
        )

        db.session.add(users)
        db.session.commit()

        users = Users.query.filter(Users.username == username).one()
        
        return users,201


    @marshal_with(user_fields)
    def delete(self,username):
        users = Users.query.filter(Users.username == username).scalar()
        if users is None:
            raise NotFoundError(status_code=404)
        db.session.delete(users)
        db.session.commit()
        return "",200

class List_api(Resource):
    @marshal_with(list_fildes)
    def get(self,list_name):
        lists = Lists.query.filter(Lists.list_name == list_name).scalar()
        if lists:
            print("list 200")
            return lists,200
        else:
            print("user 400")
            print(lists)
            return "",400

    @marshal_with(list_fildes)
    def put(self,list_name):
        lists = Lists.query.filter(Lists.list_name == list_name).scalar()
        if lists is None:
            print("user 400")
            return "",400
        
        args = update_list.parse_args()
        

        if (args['list_name'] is None) or (args['list_name'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "LIST001",
                error_message= "list Name is required and should be string."                
            )
        if (args['description'] is None) or (args['description'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "LIST002",
                error_message= "description is required and should be string."                
            )
        lists.list_name = args['list_name']
        lists.description = args['description']
        db.session.commit()
        return lists,200

    @marshal_with(list_fildes)
    def delete(self,list_name):
        lists = Lists.query.filter(Lists.list_name == list_name).scalar()

        if lists is None:
            raise NotFoundError(status_code=404)

        db.session.delete(lists)
        db.session.commit()
        return "",200

    @marshal_with(list_fildes)
    def post(self):
        args = create_list.parse_args()
        list_name = args.get("list_name", None)
        description = args.get("description", None)
        username = args.get("username",None)

        users = Users.query.filter(Users.username == username).scalar()
        lists = Lists.query.filter(Lists.list_name == list_name).scalar()
        if  lists is not None:
            print(users,lists)
            return "",409

        if (list_name is None) or (list_name.isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "LIST001",
                error_message= "list_name is required and should be string."                
            )
        if (description is None) or (description.isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "LIST002",
                error_message= "List description is required and should be string."                
            )
        lists = Lists(
            list_name=list_name,
            description = description,
            user_id= users.id
        )
        db.session.add(lists)
        db.session.commit()
        lists = Lists.query.filter(Lists.list_name == list_name).scalar()
        return lists,201

class Card_api(Resource):
    @marshal_with(card_fildes)
    def get(self,card_title):
        cards = Cards.query.filter(Cards.card_title == card_title).scalar()
        if cards:
            return cards,200
        else:
            print(cards)
            return "",400

    @marshal_with(card_fildes)
    def put(self,card_title):
        cards = Cards.query.filter(Cards.card_title == card_title).scalar()
        if cards is None:
            print("user 400")
            return "",400
        
        args = update_card.parse_args()

        if (args['list_name'] is None) or (args['list_name'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "LIST001",
                error_message= "list Name is required and should be string."                
            )

        lists = Lists.query.filter(Lists.list_name == args['list_name']).scalar()

        if (args['card_title'] is None) or (args['card_title'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "CARD001",
                error_message= "card_title is required and should be string."                
            )
        if (args['content'] is None) or (args['content'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "CARD002",
                error_message= "content is required and should be string."                
            )
        if (args['deadline'] is None) or (args['deadline'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "CARD_DATE_002",
                error_message= "deadline is required and should be as same pattern."                
            )

        deadline= datetime.strptime(args['deadline'], '%Y-%m-%d').date()
        cards.card_title = args['card_title']
        cards.content = args['content']
        cards.deadline = deadline
        cards.is_complete = args['is_complete']
        cards.list_id = lists.list_id
        db.session.commit()
        return cards,200

    @marshal_with(card_fildes)
    def delete(self,card_title):
        cards = Cards.query.filter(Cards.card_title == card_title).scalar()


        if cards is None:
            raise BusinessValidationError(
                status_code= 400,
                error_code= "card002",
                error_message= "card does not exist"
            )
        db.session.delete(cards)
        db.session.commit()
        return "",200

    @marshal_with(card_fildes)
    def post(self):
        args = create_card.parse_args()

        deadline= datetime.strptime(args['deadline'], '%Y-%m-%d').date()

        cards = Cards.query.filter(Cards.card_title == args['card_title'] ).scalar()
        lists = Lists.query.filter(Lists.list_name == args['list_name'] ).scalar()
        if  cards is not None:
            print(cards)
            return "",409

        if (args['card_title'] is None) or (args['card_title'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "CARD001",
                error_message= "card_title is required and should be string."                
            )
        if (args['content'] is None) or (args['content'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "CARD002",
                error_message= "content is required and should be string."                
            )
        if (args['deadline'] is None) or (args['deadline'].isnumeric()):
            raise BusinessValidationError(
                status_code= 400,
                error_code= "CARD_DATE_002",
                error_message= "deadline is required and should be as same pattern."                
            )
        cards = Cards(
            card_title= args['card_title'] , 
            content= args["content"] ,
            deadline = deadline, 
            is_complete=args["is_complete"],
            list_id = lists.list_id
            )
        db.session.add(cards)
        db.session.commit()
        cards = Cards.query.filter(Cards.card_title == args['card_title']).scalar()
        return cards,201
