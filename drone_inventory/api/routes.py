from flask import Blueprint, jsonify, request

from drone_inventory.helpers import token_required
from drone_inventory.models import db, User, Drone, drone_schema, drones_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value',
            'other': 44.3}

# Create Drone Route
@api.route('/drones', methods = ['POST'])
@token_required
def create_drone(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    camera_quality = request.json['camera_quality']
    flight_time = request.json['flight_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    series = request.json['series']
    user_token = current_user_token.token

    drone = Drone(name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token)

    db.session.add(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)

# Retrieve ALL drones
@api.route('/drones', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    drones = Drone.query.filter_by(user_token = owner).all()
    response = drones_schema.dump(drones)
    return jsonify(response)

# Retrieve one drone
@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_drone(current_user_token, id):
    owner = current_user_token.token
    drone = Drone.query.get(id)
    response = drone_schema.dump(drone)
    return jsonify(response)

# Update a drone
@api.route('/drones/<id>', methods = ['POST','PUT'])
@token_required
def update_drone(current_user_token, id):
    drone = Drone.query.get(id)

    drone.name = request.json['name']
    drone.description = request.json['description']
    drone.price = request.json['price']
    drone.camera_quality = request.json['camera_quality']
    drone.flight_time = request.json['flight_time']
    drone.max_speed = request.json['max_speed']
    drone.dimensions = request.json['dimensions']
    drone.weight = request.json['weight']
    drone.cost_of_production = request.json['cost_of_production']
    drone.series = request.json['series']

    db.session.commit()
    response = drone_schema.dump(drone)
    return jsonify(response)

# Delete a drone
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    drone = Drone.query.get(id)
    db.session.delete(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)