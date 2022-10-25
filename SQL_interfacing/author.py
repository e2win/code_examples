class Author:
    def __init__(self, author_id, fn, ln):
        self.id = author_id
        self.first_name = fn
        self.last_name = ln

    def __str__(self):
        return self.first_name + " " + self.last_name