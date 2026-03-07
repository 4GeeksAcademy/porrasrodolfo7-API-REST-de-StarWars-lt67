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
from models import db, User_sw, Personajes, Planetas, Personajesfavoritos, Planetasfavoritos
from sqlalchemy import select
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


#B E G I N

@app.route('/user_sw', methods=['GET'])
def get_users():
    all_users = User_sw.query.all()
    #all_users = db.session.execute(select(User_sw)).scalars().all()
    results = list(map(lambda user: user.serialize(), all_users))
    return jsonify(results), 200

@app.route('/user_sw/<int:user_id>', methods=['GET'])
def get_usersw(user_id):
    user = User_sw.query.filter_by(id=user_id).first()
    
    return jsonify(user.serialize()), 200


@app.route('/user_sw/favorites', methods=['GET'])
def get_user_favorites():
    user = User_sw.query.get(1)

    personajes_fav = list(map(lambda fper: fper.serialize(), user.personajes_fav))
    planetas_fav = list(map(lambda fpla: fpla.serialize(), user.planetas_fav))

    return jsonify({
        "usuario": user.username,
        "personajes_favoritos": personajes_fav,
        "planetas_favoritos": planetas_fav
    })



@app.route('/personajes', methods=['GET'])
def get_personajes():
    all_personajes = Personajes.query.all()
    results = list(map(lambda personaje: personaje.serialize(), all_personajes))
    return jsonify(results), 200


@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = Personajes.query.get(personaje_id)
    if personaje is None:
        return {"msg": "El personaje no existe, mi pana"}, 404
    
    return jsonify(personaje.serialize()), 200


@app.route('/personajes', methods=['POST'])
def add_personaje():
    body = request.get_json()
    campos_requeridos = ["nombre", "raza", "genero", "color_de_ojos", "color_de_piel" ]
    for campo in campos_requeridos:
        if campo not in body:
            return jsonify({"msg": f"El campo {campo} es obligatorio"}), 400
        if str(body[campo]) == "":
            return jsonify({"msg": f"El campo {campo} no puede quedar vacio"}), 400
        
    personaje = Personajes(**body)
    db.session.add(personaje)
    db.session.commit()

    return jsonify(personaje.serialize()), 200


@app.route('/favoritos/personajes', methods=['POST'])
def add_personaje_favorito():
    body = request.get_json()

    personaje = Personajes.query.get(body["personaje_id"])
    if personaje is None:
        return jsonify({"msg": "El personaje que intentas agregar no existe"}), 404
    
    new_fav = Personajesfavoritos (
        user_sw_id = 1,
        personajes_id = body["personaje_id"]
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 200


@app.route('/personajes/<int:personaje_id>', methods=['DELETE'])
def delete_personaje(personaje_id):
    personaje = db.session.get(Personajes, personaje_id)
    if personaje is None:
        return {"msg": "El personaje no existe"}, 404

    db.session.delete(personaje)
    db.session.commit()

    response_body = {
        "msg" : "Se elimino el personaje"
    }
        
    return jsonify(response_body), 200


@app.route('/planetas', methods=['POST'])
def add_planeta():
    body = request.get_json()
    campos_requeridos = ["nombre", "poblacion", "terreno", "clima", "diametro" ]
    for campo in campos_requeridos:
        if campo not in body:
            return jsonify({"msg": f"El campo {campo} es obligatorio"}), 400
        if str(body[campo]) == "":
            return jsonify({"msg": f"El campo {campo} no puede quedar vacio"}), 400
        
    planeta = Planetas(**body)
    db.session.add(planeta)
    db.session.commit()

    return jsonify(planeta.serialize()), 200


@app.route('/planetas/<int:planeta_id>', methods=['DELETE'])
def delete_planetas(planeta_id):
    planeta = db.session.get(Planetas, planeta_id)
    if planeta is None:
        return {"msg": "El planeta no existe"}, 404

    db.session.delete(planeta)
    db.session.commit()

    response_body = {
        "msg" : "Se elimino el planeta"
    }
        

    return jsonify(response_body), 200


@app.route('/planetas', methods=['GET'])
def get_planetas():
    all_planetas = Planetas.query.all()
    results = list(map(lambda planeta: planeta.serialize(), all_planetas))
    return jsonify(results), 200


@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta is None:
        return {"msg": "El planeta no existe, bro"}, 404
    
    return jsonify(planeta.serialize()), 200


@app.route('/favoritos/planetas', methods=['POST'])
def add_planeta_favorito():
    body = request.get_json()

    planeta = Planetas.query.get(body["planeta_id"])
    if planeta is None:
        return jsonify({"msg": "El planeta que intentas agregar no existe"}), 404
    
    new_fav = Planetasfavoritos (
        user_sw_id = 1,
        planetas_id = body["planeta_id"]
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
