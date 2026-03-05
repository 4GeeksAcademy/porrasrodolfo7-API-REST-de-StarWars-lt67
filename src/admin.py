import os
from flask_admin import Admin
from models import db, User_sw, Personajes, Planetas, Personajesfavoritos, Planetasfavoritos
from flask_admin.contrib.sqla import ModelView


class PersonajesFavoritosAdmin(ModelView):
    column_list = ('id', 'user_sw', 'personajes')
    form_columns = ('user_sw', 'personajes')

class PlanetasFavoritosAdmin(ModelView):
    column_list = ('id', 'user_sw', 'planetas')
    form_columns = ('user_sw', 'planetas')

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    

    admin.add_view(ModelView(User_sw, db.session, name="Users"))

    admin.add_view(ModelView(Personajes, db.session))

    admin.add_view(ModelView(Planetas, db.session))

    admin.add_view(PersonajesFavoritosAdmin(Personajesfavoritos, db.session, name="Personajes Favoritos"))
    admin.add_view(PlanetasFavoritosAdmin(Planetasfavoritos, db.session, name="Planetas Favoritos"))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))