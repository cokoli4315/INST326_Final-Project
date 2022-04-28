"""A program that looks through posts on the subreddit r/movies and comments information about an actor if they are mentioned.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project
Date: 4_14_22
Challenges Encountered: 
"""
# by Friday, 4/29: have Actor class mostly done, find_actor_name/page mostly done, & publish_comment mostly done
from imdb.Person import Person
from imdb import Cinemagoer
import datetime
import praw
import re

# McKenna & Declan
class Actor:
    """Captures and holds information about an actor using an IMDB page.
    
    Attributes:
        name (str): full name of  actor
        age (int): current age of actor
        dob (str): date of birth of actor
        pob (str): place actor was born
        movies (list of strings): 3-5 of the actor's most popular movies with title & year released
        awards (list of strings): 3-5 of the actor's most recent awards
    """

    def __init__(self, actor_id):
        """Sets the attributes for the Actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Side Effects:
            Sets name, age, dob, pob, movies, and awards attributes
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
            movies (list of strings): 3-5 of the actor's most popular movies with title & year released
        """
        pass
    
    def get_recent_awards(self, actor_id):
        """Gets 3-5 of the most recent awards the actor won.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Returns:
            awards (list of strings): 3-5 of the actor's most recent awards 
        """
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
    # sep title w/ spaces, loop thru title, once a regex match is found call find_actor_page(), 
    # if find_actor_page() does not find a match continue looking thru the post title for a name until you reach the end
    # return None if no actor name was found
    # if an actor is found return page_id (from find_actor_page())
    pass

# Chikezie
def find_actor_page(actor_name):
    """Looks through IMDB for the actor's page.
    
    Args:
        actor_name (str): the name of the actor
        
    Returns: 
        page_id (int): the IMDB page id of the actor's page
    """
    pass

# Surafel
def create_comment(actor):
    """Creates a string comment with an Actor object's attributes.
    
    Args:
        actor (Actor): the actor the comment is about
        
    Returns:
        comment (str): hold all the info about the actor parameter
    """
    # ex: f"Actor's Name: {actor.name}\n Actor's Age: {actor.age} \n"
    # actor.age calculated in actor class init
    pass

# Surafel
def publish_comment(post_id, comment):
    """Comments a string to a Reddit post.
    
    Args:
        post_id (int): the ID of the post that has the actor's name in it
        comment (str): the comment that will be published to the post
    """
    # take comment & publish it to reddit post_id as a comment (look at Reddit API on how to do that)
    pass

# McKenna & Declan
def main():
    """Runs the entire program. Calls get_post(), calls find_actor() using title, if a page for the actor is found creates an Actor instance, 
    calls create_comment() using the Actor instance, calls publish_comment() using the return of create_comment()"""
    # gets access to reddit, just an example not in final
    reddit = praw.Reddit(
        client_id="my client id",
        client_secret="my client secret",
        user_agent="my user agent",
        username="my username",
        password="my password",
    )
    
    movies_sub = reddit.subreddit("movies")
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