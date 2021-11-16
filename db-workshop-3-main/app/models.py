from .extensions import db

class Dealership(db.Model):
    dealer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def serialize(self):
        return {
            'dealer_id': self.dealer_id,
            'name': self.name,
            'saleplaces': [saleplace.serialize() for saleplace in self.saleplaces]
        }


class Saleplace(db.Model):
    saleplace_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealership.dealer_id'), nullable=False)
    address = db.Column(db.String, nullable=False)

    __table_args__ = (db.UniqueConstraint('dealer_id', 'address', name='saleplace_address_dealer_uc'),)

    owner = db.relationship(
        'Dealership', 
        backref=db.backref('saleplaces', cascade="all, delete-orphan", lazy='joined'), 
        uselist=False, 
        lazy=True
    )

    def serialize(self):
        return {
            'saleplace_id': self.saleplace_id,
            'address': self.address
        }


class Vehicle(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True)
    saleplace_id = db.Column(db.Integer, db.ForeignKey('saleplace.saleplace_id'), nullable=False)
    brand_name = db.Column(db.String, nullable=False)
    model_name = db.Column(db.String, nullable=False)
    body_type = db.Column(db.String)
    release_year = db.Column(db.Integer)

    saler = db.relationship(
        'Saleplace', 
        backref=db.backref('cars', cascade="all, delete-orphan", lazy=True), 
        uselist=False, 
        lazy=True
    )

    def serialize(self):
        return {
            'vehicle_id': self.vehicle_id,
            'brand_name': self.brand_name,
            'model_name': self.model_name,
            'body_type': self.body_type,
            'release_year' : self.release_year 
        }
