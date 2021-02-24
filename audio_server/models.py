from .extensions import db

class Song(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    upload = db.Column(db.DateTime, nullable=False)

class Podcast(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    upload = db.Column(db.DateTime, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.Integer, nullable=True)

class Audiobook(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    upload = db.Column(db.DateTime, nullable=False)
