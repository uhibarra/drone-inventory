# Standard Library Imports
import secrets
import uuid
from datetime import datetime

# Third Party Library Imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash # Flask security for passwords

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User Model Creation
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = True, default = '')
    last_name = db.Column(db.String(50), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref = "owner", lazy = True)

    def __init__(self, email, id = '', first_name = '', last_name = '', password = '', g_auth_verify = False, token = ''):
        self.id = self.set_id() 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password) 
        self.g_auth_verify = g_auth_verify
        self.token = self.set_token(24) 
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} has been added to the database, boss.'

class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    camera_quality = db.Column(db.String(50), nullable = True)
    flight_time = db.Column(db.String(100))
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_production = db.Column(db.Numeric(precision = 10, scale = 2))
    series = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.series = series
        self.user_token = user_token
        
    def set_id(self):
        return secrets.token_urlsafe()
    
    def __repr__(self):
        return f'User {self.name} has been created, boss.'

# Creation of API Schema via the Marshmallow Object
class DroneSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','price','camera_quality','flight_time','max_speed','dimensions','weight','cost_of_production','series']

drone_schema = DroneSchema()
drones_schema = DroneSchema(many=True)