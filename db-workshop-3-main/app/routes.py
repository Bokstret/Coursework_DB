from flask import Flask, request, render_template
from flask import current_app as app
from .controllers import dealer, saleplace, vehicle


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/dealers', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dealers_route():
    if request.method == 'POST':
        return dealer.create_dealer()
    elif request.method == 'PUT':
        return dealer.update_dealer()
    elif request.method == 'DELETE':
        return dealer.delete_dealer()
    else:
        return dealer.get_all_dealers()


@app.route('/api/saleplaces', methods=['POST', 'PUT', 'DELETE'])
def saleplaces_route():
    if request.method == 'POST':
        return saleplace.create_saleplace()
    elif request.method == 'PUT':
        return saleplace.update_saleplace()
    elif request.method == 'DELETE':
        return saleplace.delete_saleplace()


@app.route('/api/vehicles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def vehicles_route():
    if request.method == 'POST':
        return vehicle.create_vehicle()
    elif request.method == 'PUT':
        return vehicle.update_vehicle()
    elif request.method == 'DELETE':
        return vehicle.delete_vehicle()
    else:
        return vehicle.get_all_vehicles()
