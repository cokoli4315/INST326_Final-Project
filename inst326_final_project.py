"""A program that looks through posts on the subreddit r/movies and comments information about an actor if they are mentioned.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project
Date: 4_14_22
Challenges Encountered: 
"""
# by Friday, 4/29: have Actor class mostly done, find_actor_name/page mostly done, & publish_comment mostly done
import csv
import json
from nis import match
from imdb.Person import Person
from imdb import Cinemagoer
import datetime
import praw
import re
import requests

# McKenna & Declan
class Actor:
    """Captures and holds information about an actor using an IMDB page.
    
    Attributes:
        name (str): full name of  actor
        age (int): current age of actor
        dob (str): date of birth of actor
        pob (str): place actor was born
        works (list of strings): 3-5 of the actor's most popular movies/shows with title & year released
        awards (list of strings): 3-5 of the actor's most recent awards
    """

    def __init__(self, actor_id):
        """Sets the attributes for the Actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Side Effects:
            Sets name, age, dob, pob, works, and awards attributes
        """
        imdb = Cinemagoer()

        actor = imdb.get_person('0000115')
        self.name = actor.get('name')
        
        birthday = actor.get('birth date')
        birthday_list = birthday.split('-')
        
        today = datetime.date.today()
        birthdate = datetime.date(int(birthday_list[0]), int(birthday_list[1]), int(birthday_list[2]))
        self.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        
        datetime_birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        self.dob = datetime_birthday.strftime('%B %d, %Y')
        
        self.pob = actor.get('birth info')['birth place']
        
        self.movies = self.get_popular_movies(actor_id)
        self.awards = self.get_recent_awards(actor_id)

    def get_popular_movies(self, actor_id):
        """Gets 3-5 of the most popular movies with the actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Returns:
            works (list of strings): 3-5 of the actor's most popular movies/shows with title & year released
        """
        # uses data.tsv file since Cinemagoer does not store actor's "Known For" list
        pass
    
    def get_recent_awards(self, actor_id):
        """Gets 3-5 of the most recent awards the actor won.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Returns:
            awards (list of strings): 3-5 of the actor's most recent awards 
        """
        # uses web scraping since Cinemagoer does not store actor's awards
        pass
    
def get_post(post):
    """Accesses each post in r/movies.
    
    Args:
        post (Reddit object): current Reddit post being examined
        
    Returns:
        a tuple with the title (str) and the ID number (int) of the Reddit post currently being looked at
    """
    return post.title, post.id

# Chikezie        
def find_actor(post_title):
    """Looks for an actor's name in the title of a post using regex.
    
    Args:
        post_title (str): the title of the post being examined
        
    Returns:
        page_id (int): the IMDB page id of the actor's page taken from find_actor_page
    """
    actor_names=[]
    tsv_file=open("data.tsv")
    read_tsv=csv.reader(tsv_file,delimiter="\t")

    for row in read_tsv:
        actor_names.append(row[1])

    print(actor_names[1])

    for indv in actor_names:
        if indv in post_title:
            actor_name=indv
    tsv_file.close()
        
       
    return actor_name

# Chikezie
def find_actor_page(actor_name):

    """Looks through IMDB for the actor's page.
    
    Args:
        actor_name (str): the name of the actor
        
    Returns: 
        page_id (int): the IMDB page id of the actor's page
    """ 
    
    actor_names=[]
    actor_id=[]
    actor_id_name={}
    tsv_file=open("data.tsv")
    read_tsv=csv.reader(tsv_file,delimiter="\t")

    for row in read_tsv:
        actor_names.append(row[1])
        actor_id.append(row[0])

    index=-1
    for indv in actor_names:
        index+=1
        for j in range(len(actor_id)):
            actor_id_name[indv]=actor_id[index]

    url=f"https://imdb-api.com/API/Name/k_gwul40q2/{actor_id_name[actor_name]}"

    return actor_id_name[actor_name]

# Surafel
def create_comment(actor):
    """Creates a string comment with an Actor object's attributes.
    
    Args:
        actor (Actor): the actor the comment is about
        
    Returns:
        comment (str): hold all the info about the actor parameter
    """


    actor_name = f"Actor's Name: {actor.name}"
    actor_age = f"Actor's Age: {actor.age}"
    actor_dob = f"Actor's Date of Birth: {actor.dob}"
    actor_pob = f"Actor's Place of Birth: {actor.pob}"

    actor_works_comment = ""
    for work in actor.works:
        actor_works_comment += f"{work}"
    
    actor_awards_comment = ""
    for award in actor.awards:
        actor_awards_comment += f"{award}"
    
    return actor_name + "\n" + actor_age + "\n" + actor_dob + "\n" + actor_pob + "\n" + actor_works_comment + "\n" + actor_awards_comment

    # ex: f"Actor's Name: {actor.name}\n Actor's Age: {actor.age} \n"
    # actor.age calculated in actor class init
    # make sure when you print the movies & awards list you are using a loop and printing out each element (for formatting)
    pass

# Surafel
def publish_comment(post_id, comment):
    """Comments a string to a Reddit post.
    
    Args:
        post_id (int): the ID of the post that has the actor's name in it
        comment (str): the comment that will be published to the post
    """
    post_id.reply(comment) 
    # take comment & publish it to reddit post_id as a comment (look at Reddit API on how to do that)
    pass

# McKenna & Declan
def main():
    """Runs the entire program. Calls get_post(), calls find_actor() using title, if a page for the actor is found creates an Actor instance, 
    calls create_comment() using the Actor instance, calls publish_comment() using the return of create_comment()"""
    # gets access to reddit
    reddit = praw.Reddit(
        client_id = "_0kHj0UNHLgsztUOBVIYXg",
        client_secret = "dgjr6dsvP1CXB_N1jzN5ng08rUQEQw",
        # fix user_agent
        user_agent = "<platform>:<app ID>:<version string> (by u/INSTbot)",
        username = "INSTbot",
        password = "inst326project",
    )
    
    movies_sub = reddit.subreddit("movies")
    
    # for testing, will use specific Reddit posts already identified
    # put Reddit posts here
    # test reddit part
    
    # will be used in final, not for testing purposes
    for submission in movies_sub.new(limit=10):
        post_title, post_id = get_post(submission)
        actor_page = find_actor(post_title)
        
        # is imdb page ID & actor ID the same?
        if actor_page != None:
            actor = Actor(actor_page)
            
            comment = create_comment(actor)
            publish_comment(post_id, comment)

if __name__ == "__main__":
    # calls main to run program
    main()