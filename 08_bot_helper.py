from AddrBook import *
import pickle
from abc import ABC, abstractmethod
import pandas as pd

df = pd.DataFrame({'col_1': [1, 2, 3], 'col_2': [4, 5, 6], 'col_3': [7, 8, 9]})
# print(df) just to test external package in docker
list_of_commands = [
    "add [name] [phone]: Add a new contact.",
    "change [name] [old_phone] [new_phone]: Change phone number of a contact.",
    "phone [name]: Show phone number(s) of a contact.",
    "all: Show all contacts.",
    "add-birthday [name] [birthday]: Add birthday for a contact.",
    "show-birthday [name]: Show birthday of a contact.",
    "birthdays: Show upcoming birthdays.",
    "help: Show available commands.",
    "df: will print df examples.",
    "close/exit: Close the program."]


class UserInterface(ABC):

    @abstractmethod
    def welcome_invite(self, address_book: AddressBook):
        pass

    @abstractmethod
    def show_contacts(self, contact: Record):
        pass

    @abstractmethod
    def show_commands(self, commands: list):
        pass

    @abstractmethod
    def show_greetings_lis(self, congrats_list: list):
        pass

    @abstractmethod
    def show_birthday(self, record: Record):
        pass

    @abstractmethod
    def goodbye_note(self, address_book: AddressBook):
        pass


class ConsoleUserInterface(UserInterface):

    def welcome_invite(self, address_book: AddressBook):
        print(f"Welcome to the assistant bot! \
AddressBook contains {len(address_book)} contact(s).\n \
Hello how can I help you?\n \
Type 'help' for a list of available commands.")

    def show_contacts(self, contact: list):
        if isinstance(contact, Record):
            print("Contacts:")
            print(f"{contact.name}: {contact}")
        else:
            print("Contacts:")
            for i in contact:
                print(f"{i[0]}: {i[1]}")

    def show_commands(self, commands: list):
        print("Available commands:")
        for i in commands:
            print(f"{i}")

    def show_greetings_lis(self, congrats_list: list):
        if len(congrats_list) == 0:
            print("There are no congratulations.")
        else:
            print(f"Congratulations! \
            We have {len(congrats_list)} birthday(s): \
            {congrats_list}")

    def show_birthday(self, record: Record):
        print(f"Birthday of {record.name}: {record.birthday.strftime('%Y.%m.%d')}")

    def goodbye_note(self, address_book: AddressBook):
        print(f"You are going to exit, {len(address_book)} have been saved in the book. \nGood bye!")


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "+rb") as f:
            restored_bk = pickle.load(f)
            return restored_bk
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Command not Found."
        except KeyError:
            return "Name not Found."
        except NameError:
            return "Name not Found."
        except Exception as e:
            return f"Error: {e}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(*args):
    if args[0] in book:
        record = book.find(args[0])
        record.add_phone(args[1])
    else:
        record = Record(args[0])
        record.add_phone(args[1])
        book.add_record(record)
    return record


@input_error
def change_contact(command, *args):
    record = book.find(args[0])
    record.edit_phone(args[1], args[2])
    return record


@input_error
def show_phone(*args):
    record = book.find(args[0])
    return record


@input_error
def show_all():
    return book


@input_error
def show_birthday(*args):
    record = book.find(args[0])
    return record


@input_error
def add_birthday(*args):
    record = book.find(args[0])
    record.add_birthday(args[1])
    return record


book = load_data()


def main():
    ui = ConsoleUserInterface()
    ui.welcome_invite(book)
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            save_data(book)
            ui.goodbye_note(book)
            break
        elif command in ["hello"]:
            ui.welcome_invite(book)
        elif command in ["add"]:
            new_contact = add_contact(*args)
            ui.show_contacts(new_contact)

        elif command in ["change"]:
            changed_contact = change_contact(command, *args)
            ui.show_contacts(changed_contact)

        elif command in ["phone"]:
            phones = show_phone(*args)
            ui.show_contacts(phones)

        elif command in ["all"]:
            all_records = [i for i in book.items()]
            ui.show_contacts(all_records)

        elif command == "add-birthday":
            contact = add_birthday(*args)
            ui.show_contacts(contact)

        elif command == "show-birthday":
            b_day = show_birthday(*args)
            ui.show_birthday(b_day)

        elif command == "birthdays":
            congrats_list = book.get_birthdays(7)
            ui.show_greetings_lis(congrats_list)

        elif command == "help":
            ui.show_commands(list_of_commands)

        elif command == "df":
            print(df)

        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
