"""Routines associated with the application data.
"""
import json
from Trie import Trie

courses = {}
number_of_courses = 200
trie = Trie()


def load_data(json_path):
    """Load the data from the json file.''
	"""
    global number_of_courses
    with open(json_path) as f:
        data = json.load(f)
    # print("data",data)
    # courses = {course['id']: course for course in data}
    for course in data:
        courses[course["id"]] = course
        insert_title_trie(course["title"], course["id"])
    number_of_courses = len(courses)
    return True


def insert_title_trie(title, id):
    tokens = title.split(" ")
    for word in tokens:
        trie.insert(word, id)
