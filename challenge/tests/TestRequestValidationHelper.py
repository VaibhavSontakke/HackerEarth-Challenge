from RequestValidationHelper import RequestValidationHelper
import json
import unittest


class TestRequestValidationHelper(unittest.TestCase):
    def test_get_params(self):
        rv = RequestValidationHelper()
        with open("TestRequestValidationHelper.json") as fp:
            data = json.load(fp)

        self.assertTrue(rv.get_params(data[0], "page-number") == data[0]["page-number"])
        self.assertTrue(rv.get_params(data[0], "page-size") == data[0]["page-size"])
        self.assertTrue(rv.get_params(data[0], "title-words") == data[0]["title-words"])

    def test_title_validate(self):
        rv = RequestValidationHelper()
        with open("TestRequestValidationHelper.json") as fp:
            data = json.load(fp)

        self.assertTrue(rv.title_validate(data[0]["title-words"]) == ["ABC", "XYZ"])
        self.assertTrue(rv.title_validate("") == [])

    def test_validate_int(self):
        rv = RequestValidationHelper()
        self.assertTrue(rv.validate_int("9") == 9)
        self.assertTrue(rv.validate_int("") is False)

    def test_get_page_helper(self):
        rv = RequestValidationHelper()
        with open("../json/course.json") as fp:
            data = json.load(fp)

        self.assertTrue(rv.title_validate(data[0]["title-words"]) == ["ABC", "XYZ"])
        self.assertTrue(rv.title_validate("") == [])


if __name__ == '__main__':
    unittest.main()
