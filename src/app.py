import os
import datetime
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from dotenv import load_dotenv
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv() # cargar las variables de entorno

app = Flask(__name__)


app.config['DEBUG'] = True # Permite ver los errores
app.config['ENV'] = 'development' # Activa el servidor en modo desarrollo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASEURI') # Leemos la url de conexion a la base de datos
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def main():
    return jsonify({ "status": "Server Up"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get("username") # None
    password = request.json.get("password") # None
    
    if not username:
        return jsonify({ "error": "Username es obligatorio"}), 400
    
    if not password:
        return jsonify({ "error": "Password es obligatorio"}), 400
    
    userFound = User.query.filter_by(username=username).first()
    
    if not userFound:
        return jsonify({ "error": "username/password son incorrectos!!"}), 401
    
    if not check_password_hash(userFound.password, password):
        return jsonify({ "error": "username/password son incorrectos!!"}), 401
    
    expires = datetime.timedelta(days=3)
    access_token = create_access_token(identity=userFound.id, expires_delta=expires)
    
    data = {
        "access_token": access_token,
        "user": userFound.serialize()
    }
    
    return  jsonify(data), 200

@app.route('/api/register', methods=['POST'])
def register():
    
    username = request.json.get("username") # None
    password = request.json.get("password") # None
    
    if not username:
        return jsonify({ "error": "Username es obligatorio"}), 400
    
    if not password:
        return jsonify({ "error": "Password es obligatorio"}), 400
    
    userFound = User.query.filter_by(username=username).first()
    
    if userFound:
        return jsonify({ "error": "Username already exists"}), 400
    
    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    
    db.session.add(user)
    db.session.commit()
    
    expires = datetime.timedelta(days=3)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    
    data = {
        "access_token": access_token,
        "user": user.serialize()
    }
    
    return  jsonify(data), 200
        

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    
    id = get_jwt_identity()
    user = User.query.get(id)
    
    return jsonify({ "data": "Hola Mundo", "user": user.serialize() })


if __name__ == '__main__':
    app.run()