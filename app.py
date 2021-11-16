from flask import Flask, url_for,request, send_from_directory, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vtzefyhigwptbe:45eec3aaa53b4719cf61196aad25f2b5ca825611542238856d9801fc557c34f1@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/d1pfe0st2g9c16'
db = SQLAlchemy(app)




class Store(db.Model):
	__tablename__ = 'store'
	name = db.Column(db.String(50), primary_key=True, nullable=False)
	income = db.Column(db.Integer)
	amount = db.Column(db.Integer)
	parent = db.Column(db.String(50), nullable=False)
	publisher = db.relationship('Games')



class Publisher(db.Model):
	__tablename__ = 'publisher'
	name = db.Column(db.String(50), primary_key=True, nullable=False)
	adress = db.Column(db.String(50), nullable=False)
	popularity = db.Column(db.Integer)
	publisher = db.relationship('Games')



class Games(db.Model):
	__tablename__ = 'games'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(50), unique=True, nullable=False)
	price = db.Column(db.Integer, nullable=False)
	rating = db.Column(db.Integer)
	publisher = db.Column(db.String(50),db.ForeignKey('publisher.name'))
	store = db.Column(db.String(50), db.ForeignKey('store.name'))


db.create_all()


#valve = Publisher(name = "Valve", adress = "America", popularity = 100)
#steam = Store(name = "Steam", income = 10000, amount = 254532, parent = "Valve")
#dota2 = Games(id= 2, name ="Dota", price = 0, publisher = "Valve", store = "Steam", rating = 10)

#db.session.add(valve)
#db.session.add(steam)
#db.session.add(dota2)
#db.session.commit()

@app.route('/<table>/', methods=['post'])
def add(table):
	if table == "Games":
		gid = request.form.get('gid')
		name = request.form.get('name')
		price = request.form.get('price')
		rating = request.form.get('rating')
		publisher = request.form.get('publisher')
		store = request.form.get('store')
		new_game = Games(id = gid, name = name, price = price, rating = rating, publisher = publisher, store = store)
	elif table == "Publisher":
		name = request.form.get('name')
		adress = request.form.get('adress')
		popularity = request.form.get('popularity')
		new_game = Publisher(name = name, adress = adress, popularity = popularity)
	elif table == "Store":
		name = request.form.get('name')
		income = request.form.get('income')
		amount = request.form.get('amount')
		parent = request.form.get('parent')
		new_game = Store(name = name, income = income,amount  = amount, parent = parent)
	try:
		db.session.add(new_game)
		db.session.commit()
	except Exception:
		if table == "Games":
			return redirect(url_for('read_table_games'))
		elif table == "Publisher":
			return redirect(url_for('read_table_publisher'))
		elif table == "Store":
			return redirect(url_for('read_table_store'))
	if table == "Games":
		return redirect(url_for('read_table_games'))
	elif table == "Publisher":
		return redirect(url_for('read_table_publisher'))
	elif table == "Store":
		return redirect(url_for('read_table_store'))

@app.route('/<table>/Update', methods=['post'])
def update(table):
	if table == "Games":
		name = request.form.get('Name')
		price = request.form.get('Price')
		rating = request.form.get('Rating')
		publisher = request.form.get('Publisher')
		store = request.form.get('Store')
		gid = request.form.get('Id')
		x = db.session.query(Games).get(gid)
		x.name = name
		x.price = price
		x.rating = rating
		x.publisher = publisher
		x.store = store
	elif table == "Publisher":
		name = request.form.get('Name')
		adress = request.form.get('Adress')
		popularity = request.form.get('Popularity')
		x = db.session.query(Publisher).get(name)
		x.name = name
		x.adress = adress
		x.popularity = popularity
	elif table == "Store":
		name = request.form.get('Name')
		income = request.form.get('Income')
		amount = request.form.get('Amount')
		parent = request.form.get('Parent')
		x = db.session.query(Store).get(name)
		x.name = name
		x.income = income
		x.amount = amount
		x.parent = parent
	try:
		db.session.commit()
	except Exception:
		if table == "Games":
			return redirect(url_for('read_table_games'))
		elif table == "Publisher":
			return redirect(url_for('read_table_publisher'))
		elif table == "Store":
			return redirect(url_for('read_table_store'))
	if table == "Games":
		return redirect(url_for('read_table_games'))
	elif table == "Publisher":
		return redirect(url_for('read_table_publisher'))
	elif table == "Store":
		return redirect(url_for('read_table_store'))

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/templates/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)

@app.route('/Games')
def read_table_games():
	data = Games.query.all()
	return render_template('index.html', data=data,table="Games")

@app.route('/Publisher')
def read_table_publisher():
	data = Publisher.query.all()
	return render_template('index_publisher.html', data=data,table="Publisher")

@app.route('/Store')
def read_table_store():
	data = Store.query.all()
	return render_template('index_store.html', data=data,table="Store")

@app.route('/<table>/delete/<name>')
def delete(table,name):
	if table == "Games":
		data = Games.query.all()
	elif table == "Publisher":
		data = Publisher.query.all()
	elif table == "Store":
		data = Store.query.all()
	else:
		return redirect(url_for('hello_world'))
	for d in data:
		if d.name == name:
			db.session.delete(d)
			db.session.commit()
	if table == "Games":
		return redirect(url_for('read_table_games'))
	elif table == "Publisher":
		return redirect(url_for('read_table_publisher'))
	elif table == "Store":
		return redirect(url_for('read_table_store'))
	else:
		return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run()
