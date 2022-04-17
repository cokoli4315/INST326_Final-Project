"""Tests the Reddit bot for our final project.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project Unit Tests
Date: 4_14_22
"""
# only need to test for happy cases

import inst326_final_project as fp

def test_get_post():
    # get post ids
    assert fp.get_post("movies") == #Nic Cage post id
    assert fp.get_post("movies") == #Blade Runner post id
    assert fp.get_post("movies") == #21 years post id
    assert fp.get_post("movies") == #Ryan Reynolds post id

def test_get_title():
    # get post ids (corresponds with above function)
    assert fp.get_title(post_id) == "Nicolas Cage Says He's Done His Best Work in the Last 10 Years"
    assert fp.get_title(post_id) == "Blade Runner (1982) Deckard never speaks to Roy, is there any other movie that never has the protagonist speak to the antagonist?"
    assert fp.get_title(post_id) == "21 years since Rat Race, Its time for another \"Big ensemble cast of actors chase around America for money\" movie"
    assert fp.get_title(post_id) == "Ryan Reynolds To Narrate Discovery+ Documentary 'Curb Your Carbon'"

def test_find_actor_name():
    assert fp.find_actor_name("Nicolas Cage Says He's Done His Best Work in the Last 10 Years") == "Nicolas Cage"
    assert fp.find_actor_name("Blade Runner (1982) Deckard never speaks to Roy, is there any other movie that never has the protagonist speak to the antagonist?") == None
    assert fp.find_actor_name("21 years since Rat Race, Its time for another \"Big ensemble cast of actors chase around America for money\" movie") == None
    assert fp.find_actor_name("Ryan Reynolds To Narrate Discovery+ Documentary 'Curb Your Carbon'") == "Ryan Reynolds"

def test_find_actor_page():
    # if find_actor_name returns None, find_actor_page is not called
    # fix leading zeros
    assert fp.find_actor_page("Nicolas Cage") == 0000115
    assert fp.find_actor_page("Ryan Reynolds") == 0005351

def test_create_comment():
    # write the actual comment strings
    nic_cage = fp.Actor(fp.find_actor_page("Nicolas Cage"))
    assert fp.create_comment(nic_cage) == "comment"
    ryan_reynolds = fp.Actor(fp.find_actor_page("Ryan Reynolds"))
    assert fp.create_comment(ryan_reynolds) == "comment"