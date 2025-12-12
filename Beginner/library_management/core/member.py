class Member:
    def __init__(self, member_id, member_name, borrowed_books):
        self.member_id = member_id
        self.member_name = member_name
        self.borrowed_books = borrowed_books
        
    def borrow_book(self, book_id):
        self.borrowed_books.append(book_id)
    
    def return_book(self, book_id):
        self.borrowed_books.remove(book_id)

    def to_dict(self):
        """ convert member object to dictionary (for saving to file)

        Returns:
            _type_: Dictionary
        """
        return {self.member_id: {
            "member_name": self.member_name,
            "borrowed_books": self.borrowed_books
            }}
    
    def __str__(self):
        """ readable representation of member info
        """
        borrowed = ', '.join(self.borrowed_books) if self.borrowed_books else "None"
        return f"{self.member_id:10} {self.member_name:20} {borrowed:30}"