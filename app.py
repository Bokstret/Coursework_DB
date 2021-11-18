from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/postgres'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)




class Users(db.Model):
	__tablename__ = 'users'
	email = db.Column(db.String(50), primary_key=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)


db.create_all()




@app.route('/')
def default():
    return render_template('index.html')


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    if request.method == 'POST':
        resp = make_response(redirect('/'))
        resp.set_cookie('email', '', expires=0)
        resp.set_cookie('password', '', expires=0)
        return resp
    return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    #check for cockies
    if request.cookies.get('email'):
        cockie_email = request.cookies.get('email')
        cockie_password = request.cookies.get('password')
        db_email = db.session.query(Users).get(cockie_email)
        if db_email and db_email.password == cockie_password:
              return redirect('/')
        
    #POST method handler
    if request.method == 'POST':
        #authentication
        email = request.form.get('email')
        password = request.form.get('password')

        db_email = db.session.query(Users).get(email)
        if db_email:
                return render_template('index.html')

        #populate database
        new_user = Users(email = email, password = password)
        db.session.add(new_user)
        db.session.commit()

        #set cockie
        resp = make_response(render_template('registration.html'))
        resp.set_cookie('email', email)
        resp.set_cookie('password', password)
        return resp
    return render_template('registration.html')

if __name__ == '__main__':
    app.run()
