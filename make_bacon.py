import gzip
import bacon_functions
from app import db, Actor, Movie
import codecs

# def pickle_dump(obj, file_name):
#     f = open(file_name, 'w')
#     cPickle.dump(obj, f)
#     f.close()

def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance, True

if __name__ == "__main__":
    # Parsing file of actors (male)
    imdb_actors_file = gzip.open("data/actors.list.gz")
    # imdb_actors_file = codecs.getreader("utf-8")(gzip.open('data/actors.list.gz'))
    print 'Parsing file (actors.list) of actors (male) ...'
    for row in bacon_functions.parse_actor_data(imdb_actors_file):
        for actor, movies in row.items():
            ms = []
            for movie in movies:
                print movie
                m, created = get_or_create(Movie, name=movie.decode('latin-1'))
                ms.append(m)
            print actor
            a = Actor(name=actor.decode('latin-1'))
            a.movies = ms
            db.session.add(a)
            db.session.commit()
    imdb_actors_file.close()

    # Parsing file of actors (female)
   #imdb_actresses_file = open("actresses.list")
   #print 'Parsing file (actresses.list) of actresses (female) ...'
   #actresses_dict = bacon_functions.parse_actor_data(imdb_actresses_file)
   #imdb_actresses_file.close()

   ## thanks for the quick reminder: http://stackoverflow.com/a/38990
   ## Merging both the (actors to movies) data structures
   #print 'Merging both the (actors to movies) data structures ...'
   #actors_to_movies = dict(actors_dict.items() + actresses_dict.items())

   ## Creating a movies to actors data structure
   #print 'Creating a movies to actors data structure ...'
   #movies_to_actors = bacon_functions.invert_actor_dict(actors_to_movies)

   ## Pickling both the data structures
   ## Pickling the actors to movies data structure
   #print 'Pickling the actors to movies data structure ...'
   #pickle_dump(actors_to_movies, 'actors_to_movies')
   ## Pickling the actors to movies data structure
   #print 'Pickling the actors to movies data structure ...'
   #pickle_dump(movies_to_actors, 'movies_to_actors')

   #print 'Done! Run bacon.py to begin playing!'
