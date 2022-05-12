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
    
# movie = imdb.get_movie()
#movie.infoset2keys

# {'main': ['birth info', 'headshot', 'akas', 'filmography', 'in development', 'imdbID', 'name'], 
# 'biography': ['headshot', 'nick names', 'birth name', 'height', 'mini biography', 'trade mark', 'trivia', 'quotes', 'salary history', 'birth date', 'birth notes']}
nic_cage = imdb.get_person('0695435')
"""print(nic_cage.get('name'))
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

import csv

actor_names=[]
tsv_file=open("data.tsv", encoding='utf8')
read_tsv=csv.reader(tsv_file,delimiter="\t")

for i, row in enumerate(read_tsv):
    # actor known for: row[5]
    known_for = row[5].split(',')
    
    if i==2:
        break

tsv_file.close()"""

import requests
import re
from bs4 import BeautifulSoup

actor_awards_page = f"https://www.imdb.com/name/nm{nic_cage.get('imdbID')}/awards?ref_=nm_awd"
request_page = requests.get(actor_awards_page)
soup = BeautifulSoup(request_page.text, "html.parser")
# fix this so it does not go past awards tables
all_awards = soup.find_all("tr")

awards_won = []
for count, award in enumerate(all_awards):
    try:
        award_outcome = award.b.contents[0]
        if award_outcome == "Winner":
            awards_won.append(award)
        if count > 6:
            break
    except AttributeError:
        continue
    
print(len(awards_won))
awards = []
for award in awards_won:
    award_html = award.find_all("td")

    award_year = re.findall(r"> (\d{4})", str(award_html[0].contents[1]))
    if award_year:
        award_year = award_year[0]
    award_category = re.findall(r"\"award_category\">(.*)<", str(award_html[1].contents[4]))
    if award_category:
        award_category = award_category[0]
    award_description = ''
    if len(award_html) > 2:
        award_description = award_html[2].contents[0].lstrip()
    
    if award_year and award_category and award_description:
        awards.append(str(award_year) + " " + str(award_category) + " for " + str(award_description))
    
print(awards)

"""import csv

filename = "data.tsv"
target = 'nm'+"0000115"
row_num = 0

def open_tsv_file(filename, target, row_num):
    Opens the TSV file once to be used for other functions.
    # work on this more once we've decided where/how we are using data.tsv
    # might call find_actor & find_actor_page here
    # take in str arg called target (can be actor_id or actor_name), opens tsv, goes through file and returns entire row if target is found
    tsv_file=open(filename, encoding='utf8')
    read_tsv=csv.reader(tsv_file,delimiter="\t")
    for row in read_tsv:
        if row[row_num] == target:
            return row
        
works = []
actor_id = "0000115"
known_for = []

target_row = open_tsv_file("data.tsv", 'nm'+actor_id, 0)
known_for = target_row[5].split(',')

count = 0    
for film in known_for:
    movie_code = film[2:]
    known_for[count] = imdb.get_movie(movie_code)
    count+=1

for work in known_for:
    works.append(f"Title: {work.data['title']}, Year: {work.data['year']}")
    
print(works)"""

"""post_title = 'What are some non-American actors who suck at doing American accent?'
title = post_title.split(' ')
title_list = []

first_word = title[0]
for count, word in enumerate(title[1:]):
    if count == 0:
        title_list.append(first_word + ' ' + word)
    else:
        title_list.append(title[count] + ' ' + word)
        
print(title_list)"""

from prompt_toolkit import print_formatted_text, HTML
actor_works_comment = str(HTML("\n<b>Popular Works:</b>"))
print(actor_works_comment)

word = "Zack Snyder's"

if word[-2:] == "'s":
    word = word[0:-2]
    
print(word)