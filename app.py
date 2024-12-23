from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from dotenv import get_key
from os.path import abspath

APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
APP.permanent_session_lifetime = 3600
APP.secret_key = get_key(abspath('.env'), 'KEY')

Logged = False

class Base(DeclarativeBase):
    pass

DB = SQLAlchemy(model_class = Base)

DB.init_app(APP)

class user(DB.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30), nullable = True)
    cpf: Mapped[str] = mapped_column(String(11), nullable = False, unique = True)
    password: Mapped[str] = mapped_column(String(50), nullable = False)

    def __repr__(self):
        return self.cpf

class items(DB.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30), nullable = False)
    code: Mapped[str] = mapped_column(String(30), nullable = False)
    status: Mapped[bool] = mapped_column(Boolean(), nullable = False)
    repair: Mapped[str] = mapped_column(String(255), nullable = True)

# class Repair(DB.Model):
#     id = Mapped[int] = mapped_column(primary_key = True)
#     item_id = Mapped[int] = mapped_column(ForeignKey('user.id'))



with APP.app_context():
    DB.create_all()

@APP.route("/", methods=["GET", "POST"])
def home():
    session.permanent = True

    if 'name' in session:
        return redirect(url_for('control'))

    if request.method == "POST":
        if user.query.filter_by(cpf = request.form['cpf'], password = request.form['password']).first():
            session['name'] = user.query.filter_by(cpf = request.form['cpf']).first().name
            return redirect(url_for('control'))

    return render_template("index.html")

@APP.route("/control")
def control():
    if 'name' in session:
        return render_template('control.html', name = session['name'])
    else:
        return redirect(url_for('home'))

@APP.route("/control/consulta")
def consulta():
    if 'name' in session:
        return render_template('consult.html', name = session['name'], Itens = items.query.all())



@APP.route("/DeleteSession")
def RemoveSession():
    del session['name']
    return redirect(url_for('home'))


if __name__ == "__main__":
    APP.run("0.0.0.0", 5000, True, True)