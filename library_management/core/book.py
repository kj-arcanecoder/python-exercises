class Book:
    def __init__(self, book_id, title, author, available):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available = available
        
    def to_dict(self):
        """ convert book object to dictionary (for saving to file)
        """
        return {self.book_id:{
            "title": self.title,
            "author": self.author,
            "available": self.available
            }}

    def __str__(self):
        """ readable representation of book info
        """
        return f"{self.book_id:10} {self.title:35} {self.author:25} {str(self.available):5}"
