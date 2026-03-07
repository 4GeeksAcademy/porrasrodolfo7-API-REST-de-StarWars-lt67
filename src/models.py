from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

    
class User_sw (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fecha: Mapped[str] = mapped_column(String(120), nullable=False)

    personajes_fav: Mapped[List["Personajesfavoritos"]] = relationship(back_populates="user_sw")
    planetas_fav: Mapped[List["Planetasfavoritos"]] = relationship(back_populates="user_sw")
    
    def __repr__(self):
        return f"{self.username}" 

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha": self.fecha,
            # do not serialize the password, its a security breach
        }

class Personajes (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    raza: Mapped[str] = mapped_column(String(120), nullable=False)
    genero: Mapped[str] = mapped_column(String(120), nullable=False)
    color_de_ojos: Mapped[str] = mapped_column(String(120), nullable=False)
    color_de_piel: Mapped[str] = mapped_column(String(120), nullable=False)

    personajes_fav: Mapped[List["Personajesfavoritos"]] = relationship(back_populates="personajes")
    
    def __repr__(self):
        return f"{self.nombre}"  

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "raza": self.raza,
            "genero": self.genero,
            "color_de_ojos": self.color_de_ojos,
            "color_de_piel": self.color_de_piel
            # do not serialize the password, its a security breach
        }    

class Planetas (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    poblacion: Mapped[str] = mapped_column(String(120),  nullable=False)
    terreno: Mapped[str] = mapped_column(String(120),  nullable=False)
    diametro: Mapped[int] = mapped_column(Integer, nullable=True)
    clima: Mapped[str] = mapped_column(String(120), nullable=False)

    planetas_fav: Mapped[List["Planetasfavoritos"]] = relationship(back_populates="planetas")
  
    def __repr__(self):
        return f"{self.nombre}" 

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "terreno": self.terreno,
            "diametro": self.diametro,
            "clima": self.clima
            # do not serialize the password, its a security breach
        }    
    
class Personajesfavoritos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_sw_id: Mapped[int] = mapped_column(ForeignKey("user_sw.id"))
    user_sw: Mapped["User_sw"] = relationship(back_populates="personajes_fav")

    personajes_id: Mapped[int] = mapped_column(ForeignKey("personajes.id"))
    personajes: Mapped["Personajes"] = relationship(back_populates="personajes_fav")


    def serialize(self):
        return {
            "id": self.id,
            "personaje": self.personajes.serialize()
            # do not serialize the password, its a security breach
        }
    
class Planetasfavoritos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_sw_id: Mapped[int] = mapped_column(ForeignKey("user_sw.id"))
    user_sw: Mapped["User_sw"] = relationship(back_populates="planetas_fav")

    planetas_id: Mapped[int] = mapped_column(ForeignKey("planetas.id"))
    planetas: Mapped["Planetas"] = relationship(back_populates="planetas_fav")


    def serialize(self):
        return {
            "id": self.id,
            "planeta": self.planetas.serialize()
            # do not serialize the password, its a security breach
        }