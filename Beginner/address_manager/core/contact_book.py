from collections import defaultdict
import logging
import time
from . import utils as address_utils
from . import contact
from email_validator import validate_email, EmailNotValidError
import phonenumbers

logger = logging.getLogger(__name__)

class ContactBook:
    
    def __init__(self):
        """To initialize, fetching all the contacts from file and stores it in a dictionary list 
        """
        logger.info("Initializing the full contacts list.")
        self.contacts = defaultdict(list)
        self.get_all_contacts()
        
    
    def get_all_contacts(self):
        """Fetches all the contacts from file and stores it in a dictionary list 
        """
        all_contacts = address_utils.get_all_contacts()
        for name, details in sorted(all_contacts.items()):
            self.contacts[name] = contact.Contact(name, details['phone'], details['email'], 
                                                  details['address'])
    
    def add_contact(self):
        """Initiates the add contact operation
        """
        logger.info("In add contact section.")
        while True:
            address_utils.clear_cli()
            address_utils.print_header("Add Contact")
            try:
                name, phone, email, address = self.input_and_validate_details()
                self.save_new_contact(name, phone, email, address)
            except ValueError as e:
                address_utils.print_and_log_warn_message(f"{e}")
            finally:
                is_continue = input("\nDo you want to continue (y/n): ")
                if is_continue == 'n':
                    break
                elif is_continue == 'y':
                    continue
                else:
                    print("\nInvalid input, returning to main menu.")
                    time.sleep(1)

    def input_and_validate_details(self):
        """Validates all the inputs from user for the add contact operation

        Raises:
            ValueError: When the contact name is already present

        Returns:
            str: Fields name,phone,email,address inputed by user if successfully validated
        """
        name = input("\nEnter name of the contact: ").title()
        if name in self.contacts.keys():
            raise ValueError("Name already exists in the address book.")
        phone = input("Enter phone number: ")
        self.validate_phone(phone)
        email = input("Enter email: ")
        self.validate_email_address(email)
        address = input("Enter address: ")
        logger.info("All contact details validated.")
        return name,phone,email,address

    def save_new_contact(self, name, phone, email, address):
        """Saves the new contact during the add contact operation

        Args:
            name (str): name of the contact
            phone (str): phone number
            email (str): email address
            address (str): contact's address
        """
        print("\nSaving contact information.")
        new_contact = contact.Contact(name, phone, email, address)
        self.contacts[name] = new_contact
        address_utils.save_contact(new_contact.to_dict())
        time.sleep(2)
        address_utils.print_and_log_info_message(f"\nDetails of {name} added successfully.")
    
    def validate_phone(self, phone):
        """Validates the user phone number

        Args:
            phone (str): phone number

        Raises:
            ValueError: if phone number is invalid
            ValueError: if phone number format is invalid
        """
        try:
            parsed = phonenumbers.parse(phone, "IN")
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format.")
        
    def validate_email_address(self, email):
        """Validates the user email address

        Args:
            email (str): the email address

        Raises:
            ValueError: if the email is invalid

        Returns:
            str: valid status of email
        """
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError("Email is invalid.")
                
    def view_all_contacts(self):
        """Displays all the contacts
        """
        logger.info("In view all contacts section.")
        address_utils.clear_cli()
        address_utils.print_header("All Contacts List")
        self.display_contact_header()
        for contact_detail in self.contacts.values():
            self.display_contact(contact_detail)
        input("\n\nPress Enter to continue.")

    def display_contact_header(self):
        """Displays the header to show the contact info
        """
        print(f"\n{'Name':<20} {'Phone':<15} {'Email':<30} {'Address':<30}")

    def display_contact(self, contact_detail):
        """Displays the contact details

        Args:
            contact_detail (Contact): Contact object containing the contact information
        """
        print(f"{contact_detail.name:<20} {contact_detail.phone:<15} {contact_detail.email:<30} " 
              f"{contact_detail.address:<30}")
    
    def search_contacts(self):
        """Searches the contact based on various attributes

        Raises:
            ValueError: If the attribute requested for search is invalid
        """
        logger.info("In search contacts section.")
        while True:
            address_utils.clear_cli()
            address_utils.print_header("Search Contact")
            try:
                found_result = False
                attribute_to_search = input("\nEnter the name of the attribute you want " 
                                            "to search (name, phone, email or address): ").lower()
                if not attribute_to_search in ("name","phone","email","address"):
                    raise ValueError("Invalid attribute requested for search")
                text_to_search = input("Enter the text to search: ").lower()
                self.search_text_in_attribute(found_result, attribute_to_search, text_to_search)   
            except ValueError as e:
                address_utils.print_and_log_warn_message(e)
            finally:
                is_continue = input("\nDo you want to continue (y/n): ")
                if is_continue == 'n':
                    break
                elif is_continue == 'y':
                    continue
                else:
                    print("\nInvalid input, returning to main menu.")
                    time.sleep(1)

    def search_text_in_attribute(self, found_result, attribute_to_search, text_to_search):
        """Searches for text in requested attribute in search contacts section

        Args:
            found_result (boolean): if text matches with any contact info
            attribute_to_search (str): attribute on which search needs to be performed
            text_to_search (_type_): the text which needs to be searched on the attribute

        Raises:
            ValueError: If no results are found
        """
        print("\nSearching...")
        time.sleep(2)
        if attribute_to_search == "name":
            for name in self.contacts.keys():
                if text_to_search in name.lower():
                    if not found_result:
                        found_result = True
                        self.display_contact_header()
                    self.display_contact(self.contacts[name])
        else:
            for details in self.contacts.values():
                if ((attribute_to_search == "phone" and text_to_search in details.phone)
                            or (attribute_to_search == "email" and text_to_search in details.email.lower())
                            or (attribute_to_search == "address" and text_to_search in details.address.lower())):
                    if not found_result:
                        found_result = True
                        self.display_contact_header()
                    self.display_contact(details) 
        if not found_result:
            time.sleep(2)
            raise ValueError("\nNo results found.")

    def edit_contact(self):
        """Edit's any of the attribute of a contact
        """
        logger.info("In edit contact section.")
        while True:
            found_result = False
            address_utils.clear_cli()
            address_utils.print_header("Edit Contact")
            try:
                name_to_edit = input("\nEnter the name of the contact that you want to edit:").title()
                self.search_contact_to_edit(name_to_edit, found_result)
            except ValueError as e:
                address_utils.print_and_log_warn_message(e)
            finally:
                is_continue = input("\nDo you want to continue (y/n): ")
                if is_continue == 'n':
                    break
                elif is_continue == 'y':
                    continue
                else:
                    print("\nInvalid input, returning to main menu.")
                    time.sleep(1)

    def search_contact_to_edit(self, name_to_edit, found_result):
        """Searches for the contact and if found then updates the requested attribute

        Args:
            name_to_edit (str): name of contact that should be edited

        Raises:
            ValueError: attribute requested is invalid
            ValueError: name of contact not found
        """
        print("\nSearching...")
        time.sleep(1)
        for contact in self.contacts.keys():
            if name_to_edit == contact:
                contact_to_edit = self.contacts[contact]
                found_result = True
                time.sleep(2)
                self.display_contact_header()
                self.display_contact(contact_to_edit)
                attribute_to_edit = input("\nEnter the name of the attribute you want " 
                                            "to edit (phone, email or address): ").lower()
                match attribute_to_edit:
                    case "phone":
                        self.edit_phone(contact_to_edit)
                    case "email":
                        self.edit_email(contact_to_edit)
                    case "address":
                        self.edit_address(contact_to_edit)
                    case _:
                        raise ValueError("Invalid attribute requested for search")
                print(f"\nContact {name_to_edit.title()} edited")
                break
        if not found_result:
            time.sleep(2)
            raise ValueError("Contact not found by this name.")

    def edit_address(self, contact_to_edit):
        """modifies the address attribute

        Args:
            contact_to_edit (Contact): Contact object containing the contact's information
        """
        new_address = input("\nEnter the new address: ")
        print("Updating address.")
        contact_to_edit.address = new_address
        address_utils.save_contact(contact_to_edit.to_dict())
        time.sleep(2)

    def edit_email(self, contact_to_edit):
        """Modifies the email attribute

        Args:
            contact_to_edit (Contact): Contact object containing the contact's information
        """
        new_email = input("\nEnter the new email: ")
        print("Updating email.")
        self.validate_email_address(new_email)
        contact_to_edit.email = new_email
        address_utils.save_contact(contact_to_edit.to_dict())
        time.sleep(2)

    def edit_phone(self, contact_to_edit):
        """Modifies the phone number attribute

        Args:
            contact_to_edit (Contact): Contact object containing the contact's information
        """
        new_phone = input("\nEnter the new phone number: ")
        print("Updating phone number.")
        self.validate_phone(new_phone)
        contact_to_edit.phone = new_phone
        address_utils.save_contact(contact_to_edit.to_dict())
        time.sleep(2)
    
    def delete_contact(self):
        """Deletes the requested contact name
        """
        logger.info("In delete contact section")
        while True:
            found_result = False
            address_utils.clear_cli()
            address_utils.print_header("Delete Contact")
            try:
                name_to_delete = input("\nEnter the name of the contact that you want to delete: ").title()
                self.search_contact_to_delete(name_to_delete, found_result)
            except ValueError as e:
                address_utils.print_and_log_warn_message(e)
            finally:
                is_continue = input("\nDo you want to continue (y/n): ")
                if is_continue == 'n':
                    break
                elif is_continue == 'y':
                    continue
                else:
                    print("\nInvalid input, returning to main menu.")
                    time.sleep(1)

    def search_contact_to_delete(self, name_to_delete, found_result):
        """Searches for the contact name to be deleted and then deletes it.

        Args:
            name_to_delete (_type_): _description_

        Raises:
            ValueError: _description_
        """
        print("\nSearching...")
        time.sleep(1)
        for contact in self.contacts.keys():
            if name_to_delete == contact:
                found_result = True
                print("Found contact, deleting...")
                time.sleep(2)
                address_utils.delete_contact(name_to_delete.title())
                del self.contacts[contact]
                print(f"\nContact {name_to_delete.title()} deleted")
                break
        if not found_result:
            time.sleep(2)
            raise ValueError("Contact not found by this name.")
        
    def export_to_csv(self):
        logger.info("In export to csv section")
        address_utils.clear_cli()
        address_utils.print_header("Export to CSV")
        try:
            if self.contacts:
                print("Exporting all contacts to CSV file...")
                time.sleep(1)
                full_contacts_dict = self.get_full_contacts_dict()
                address_utils.export_to_csv(full_contacts_dict)
            else:
                raise ValueError("No contacts to export")
        except ValueError as e:
            print(e)
        finally:
            print("\nReturning to main menu.")
            time.sleep(2)
        
    def get_full_contacts_dict(self):
        full_contacts_dict = defaultdict(list)
        for name, details in self.contacts.items():
            full_contacts_dict[name] = {"phone" : details.phone,
                                        "email" : details.email,
                                        "address" : details.address}
        return full_contacts_dict