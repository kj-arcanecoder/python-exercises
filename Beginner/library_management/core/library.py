from collections import defaultdict
import logging
import os
import time
import traceback
from . import utils as lib_utils
from . import book as book_obj
from . import member as member_obj

logger = logging.getLogger(__name__)

class Library:
    def __init__(self):
        """ Initializing the Library class to fetch books and members
        """
        logger.info("Initializing library class")
        self.fetch_books_from_file()
        self.fetch_members_from_file()
        logger.info("Fetched books and members")

    def fetch_books_from_file(self):
        """ Fetching books from the json file
        """
        logger.info("Fetching all books from books.json")
        self.books = defaultdict(list)
        raw_books_data = lib_utils.get_all_books()
        for id,details in raw_books_data.items():
            self.books[id] = book_obj.Book(id,details['title'],details['author'],details['available'])
        count = len(self.books)
        if count > 0:
            logger.info(f"{count} books fetched from books.json")
    
    def fetch_members_from_file(self):
        """ Fetching members from the json file
        """
        logger.info("Fetching all members from members.json")
        self.members = defaultdict(list)
        raw_members_data = lib_utils.get_all_members()
        for id,details in raw_members_data.items():
            self.members[id] = member_obj.Member(id,details['member_name'],details['borrowed_books'])
        count = len(self.members)
        if count > 0:
            logger.info(f"{count} members fetched from members.json")
    
    def add_book(self):
        """ Add one or more books and save to file
        """
        add_another = True
        add_another_choice = ""
        while add_another:
            os.system("cls")
            try:
                title = input("Enter title of the book: ")
                titles = [book.title.lower() for book in self.books.values()]
                if title.lower() not in titles:
                    self.save_book(title)
                    add_another_choice = input("\nDo you want to continue (y/n): ")
                else:
                    raise ValueError("Book with this title already exists.")
            except ValueError as e:
                lib_utils.print_and_log_warn_message(e)
                add_another_choice = input("\nDo you want to try again (y/n): ")
            finally:
                match add_another_choice.lower():
                    case 'y':
                        continue
                    case 'n':
                        add_another = False
                    case _:
                        print("\nInvalid choice, returning to main menu.")
                        time.sleep(1)
                        break

    def save_book(self, title):
        author = input("Enter the author of the book: ")
        book_id = max(map(int, self.books.keys())) + 1
        lib_utils.print_and_log_info_message(f"Saving new book {book_id}")
        new_book = book_obj.Book(book_id, title, author, True).to_dict()
        lib_utils.save_book(new_book)
        time.sleep(1)
        lib_utils.print_and_log_info_message(f"Book {book_id} added to library successfully.")
                        
    def add_member(self):
        """ Add one or more members and save to file
        """
        add_another = True
        add_another_choice = "n"
        while add_another:
                os.system("cls")
                try:
                    member_name = input("Enter name of the member: ")
                    names = [member.member_name.lower() for member in self.members.values()]
                    if member_name.lower() not in names:
                        self.save_member(member_name)
                        add_another_choice = input("\nDo you want to continue (y/n): ")
                    else:
                        raise ValueError("Member already exists.")
                except ValueError as e:
                    lib_utils.print_and_log_warn_message(e)
                    add_another_choice = input("\nDo you want to try again (y/n): ")
                finally:
                    match add_another_choice.lower():
                        case 'y':
                            continue
                        case 'n':
                            add_another = False
                        case _:
                            print("\nInvalid choice, returning to main menu.")
                            time.sleep(1)
                            break

    def save_member(self, member_name):
        lib_utils.print_and_log_info_message(f"Saving new member, generating member ID.")
        member_id = max(map(int, self.members.keys())) + 1
        new_member = member_obj.Member(member_id, member_name, list()).to_dict()
        lib_utils.save_member(new_member)
        self.members[member_id] = {'member_name':member_name, 'borrowed_books':list()}
        time.sleep(1)
        lib_utils.print_and_log_info_message(f"Member {member_id} saved successfully.")
            
    def borrow_book(self):
        """ Issue book to member if member ID and book name matches.

        Raises:
            ValueError: If book name does not exist
            ValueError: If member name does not exist
        """
        borrow_another = True
        borrow_another_choice = "n"
        error = False
        while borrow_another:
            os.system("cls")
            try:
                member_id = input("Enter member ID: ")
                members = [member for member in self.members.values() if member.member_id == member_id]
                if members:
                    member = members[0]
                    req_book_name = input("Enter the book name to be borrowed: ").lower()
                    books = [book for book in self.books.values() if book.title.lower() == req_book_name]
                    if books:
                        book = books[0]
                        if book.available:
                            self.checkout_book_for_member(member_id, member, book)
                            lib_utils.save_transaction(member_id, req_book_name, "Borrowed")
                            time.sleep(1)
                            lib_utils.print_and_log_info_message(f"Book {book.book_id} checked out successfully.")
                        else:
                            lib_utils.print_and_log_info_message(f"{book.title} is unavailable as it has been checked out.")
                    else:
                        raise ValueError("Book with this name does not exist.")
                else:
                    raise ValueError("Member with this ID does not exist.")
            except ValueError as e:
                lib_utils.print_and_log_warn_message(e)
                error = True
            except TypeError as e:
                lib_utils.print_and_log_error_message(f"\nType Error: {traceback.print_exc()}")
                error = True
            finally:
                if error:
                    borrow_another_choice = input("\nDo you want to try again (y/n): ")
                else:
                    borrow_another_choice = input("\nDo you want to checkout another book (y/n): ")
                match borrow_another_choice.lower():
                    case 'y':
                        continue
                    case 'n':
                        borrow_another = False
                    case _:
                            print("\nInvalid choice, returning to main menu.")
                            time.sleep(1)
                            break

    def checkout_book_for_member(self, member_id, member, book):
        lib_utils.print_and_log_info_message(f"Member {member_id} & book {book.book_id} match, checking out.")
        book.available = False
        member.borrow_book(book.book_id)
        lib_utils.save_book(book.to_dict())
        lib_utils.save_member(member.to_dict())   
            
    def return_book(self):
        return_another = True
        return_another_choice = "n"
        error = False
        while return_another:
            os.system("cls")
            try:
                member_id = input("Enter member ID: ")
                members = [member for member in self.members.values() if member.member_id == member_id]
                if members:
                    member = members[0]
                    return_book_name = input("Enter the book name to be returned: ").lower()
                    books = [book for book in self.books.values() if book.title.lower() == return_book_name]
                    if books:
                        book = books[0]
                        self.check_return_book_condition(member_id, member, return_book_name, book)
                    else:
                        raise ValueError("Book with this name does not exist.")
                else:
                    raise ValueError("Member with this ID does not exist.")
            except ValueError as e:
                lib_utils.print_and_log_warn_message(e)
                error = True
            except TypeError as e:
                lib_utils.print_and_log_error_message(f"\nType Error: {traceback.print_exc()}")
                error = True
            finally:
                if error:
                    return_another_choice = input("\nDo you want to try again (y/n): ")
                else:
                    return_another_choice = input("\nDo you want to return another book (y/n): ")
                match return_another_choice.lower():
                    case 'y':
                        continue
                    case 'n':
                        return_another = False
                    case _:
                            print("\nInvalid choice, returning to main menu.")
                            time.sleep(1)
                            break

    def check_return_book_condition(self, member_id, member, return_book_name, book):
        if not book.available:
            if book.book_id in member.borrowed_books:
                self.return_book_for_member(member_id, member, book)
                lib_utils.save_transaction(member_id, return_book_name, "Returned")
                time.sleep(1)
                lib_utils.print_and_log_info_message(f"Book {book.book_id} returned successfully.")
            else:
                lib_utils.print_and_log_warn_message(f"Book {book.book_id} was not checked out by {member_id}, can't be returned.")
        else:
            lib_utils.print_and_log_info_message(f"{book.title} has already been returned.")

    def return_book_for_member(self, member_id, member, book):
        lib_utils.print_and_log_info_message(f"Member {member_id} & book {book.book_id} match, returning to library.")
        book.available = True
        member.return_book(book.book_id)
        lib_utils.save_book(book.to_dict())
        lib_utils.save_member(member.to_dict()) 

    def show_books(self):
        """ To display all books
        """
        os.system('cls')
        count = 0
        print(f"{'Book Id':10} {'Name':35} {'Author':25} {'Available':5}")
        for details in self.books.values():
            print(str(details))
            count+=1
        if count > 0:
            lib_utils.print_and_log_info_message(f"\n{count} books fetched.")
            input("\nPress Enter to continue.")
            
    def view_members(self):
        """ To display all members
        """
        os.system('cls')
        count = 0
        print(f"{'Member Id':10} {'Name':20} {'Books borrowed':30}")
        for details in self.members.values():
            print(str(details))
            count+=1
        if count > 0:
            lib_utils.print_and_log_info_message(f"\n{count} members fetched.")
            input("\nPress Enter to continue.")
            
