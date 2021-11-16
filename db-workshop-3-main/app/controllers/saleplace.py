from flask import request, jsonify, make_response
from app import models
from app.extensions import db


def create_saleplace():
    try:
        new_saleplace = models.Saleplace(
            dealer_id=request.form.get('dealer_id'),
            address=request.form.get('address')
        )
        db.session.add(new_saleplace)
        db.session.commit()
        return make_response(new_saleplace.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)


def update_saleplace():
    try:
        saleplace_id = request.form.get('id')
        #new_dealer_id = request.form.get('dealer_id')
        new_address = request.form.get('address')

        found = models.Saleplace.query.get(saleplace_id)
        if not found:
            return make_response(jsonify(error='Not found'), 404)
        #found.dealer_id = new_dealer_id
        found.address = new_address
        db.session.add(found)
        db.session.commit()
        return make_response(found.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)


def delete_saleplace():
    try:
        saleplace_id = request.form.get('id')
        found = models.Saleplace.query.get(saleplace_id)
        if not found:
            return make_response(jsonify(error='Not found'), 404)
        db.session.delete(found)
        db.session.commit()
        return make_response(fount.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)
