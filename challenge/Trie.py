"""
In this class I have create a special Trie which is used to optimise searching
of title words in courses.
In this Trie at the end of the every word I have added another dictionary which
stores the course_ID and count of that word in that course. So, in short if any
word is given in the query we just have to traverse the Trie once to get the
occurrences and frequency of that word in any course.
This method greatly decreases the searching speed of title words. And it can also
one of the most optimised algorithm for searching.

"""


class Trie:
    def __init__(self):
        self.root = {}
        self.end = "__-end-__"

    def insert(self, word, idx):
        word = word.lower()
        curr = self.root
        for i in range(len(word)):
            character = word[i]
            if character in curr:
                curr = curr[character]
            else:
                curr[character] = {}
                curr = curr[character]
        if self.end not in curr:
            curr[self.end] = {idx: 1}
        else:
            if idx not in curr[self.end]:
                curr[self.end][idx] = 1
            else:
                curr[self.end][idx] += 1

    def delete(self, word, idx):
        word = word.lower()
        curr = self.root
        for i in range(len(word)):
            character = word[i]
            curr = curr[character]
        curr[self.end].pop(idx)

    def courses_containing_word(self, word):
        word = word.lower()
        curr = self.root
        for i in range(len(word)):
            character = word[i]
            if character in curr:
                curr = curr[character]
            else:
                return False
        if self.end in curr:
            return curr[self.end]
        else:
            return False