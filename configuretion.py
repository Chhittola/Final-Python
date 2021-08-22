from flask import Flask, request, jsonify, make_response, json
from flask_migrate import Migrate

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/EnrollmentDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret'
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

