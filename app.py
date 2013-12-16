from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['BACON_CONN']
db = SQLAlchemy(app)

actor_movie = db.Table(
    'actor_movie', 
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
)

class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    movies = db.relationship('Movie', secondary=actor_movie,
        backref=db.backref('actors', lazy='dynamic'))
    
    def __unicode__(self):
        return self.name
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    def __unicode__(self):
        return self.name
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/actor/<name>/')
def actor(name):
    actors = db.session.query(Actor).filter(Actor.name.ilike('%%%s%%' % name)).all()
    data = []
    for actor in actors:
        d = actor.as_dict()
        d['movies'] = []
        for movie in actor.movies:
            d['movies'].append(movie.as_dict())
        data.append(d)
    resp = make_response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
