from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/postgres'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)




class Users(db.Model):
	__tablename__ = 'users'
	login = db.Column(db.String(50), primary_key=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)


db.create_all()




@app.route('/')
def default():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('somecookiename', 'I am cookie')
    return resp 



@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('1.html')

if __name__ == '__main__':
    app.run()
