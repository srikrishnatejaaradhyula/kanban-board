from flask import Flask,render_template,flash, redirect,url_for,session,logging,request,Response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin,login_user,login_required,logout_user,current_user
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask_restful import Resource, Api
from matplotlib.figure import Figure
import numpy as np
import io
from api import Users_api,List_api,Card_api


app = Flask(__name__,template_folder='template')
app.secret_key = 'hello'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
api = Api(app)
app.app_context().push()

login_manger =LoginManager()
login_manger.init_app(app)

class Users(UserMixin,db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))

class Lists(UserMixin,db.Model):
    __tablename__= 'lists'
    list_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    list_name = db.Column(db.String(120),unique=True)
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Cards(UserMixin,db.Model):
    __tablename__= 'cards'
    card_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    card_title=db.Column(db.String(120),unique=True)
    content=db.Column(db.String(1000))
    deadline=db.Column(db.Date)
    is_complete=db.Column(db.Integer)
    list_id=db.Column(db.Integer, db.ForeignKey('lists.list_id'))

@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _uname = request.form["luname"]
        _passw = request.form["lpwd"]
        login = Users.query.filter_by(username=_uname, password=_passw).first()
        if login is not None:
            login_user(login)
            return redirect('/home')
        else:
            flash('Username or password is wrong')
            return redirect('/login')
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        _uname = request.form['sname']
        _user = request.form['suname']
        _passw = request.form['spwd']
        login = Users.query.filter_by(username=_user).first()
        print(login)
        if  login:
            flash('Username is already used')
            return redirect('/register')
        else:
            db.session.add(Users(name = _uname , username = _user, password = _passw))
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/home")
@login_required
def home():
    user_list = Lists.query.filter_by(user_id = current_user.id).all()
    user_card = Cards.query.all()
    return render_template("home.html",users=current_user,lists=user_list,cards=user_card)


@app.route("/list", methods=["GET", "POST"])
@login_required
def list():
    if request.method == "POST":
        _lname = request.form['l_name']
        _desc = request.form['l_desc']
        lists=Lists.query.filter_by(list_name = _lname ).first() 
        if lists:
            flash('Name of list is already used')
            return redirect('/list')
        else:
            db.session.add(Lists(list_name = _lname , description= _desc, user_id =current_user.id))
            db.session.commit()
            return redirect('/home')
    return render_template("list.html",users=current_user)

@app.route("/list_edit/<id>", methods=["GET", "POST"])
@login_required
def list_edit(id):
    lists = Lists.query.filter_by(list_id= id).first()
    if request.method == "POST":
        if lists:
            _lname = request.form['l_name']
            _desc = request.form['l_desc']
            lists.list_name=_lname
            lists.description=_desc
            db.session.commit()
            return redirect('/home')
    return render_template("list_edit.html",lists=lists,users=current_user)

@app.route("/list_delete/<id>")
def list_delete(id):
    lists = Lists.query.filter_by(list_id= id).first()
    cards = Cards.query.filter_by(list_id= lists.list_id).first()
    if cards:
        db.session.delete(cards)
    db.session.delete(lists)
    db.session.commit()
    return redirect('/home')

@app.route("/card", methods=["GET", "POST"])
@login_required
def card():
    u_list= Lists.query.filter(Lists.user_id == current_user.id).all()

    if request.method == "POST":
        _list= request.form['list_title']
        _title = request.form['card_title']
        _content= request.form['content']
        _dead= request.form['deadline']
        _iscomplete= request.form['c_complete']
        _lists = Lists.query.filter_by(list_name= _list).first()
        dto = datetime.strptime(_dead, '%Y-%m-%d').date()
        cards=Cards.query.filter_by(card_title = _title ).first() 
        if cards:
            flash('Name of card is already used')
            return redirect('/card')
        elif _list == "": 
            flash('please select the list name')
            return redirect('/card')
        else:
            db.session.add(Cards(card_title= _title , content=_content, deadline =dto, is_complete=_iscomplete,list_id = _lists.list_id))
            db.session.commit()
            return redirect('/home')
    return render_template("card.html",lists=u_list,users=current_user)

@app.route("/card_edit/<id>", methods=["GET", "POST"])
@login_required
def card_edit(id):
    lists=Lists.query.filter(Lists.user_id == current_user.id).all()
    cards = Cards.query.filter_by(card_id= id).first()
    if request.method == "POST":
        if cards:
            _list= request.form['list_title']
            _title = request.form['card_title']
            _content= request.form['content']
            _dead= request.form['deadline']
            _iscomplete= request.form['c_complete']
            _lists = Lists.query.filter_by(list_name= _list).first()
            dto = datetime.strptime(_dead, '%Y-%m-%d').date()
            cards.card_title=_title
            cards.content=_content
            cards.deadline=dto
            cards.is_complete=_iscomplete
            cards.list_id=_lists.list_id
            db.session.commit()
            return redirect('/home')
    return render_template("card_edit.html",cards=cards,lists=lists,users=current_user)

@app.route("/card_delete/<id>")
def card_delete(id):
    cards = Cards.query.filter_by(card_id= id).first()
    db.session.delete(cards)
    db.session.commit()
    return redirect('/home')


@app.route("/summary")
@login_required
def summary():
    lists = Lists.query.filter_by(user_id = current_user.id).all()
    cards = Cards.query.all()
    today = datetime.today()
    to_date = today.strftime("%Y-%m-%d")
    t_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    print("******",t_date)
    return render_template("summary.html",lists=lists,users=current_user,cards=cards,t_date=t_date)


@app.route('/plot/<id>.png')
def plot_png(id):
    fig = create_figure(id)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(id):
    fig = Figure()
    axis = fig.add_subplot()
    cards = Cards.query.filter_by(list_id= id).all()
    com=[]
    tit=[]
    for cad in range(len(cards)):
        com.append(cards[cad].is_complete)
        tit.append(cards[cad].card_title)
    y=np.array(com)
    print(tit,y)
    axis.bar(tit,y)
    return fig


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")



api.add_resource(Users_api, "/api/users", "/api/users/<string:username>")
api.add_resource(List_api, "/api/lists", "/api/lists/<string:list_name>")
api.add_resource(Card_api, "/api/cards", "/api/cards/<string:card_title>")





if __name__ == "__main__":
    app.run(
        debug=True)