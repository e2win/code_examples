class Book:
    def __init__(self, i, t, p):
        self.id = i
        self.title = t
        self.price = p

    def __str__(self):
        return self.title
