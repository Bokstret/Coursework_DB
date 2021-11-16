from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


app = Flask(__name__, static_url_path='')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vtzefyhigwptbe:45eec3aaa53b4719cf61196aad25f2b5ca825611542238856d9801fc557c34f1@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/d1pfe0st2g9c16'
db = SQLAlchemy(app)




class Users(db.Model):
	__tablename__ = 'users'
	login = db.Column(db.String(50), primary_key=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)


db.create_all()


@app.route('/')
def default():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["name"] = 'ihorek'
	return redirect("/")
    return render_template('login.html')



if __name__ == '__main__':
    app.run()
