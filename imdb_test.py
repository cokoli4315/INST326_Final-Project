#from imdb.Person import Person
from imdb import Cinemagoer

#print(Person.default_info)

"""# create an instance of the Cinemagoer class
ia = Cinemagoer()

# get a movie
movie = ia.get_movie('0133093')

# print the names of the directors of the movie
print('Directors:')
for director in movie['directors']:
    print(director['name'])

# print the genres of the movie
print('Genres:')
for genre in movie['genres']:
    print(genre)

# search for a person name
people = ia.search_person('Mel Gibson')
for person in people:
   print(person.personID, person['name'])"""
   
# example code
imdb = Cinemagoer()
movie = imdb.get_movie('0109830')
if movie.get('title') != "Forrest Gump":
    print('False')
    
#movie = ia.get_movie('0094226', info=['taglines', 'plot'])
#movie.infoset2keys

nic_cage = imdb.get_person(115)
print(imdb.get_person('0000115'))
# {'main': ['birth info', 'headshot', 'akas', 'filmography', 'in development', 'imdbID', 'name'], 
# 'biography': ['headshot', 'nick names', 'birth name', 'height', 'mini biography', 'trade mark', 'trivia', 'quotes', 'salary history', 'birth date', 'birth notes']}
nic_cage = imdb.get_person('0000115')
print(nic_cage.get('birth name'))