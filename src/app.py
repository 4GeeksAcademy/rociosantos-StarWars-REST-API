"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, favorite_character, Planets, favorite_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    user = User(firstname = body['firstname'],lastname = body['lastname'],email = body['email'])
    db.session.add(user)
    try: 
        db.session.commit()
        return jsonify({'response': 'ok'}), 200
    except: 

        return 'error al crear el usuario', 400

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users_serialized = [user.serialize() for user in all_users]
    return jsonify(all_users_serialized), 200

@app.route('/character', methods=['POST'])
def create_character():
    body = request.get_json()
    character = Character(name = body['name'], gender = body['gender'], homeworld = body['homeworld'])
    db.session.add(character)
    try: 
        db.session.commit()
        return jsonify({'response': 'ok'}), 200
    except: 

        return 'error al crear el usuario', 400

@app.route('/characters', methods=['GET'])
def get_characters():
    all_character = Character.query.all()
    all_character = list(map(lambda x: x.serialize(), all_character))

    return jsonify(all_character), 200

@app.route('/favorite/character', methods=['GET'])
def get_favorite_character():
   
    character_favorite = favorite_character.query.all()
 
    all_character_favorite = []
    for favorite in character_favorite:
        serialized_favorite = favorite.serialize()
        serialized_favorite['name'] = favorite.character.name if favorite.character else None
        all_character_favorite.append(serialized_favorite)

    return jsonify(all_character_favorite), 200

@app.route('/favorite/character', methods = ['POST'])
def add_favorite_character():
    request_body_favorite_character = request.get_json()
    new_favorite_character = favorite_character(user_id = request_body_favorite_character['user_id'], character_id = request_body_favorite_character['character_id'])
    db.session.add(new_favorite_character)
    db.session.commit()
    response = {'msg': 'ok'}
    return jsonify(response), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json()
    planet = Planets(name = body['name'], gravity = body['gravity'], population = body['population'])
    db.session.add(planet)
    try: 
        db.session.commit()
        return jsonify({'response': 'ok'}), 200
    except: 

        return 'error al crear el usuario', 400
    
    
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200


@app.route('/favorite/planet', methods=['GET'])
def get_favorite_planet():
    # Obtener todos los objetos favorite_planet
    planet_favorite = favorite_planet.query.all()

    # Serializar los objetos favorite_planet, incluyendo el nombre del planeta asociado
    all_planet_favorite = []
    for favorite in planet_favorite:
        serialized_favorite = favorite.serialize()
        # Obtener el nombre del planeta asociado
        serialized_favorite['planet_name'] = favorite.planet.name if favorite.planet else None
        all_planet_favorite.append(serialized_favorite)

    return jsonify(all_planet_favorite), 200

@app.route('/favorite/planet', methods = ['POST'])
def add_favorite_planet():
    request_body_favorite_planet = request.get_json()
    new_favorite_planet = favorite_planet(user_id = request_body_favorite_planet['user_id'], planet_id = request_body_favorite_planet['planet_id'])
    db.session.add(new_favorite_planet)
    db.session.commit()
    response = {'msg': 'ok'}
    return jsonify(response), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
