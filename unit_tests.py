"""Tests the Reddit bot for our final project.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project Unit Tests
Date: 4_14_22
"""
# tests as of 5/13/22 at 2:40 AM (5 newest posts on r/movies at that time)

import inst326_final_project as fp

def test_get_post():
    assert fp.get_post("uoljbe") == "Rob Reiner Confirms Sequel To 'This Is Spinal Tap' Is In The Works", "uoljbe"
    assert fp.get_post("uol6md") == "Do you ever get confused between Actors?", "uol6md"
    assert fp.get_post("uoky7x") == "Characters like Cpt. Willard/Rust Cohle?", "uoky7x"
    assert fp.get_post("uokh13") == "I cant find the name of this movie", "uokh13"
    assert fp.get_post("uokg73") == "World's largest film restoration project commences in India for Rs 363 crore", "uokg73"

def test_find_actor():
    assert fp.find_actor("Rob Reiner Confirms Sequel To 'This Is Spinal Tap' Is In The Works", fp.get_imdb_actor_names()) == int("0001661")
    assert fp.find_actor("Do you ever get confused between Actors?", fp.get_imdb_actor_names()) == None
    assert fp.find_actor("Characters like Cpt. Willard/Rust Cohle?", fp.get_imdb_actor_names()) == None
    assert fp.find_actor("I cant find the name of this movie", fp.get_imdb_actor_names()) == None
    assert fp.find_actor("World's largest film restoration project commences in India for Rs 363 crore", fp.get_imdb_actor_names()) == None

def test_Actor_class():
    rob_reiner = fp.Actor(int("0001661"))
    assert rob_reiner.name == "Rob Reiner"
    assert rob_reiner.age == 75
    assert rob_reiner.dob == "March 06, 1947"
    assert rob_reiner.pob == "The Bronx, New York City, New York, USA"
    assert rob_reiner.works == ["The Wolf of Wall Street (2013)", "All in the Family (1971)", "This Is Spinal Tap (1984)", "The Story of Us (1999)"]
    assert rob_reiner.awards == ["1978 Primetime Emmy for Outstanding Continuing Performance by a Supporting Actor in a Comedy Series", "1974 Primetime Emmy for Best Supporting Actor in Comedy"]

def test_create_comment():
    rob_reiner = fp.Actor(int("0001661"))
    assert fp.create_comment(rob_reiner, int("0001661")) == """**Actor's Name:** Rob Reiner
**Actor's Age:** 75
**Actor's Date of Birth:** March 06, 1947
**Actor's Place of Birth:** The Bronx, New York City, New York, USA
**Popular Works:**
            1. The Wolf of Wall Street (2013)
            2. All in the Family (1971)
            3. This Is Spinal Tap (1984)
            4. The Story of Us (1999)
**Some Awards Won:**
            1. 1978 Primetime Emmy for Outstanding Continuing Performance by a Supporting Actor in a Comedy Series
            2. 1974 Primetime Emmy for Best Supporting Actor in Comedy

This bot gives information about the first actor mentioned in a post title on r/movies, but sometimes mistakes are made.
Click [here](https://www.imdb.com/name/nm0001661/) to learn more about the actor found for this post!"""