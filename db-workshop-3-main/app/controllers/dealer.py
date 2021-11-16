from flask import request, jsonify, make_response
from app import models
from app.extensions import db


def get_all_dealers():
    all_dealers = models.Dealership.query.all()
    return make_response(jsonify(dealers=[dealer.serialize() for dealer in all_dealers]), 200)


# NOT NEEDED
def get_dealer_by_id():
    dealer_id = request.args.get('id')
    found = models.Dealership.query.get(dealer_id)
    if found:
        return make_response(found.serialize(), 200)
    else:
        return make_response(jsonify(error='Not found'), 404)


def create_dealer():
    try:
        new_dealer = models.Dealership(name=request.form.get('name'))
        db.session.add(new_dealer)
        db.session.commit()
        return make_response(new_dealer.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)


def update_dealer():
    try:
        dealer_id = request.form.get('id')
        new_name = request.form.get('name')
        found = models.Dealership.query.get(dealer_id)
        if not found:
            return make_response(jsonify(error='Not found'), 404)
        found.name = new_name
        db.session.add(found)
        db.session.commit()
        return make_response(found.serialize(), 200)
    except Exception as err:
        return make_response(err, 400)


def delete_dealer():
    try:
        dealer_id = request.form.get('id')
        found = models.Dealership.query.get(dealer_id)
        if not found:
            return make_response(jsonify(error='Not found'), 404)
        db.session.delete(found)
        db.session.commit()
        return make_response(found.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)
