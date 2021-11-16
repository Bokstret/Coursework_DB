from flask import request, jsonify, make_response
from app import models
from app.extensions import db


def get_all_vehicles():
    cars = models.Vehicle.query.all()
    return make_response(jsonify(cars=[car.serialize() for car in cars]), 200)


def create_vehicle():
    try:
        new_vehicle = models.Vehicle(
            saleplace_id=request.form.get('saleplace_id'),
            brand_name=request.form.get('brand_name'),
            model_name=request.form.get('model_name'),
            body_type=request.form.get('body_type'),
            release_year=request.form.get('release_year')
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return make_response(new_vehicle.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)


def update_vehicle():
    try:
        vehicle_id = request.form.get('id')
        new_saleplace_id = request.form.get('saleplace_id'),
        new_brand_name = request.form.get('brand_name'),
        new_model_name = request.form.get('model_name'),
        new_body_type = request.form.get('body_type'),
        new_release_year = request.form.get('release_year')

        found = models.Vehicle.query.get(vehicle_id)
        if not found:
            return make_response(jsonify(error='Not found'), 404)

        found.saleplace_id = new_saleplace_id
        found.brand_name = new_brand_name
        found.model_name = new_model_name
        found.body_type = new_body_type
        found.release_year = new_release_year

        db.session.add(found)
        db.session.commit()
        return make_response(found.serialize(), 200)
    except Exception as err:
        return make_response(jsonify(error='Error'), 400)


def delete_vehicle():
    try:
        vehicle_id = request.form.get('id')

        found = models.Vehicle.query.get(vehicle_id)
        if not found:
            return make_response(jsonify(error='Not found'), 404)

        db.session.delete(found)
        db.session.commit()
        return make_response(found.serialize(), 200)
    except:
        return make_response(jsonify(error='Error'), 400)
