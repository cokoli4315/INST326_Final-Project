"""Tests the Reddit bot for our final project.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project Unit Tests
Date: 4_14_22
"""
# only need to test for happy cases

import inst326_final_project as fp

def test_get_post():
    assert fp.get_post("movies") == "u4965x"
    assert fp.get_post("movies") == "u3xc2o"
    assert fp.get_post("movies") == "u3qb8r"
    assert fp.get_post("movies") == "u4bff5"

def test_get_title():
    assert fp.get_title("u4965x") == "Nicolas Cage Says He's Done His Best Work in the Last 10 Years"
    assert fp.get_title("u3xc2o") == "Blade Runner (1982) Deckard never speaks to Roy, is there any other movie that never has the protagonist speak to the antagonist?"
    assert fp.get_title("u3qb8r") == "21 years since Rat Race, Its time for another \"Big ensemble cast of actors chase around America for money\" movie"
    assert fp.get_title("u4bff5") == "Ryan Reynolds To Narrate Discovery+ Documentary 'Curb Your Carbon'"

def test_find_actor_name():
    assert fp.find_actor_name("Nicolas Cage Says He's Done His Best Work in the Last 10 Years") == "Nicolas Cage"
    assert fp.find_actor_name("Blade Runner (1982) Deckard never speaks to Roy, is there any other movie that never has the protagonist speak to the antagonist?") == None
    assert fp.find_actor_name("21 years since Rat Race, Its time for another \"Big ensemble cast of actors chase around America for money\" movie") == None
    assert fp.find_actor_name("Ryan Reynolds To Narrate Discovery+ Documentary 'Curb Your Carbon'") == "Ryan Reynolds"

def test_find_actor_page():
    # if find_actor_name returns None, find_actor_page is not called
    # fix leading zeros
    assert fp.find_actor_page("Nicolas Cage") == "0000115" # this returns true if the post_id is assigned to Nicolas Cage
    assert fp.find_actor_page("Ryan Reynolds") == "0005351" # returns true if post_id is assigned to Ryan Reynolds

def test_create_comment():
    nic_cage = fp.Actor(fp.find_actor_page("Nicolas Cage"))
    assert fp.create_comment(nic_cage) == "Actor's Name: Nicolas Cage\nAge: 58\nDate of Birth: January 7, 1964\nPlace of Birth: Long Beach, California, USA\nMovies: Face/Off (1997), Leaving Las Vegas (1995), The Rock (1996), Next (2007)\nAwards Won: Best Actor, Best Actor in a Leading Role"
    ryan_reynolds = fp.Actor(fp.find_actor_page("Ryan Reynolds"))
    assert fp.create_comment(ryan_reynolds) == "Actor's Name: Ryan Reynolds\nAge: 45\nDate of Birth: October 23, 1976\nPlace of Birth: Vancouver, British Columbia, Canada\nMovies: Deadpool 2 (2018), Deadpool (2016), Buried (2010), The Proposal (2009)\nAwards: Best Actor, Best Actor in a Comedy, Favorite Celebrity of the Year"