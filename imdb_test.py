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
"""movie = imdb.get_movie('0109830')
if movie.get('title') != "Forrest Gump":
    print('False')"""
    
#movie = ia.get_movie('0094226', info=['taglines', 'plot'])
#movie.infoset2keys

# {'main': ['birth info', 'headshot', 'akas', 'filmography', 'in development', 'imdbID', 'name'], 
# 'biography': ['headshot', 'nick names', 'birth name', 'height', 'mini biography', 'trade mark', 'trivia', 'quotes', 'salary history', 'birth date', 'birth notes']}
nic_cage = imdb.get_person('0000115')
print(nic_cage.get('name'))
nic_birthday = nic_cage.get('birth date') #1964-01-07

birthday_list = nic_birthday.split('-')
import datetime
 
today = datetime.date.today()
birthdate = datetime.date(int(birthday_list[0]), int(birthday_list[1]), int(birthday_list[2]))
age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
print(age)

datetimeobject = datetime.datetime.strptime(nic_birthday, '%Y-%m-%d')
new_format = datetimeobject.strftime('%B %d, %Y')
print(new_format)

nic_birth = nic_cage.get('birth info')['birth place']
print(nic_birth)

nic_films = nic_cage.get('filmography') 

for film in nic_films['actor'][0:5]:
    if 'year' in film.data: 
        print(f"Title: {film.data['title']}, Year: {film.data['year']}")
    else:
        print(f"Title: {film.data['title']}, Year: N/A")
        
import requests
from bs4 import BeautifulSoup

actor_page = f"https://www.imdb.com/name/nm{nic_cage.get('imdbID')}/"
request_page = requests.get(actor_page)
soup = BeautifulSoup(request_page.text, "html.parser")
known_for = soup.findAll("Known For")
print(known_for)