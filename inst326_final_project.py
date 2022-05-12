"""A program that looks through posts on the subreddit r/movies and comments information about an actor if they are mentioned in the post title.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project
Date: 4_14_22
Challenges Encountered: learning about the APIs we are using, figuring out how to find an actor's name in a title, 
getting an actor's most popular movies (stored in their "known for" list of IMDB), getting awards won by an actor
"""
import csv
from imdb import Cinemagoer
import datetime
import praw
import re
import requests
from bs4 import BeautifulSoup
import string

class Actor:
    """Captures and holds information about an actor using an IMDB page.
    
    Attributes:
        name (str): full name of actor
        age (int/str): current age of actor or age at passing if actor has died (as a str)
        dob (str): date of birth of actor
        pob (str): place actor was born
        works (list of strings): 4 of the actor's most popular movies/shows with title & year released
        awards (list of strings): 3-5 of some of the awards the actor has won
    """
    # McKenna & Chikezie
    def __init__(self, actor_id):
        """Sets the attributes for the Actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Side Effects:
            Sets name, age, dob, pob, works, and awards attributes
        """
        imdb = Cinemagoer()

        actor = imdb.get_person(actor_id)
        self.name = actor.get('name')
        
        birthday = actor.get('birth date')
            
        birthday_list = birthday.split('-')
        birthdate = datetime.date(int(birthday_list[0]), int(birthday_list[1]), int(birthday_list[2]))
        
        deathday = actor.get('death date')
        if deathday:
            death_date_list = deathday.split('-')
            death_date = datetime.date(int(death_date_list[0]), int(death_date_list[1]), int(death_date_list[2]))
        
            self.age = death_date.year - birthdate.year - ((death_date.month, death_date.day) < (birthdate.month, birthdate.day))
            self.age = str(self.age) + " (at passing)"
        else:
            today = datetime.date.today()
            self.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    
        datetime_birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        self.dob = datetime_birthday.strftime('%B %d, %Y')
        
        try:
            self.pob = actor.get('birth info')['birth place']
        except TypeError:
            self.pob = 'Could not find one'
        
        self.works = self.get_popular_movies(actor_id)
        self.awards = self.get_actor_awards(actor_id)

    # McKenna & Declan
    def get_popular_movies(self, actor_id):
        """Gets 3-5 of the most popular movies with the actor using a TSV file.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Returns:
            works (list of strings): 3-5 of the actor's most popular movies/shows with title & year released
        """
        # look thru data.tsv for actor_id ('nm'+str(actor_id)), access row with their info, get last column (col[5]) that has  known for movies
        # split last col into a list using known_for = row[5].split(','), substring off the "tt" at the beginning of each movie id
        # use imdb.get_movie(movie_id) to get the Movie object of each movie, add each movie to the works attribute (code below)
        imdb = Cinemagoer()
        
        self.works = []
        known_for = []

        target_row = open_tsv_file('nm'+actor_id, 0)
        known_for = target_row[5].split(',')

        count = 0
        for film in known_for:
            movie_code = film[2:]
            known_for[count] = imdb.get_movie(movie_code)
            count+=1

        for work in known_for:
            self.works.append(f"{work.data['title']} ({work.data['year']})")
                
        return self.works
    
    # McKenna & Declan
    def get_actor_awards(self, actor_id):
        """Gets 3-5 of the most recent awards the actor won using web scraping.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Returns:
            awards (list of strings): 3-5 of the actor's most recent awards 
        """
        actor_awards_page = f"https://www.imdb.com/name/nm{actor_id}/awards?ref_=nm_awd"
        request_page = requests.get(actor_awards_page)
        soup = BeautifulSoup(request_page.text, "html.parser")
        all_awards = soup.find_all("tr")

        awards_won = []
        for count, award in enumerate(all_awards):
            try:
                award_outcome = award.b.contents[0]
                if award_outcome == "Winner":
                    awards_won.append(award)
            except AttributeError:
                continue
            except IndexError:
                break
        
        self.awards = []
        for count, award in enumerate(awards_won):
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
                self.awards.append(str(award_year) + " " + str(award_category) + " for " + str(award_description))
                
            if count > 3:
                break
        
        return self.awards
    
def get_post(post):
    """Accesses each post in r/movies.
    
    Args:
        post (Reddit object): current Reddit post being examined
        
    Returns:
        a tuple with the title (str) and the ID number (int) of the Reddit post currently being looked at
    """
    return post.title, post.id

# Chikezie & Surafel    
def find_actor(post_title, actor_names):
    """Looks for an actor's name in the title of a post using a csv file.
    
    Args:
        post_title (str): the title of the post being examined
        
    Returns:
        page_id (int): the IMDB page id of the actor's page taken from find_actor_page
    """
    title = post_title.split(' ')
    title_pairs = []

    first_word = title[0]
    for count, word in enumerate(title[1:]):
        if word[-2:] == "'s":
            word = word.replace(word, word[0:-2])
            
        word = word.replace(word, word.strip(string.punctuation))
        
        if count == 0:
            title_pairs.append(first_word + ' ' + word)
        else:
            title_pairs.append(title[count] + ' ' + word)
    
    actor_name = ''
    actor_page = ''
    
    for title_pair in title_pairs:
        if title_pair in actor_names:
            actor_name = title_pair
            actor_page = find_actor_page(actor_name)
            
            if actor_page != None:
                break
            
            actor_name = ''
    
    if actor_name != '':
        return actor_page
    
    return None

# Chikezie & Surafel
def find_actor_page(actor_name):

    """Looks through IMDB for the actor's page.
    
    Args:
        actor_name (str): the name of the actor
        
    Returns: 
        page_id (int): the IMDB page id of the actor's page
    """ 
    target_row = open_tsv_file(actor_name, 1)
    
    if target_row != None:
        profession = target_row[4].split(',')
    
        if ('actor' in profession or 'actress' in profession) and target_row[2] != '\\N':
            page_id = target_row[0]
            return page_id[2:]
    
    return None

# Surafel & McKenna
def create_comment(actor, actor_id):
    """Creates a string comment with an Actor object's attributes.
    
    Args:
        actor (Actor): the actor the comment is about
        
    Returns:
        comment (str): hold all the info about the actor parameter
    """
    actor_name = f"**Actor's Name:** {actor.name}    "
    actor_age = f"**Actor's Age:** {actor.age}    "
    actor_dob = f"**Actor's Date of Birth:** {actor.dob}    "
    actor_pob = f"**Actor's Place of Birth:** {actor.pob}    "

    actor_works_comment = "**Popular Works:**    "
    for count, work in enumerate(actor.works):
        actor_works_comment += f"""    
            {count+1}. {work}"""
    
    actor_awards_comment = "**Some Awards Won:**    "
    if actor.awards:
        for count, award in enumerate(actor.awards):
            actor_awards_comment += f"""    
            {count+1}. {award}"""
    else:
        actor_awards_comment += " Could not find any    "
        
    mistakes_message = f"""This bot gives information about the first actor mentioned in a post title on r/movies, but sometimes mistakes are made. 
Click [here](https://www.imdb.com/name/nm{actor_id}/) to learn more about the actor found for this post!"""
    
    return (actor_name + """ 
""" + actor_age + """ 
""" + actor_dob + """ 
""" + actor_pob + """ 
""" + actor_works_comment + """    
""" + actor_awards_comment + """ 
 
""" + mistakes_message)

# Surafel & McKenna
def publish_comment(post, comment):
    """Comments a string to a Reddit post.
    
    Args:
        post_id (int): the ID of the post that has the actor's name in it
        comment (str): the comment that will be published to the post"""
    
    post.reply(comment)

# Chikezie, & Surafel
def open_tsv_file(target, row_num):
    """Opens the TSV file once to be used for other functions.
    """
    # take in str arg called target (can be actor_id or actor_name so it fits for the multiple uses), 
    # opens tsv, goes through file and returns entire row if target is found
    tsv_file=open('data.tsv', encoding='utf8')
    read_tsv=csv.reader(tsv_file,delimiter="\t")
    
    for row in read_tsv:
        if row[row_num] == target:
            return row
        
def get_imdb_actor_names():
    actor_names=[]
    
    file = open("data.tsv", encoding='utf8')
    read_tsv = csv.reader(file,delimiter="\t")
    
    for row in read_tsv:
        actor_names.append(row[1])
    
    file.close()
    
    return actor_names

# Chikenzie & Declan
def main():
    """Runs the entire program. Calls get_post(), calls find_actor() using title, if a page for the actor is found creates an Actor instance, 
    calls create_comment() using the Actor instance, calls publish_comment() using the return of create_comment()."""
    # gets access to reddit
    reddit = praw.Reddit(
        client_id = "_0kHj0UNHLgsztUOBVIYXg",
        client_secret = "dgjr6dsvP1CXB_N1jzN5ng08rUQEQw",
        # fix user_agent
        user_agent = "<platform>:<app ID>:<version string> (by u/INSTbot)",
        username = "INSTbot",
        password = "inst326project",
    )
    
    actor_names = get_imdb_actor_names()
    movies_sub = reddit.subreddit("movies")
    
    for count, submission in enumerate(movies_sub.new(limit=15)):
        post_title, post_id = get_post(submission)
        print(f"\n\033[1mPost #{count+1} Title:\033[0m \"{post_title}\" \t \033[1mPost ID:\033[0m {post_id}")
        actor_page = find_actor(post_title, actor_names)
        print(f"\033[1mActor IMDB Page ID:\033[0m {actor_page}")
   
        if actor_page != None:
            actor = Actor(actor_page)
            
            comment = create_comment(actor, actor_page)
            print('\n\033[1mPost Comment:\033[0m \n"' + comment + '"')
            publish_comment(submission, comment)
            print('\nPublished comment! Check Reddit post for comment.')

if __name__ == "__main__":
    # calls main to run program
    main()