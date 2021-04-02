"""Routes for the course resource.
"""

from run import app
from flask import request, jsonify
from collections import Counter
import data
from datetime import datetime
from RequestValidationHelper import RequestValidationHelper


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object

    Solution:
    Here I solved the problem in O(1) time complexity by just editing
    the given data array and making a data dictionary which is callable
    by id.
    """

    if id in data.courses:
        return jsonify(data.courses[id]), 200
    else:
        course_not_found = {
            "messge": "Course {} does no exist".format(id)
        }
        return jsonify(course_not_found), 404
        # return app.response_class(response=json.dumps(course_not_found),
        #                               status=404,
        #                                   mimetype='application/json')


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
       
    --------
    Solution: 
    I solved this problem using a slightly modified Trie data 
    structure which vastly reduced the time-complexity required for searching 
    words in titles. Searching time here is O(log(H)), where H is height of 
    longest word in title and log is of base 26. This is very fast and 
    independent of number of records are stored in the Trie.
    Here I have created a class Trie which uses basic dictionary but at the 
    end of the word I have added another dictionary which stores the course_ID
    and count of the word in that course. So, in short if any word is given 
    in the query we just have to traverse the Trie once to get the occurrences
    and frequency of that word in any course_id.
    Implementing Trie also increased the time-complexity of course-creation,
    deletion and updation operations from O(1) to O(log(H)). But display operations 
    are greatly optimized. As creation, updation and deletion of courses is not 
    as frequent as display of courses, we chose to comprise just a lil bit 
    performance on those for a vast performance increase in display APIs
    
    Also all bonus points have been collected in this API. I have also added 
    performance metric as a header in all the API responses. I will 
    attach screen shot of that in screenshots folder.
     
    """
    rv = RequestValidationHelper()
    req = request.args
    page_number = rv.get_params(req, "page-number")
    page_size = rv.get_params(req, "page-size")
    title_words = rv.get_params(req, "title-words") or ""
    page_number = rv.validate_int(page_number) or 1  # takes defaults if invalid values are given
    page_size = rv.validate_int(page_size) or 10
    # print(page_size, page_number, title_words, type(title_words))
    title_words = rv.title_validate(title_words)
    usages = Counter()  # Used counter to sum up all the frequencies of words in different courses
    if len(title_words) > 0:
        for title in title_words:
            curr_usage = Counter(data.trie.courses_containing_word(title.lower()))
            usages += curr_usage
        sorted_usages = usages.most_common()
        # print(sorted_usages)
        sorted_usages_id = list(map(lambda m: data.courses[m[0]], sorted_usages))
        courses = rv.get_page_helper(sorted_usages_id, len(sorted_usages_id), page_size, page_number)
    else:
        # print(data.courses)
        # sorted_courses_id = list(map(lambda m: m[1], list(sorted(data.courses.items(), key=lambda x: x[0]))))
        sorted_courses_id = list(map(lambda m: m[1], list(data.courses.items())))  # No need to sort the courses here
        # print(sorted_courses_id)
        length_courses = data.number_of_courses
        courses = rv.get_page_helper(sorted_courses_id, length_courses, page_size, page_number)
    return jsonify(courses), 200


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object

    Solution:
    Here I had reduced the update time by using dictionary but after using Trie
    the time-complexity increased to O(wlog(H)), where H is height of
    longest word in title, w is number of words in title and log is of base 26,
    this time-complexity increase is because I had add new words in the Trie.

    """
    rv = RequestValidationHelper()
    current_course = request.json
    status, current_course = rv.validate_course_fields(current_course, True)
    if status is False:
        return jsonify({"messg": current_course}), 400
    else:
        date = str(datetime.now()).split(".")[0].strip()
        # print(date)
        data.number_of_courses += 1
        current_course_id = data.number_of_courses
        current_course['id'] = current_course_id
        current_course["date_created"] = date
        current_course["date_updated"] = date
        rv.trie_insert(current_course, current_course_id)
        data.courses[current_course_id] = current_course
        return jsonify(current_course), 201


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object

    Solution:
    Here I had reduced the update time by using dictionary but after using Trie
    the time-complexity increased to O(wlog(H)), where H is height of
    longest word in title, w is number of words in title and log is of base 26,
    this time-complexity increase is because I had to delete and add new
    words in the Trie.

    """

    course_to_be_updated = request.json
    if id in data.courses:
        if "id" not in course_to_be_updated or id == course_to_be_updated['id']:
            rv = RequestValidationHelper()
            status, course_to_be_updated = rv.validate_course_fields(course_to_be_updated, False)
            if status is False:
                return jsonify({"messg": course_to_be_updated}), 400
            else:
                date = str(datetime.now()).split(".")[0].strip()
                course_to_be_updated["date_updated"] = date
                for field in course_to_be_updated:
                    if field == "title":
                        rv.trie_delete(id)
                        rv.trie_insert(course_to_be_updated, id)
                    data.courses[id][field] = course_to_be_updated[field]
                return jsonify(course_to_be_updated), 200
        else:
            id_mismatch_error = {
                "message": "The id does match the payload"
            }
            return jsonify(id_mismatch_error), 400
    else:
        course_not_found = {
            "messge": "Course {} does no exist".format(id)
        }
        return jsonify(course_not_found), 404


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    
    Solution:
    Here I had reduced the update time by using dictionary but after using Trie 
    the time-complexity increased to O(wlog(H)), where H is height of 
    longest word in title, w is number of words in title and log is of base 26, 
    this time-complexity increase is because I had to delete words from the Trie.
    
    """
    if id in data.courses:
        rv = RequestValidationHelper()
        rv.trie_delete(id)
        del data.courses[id]
    else:
        course_not_found = {
            "messge": "Course {} does no exist".format(id)
        }
        return jsonify(course_not_found), 404

        # YOUR CODE HERE
