from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), index=True)
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(250), unique=True)
    gravity = db.Column(db.String(250))
    population = db.Column(db.String(250))

    def __repr__(self):
        return f'<Planet planets_name={self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "population": self.population
        }

class favorite_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planets_id = db.Column(db.Integer, db.ForeignKey(Planets.id))
    Planet = db.relationship('Planets')

    def __repr__(self):
        return f'<favorite_planet user_id={self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planets_id,
            "name": self.planets.name if self.planets else None
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    homeworld = db.Colum(db.Integer, db.ForeingnKey('planets.id'))

    def __repr__(self):
        return f'<Character name={self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "homeworld": self.homeworld,
        }
    
class favorite_character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    character_id = db.Column(db.Integer, db.ForeignKey(Character.id))
    character = db.relationship('Character')

    def __repr__(self):
        return f'<favorite_character user_id={self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "character_name": self.character.name if self.character else None
        }