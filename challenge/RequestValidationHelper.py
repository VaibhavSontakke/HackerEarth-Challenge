import data

"""
In this class I have created validation and helper methods for separation
of concerns and re-usability. 
This class also has a corresponding test class in test directory for 
unit testing which covers almost all methods in the class.

"""


class RequestValidationHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_params(req, param):
        if param in req:
            return req[param]
        else:
            return False

    @staticmethod
    def title_validate(title_words):
        if len(title_words) > 0:
            return [x.strip() for x in title_words.split(",")]
        else:
            return []

    @staticmethod
    def validate_int(param):
        try:
            return int(param)
        except ValueError:
            return False

    @staticmethod
    def get_page_helper(courses, length_courses, page_size, page_number):
        last_idx = page_size * page_number
        first_idx = last_idx - page_size
        return courses[first_idx:last_idx]

    def validate_course_fields(self, course, creation):
        err_msg = ""
        status = True
        if course is None:
            return False, "Course Field information is not entered. Please enter"
        if "description" in course:
            if len(course["description"]) > 255:
                status = False
                err_msg += "Description is too long. It should not exceed more than 255 characters. "
        if "image_path" in course:
            if len(course["image_path"]) > 100:
                status = False
                err_msg += "Image Path is too long. It should not increase more than 100 characters. "
        if "title" in course:
            if len(course["title"]) < 5 or len(course["title"]) > 100:
                status = False
                err_msg += "Title is not of appropriate size. It should between 5 to 100 characters. "
        if "price" in course:
            try:
                float(course["price"])
            except ValueError:
                status = False
                err_msg += "Price should be a decimal value. "
        if "on_discount" in course:
            if type(course["on_discount"]) is not bool:
                status = False
                err_msg += "On Discount should be a Boolean value. "
        if creation:
            status, err_msg = self.validate_course_fields_creation(course, status, err_msg)
        if status is True:
            return status, course
        return status, err_msg

    @staticmethod
    def validate_course_fields_creation(course, status, err_msg):
        if "on_discount" not in course:
            status = False
            err_msg += "On discount is field is not available. It is required for course creation ."
        if "price" not in course:
            status = False
            err_msg += "Price is field is not available. It is required for course creation. "
        if "title" not in course:
            status = False
            err_msg += "Title is field is not available. It is required for course creation. "

        return status, err_msg

    @staticmethod
    def trie_delete(idx):
        title = data.courses[idx]["title"]
        tokens_title = set(title.split(" "))
        for token in tokens_title:
            data.trie.delete(token, idx)

    @staticmethod
    def trie_insert(curr_course, idx):
        title = curr_course["title"]
        tokens_title = set(title.split(" "))
        for token in tokens_title:
            data.trie.insert(token, idx)
