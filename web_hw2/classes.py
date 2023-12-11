import re
import pickle
import os
from genericpath import exists
from collections import UserDict
from datetime import date, datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def self_name(self, name):
        self.__privat_name = None
        self.name = name
        return str(self.name)

    @property
    def name(self):
        return self.__privat_name

    @name.setter
    def name(self, name: str):
        if name.isalpha():
            self.__privat_name = name
        else:
            raise Exception("Wrong name")


class Location(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) != 10 or not new_value.isdigit():
            raise ValueError("Invalid phone number, should contain 10 digits")
        else:
            self.__value = new_value

    def __str__(self):
        return f"Phone: {self.value}"


class Mail(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        patern_mail = r"[A-z.]+\w+@[A-z]+\.[A-z]{2,}"
        try:
            if bool(re.match(patern_mail, value)):
                self.__value = value
            else:
                raise ValueError(
                    "Mail should have the following format nickname@domen.yy"
                )
        except ValueError as e:
            raise ValueError(
                "Mail should have the following format nickname@domen.yy"
            ) from e

    # def __str__(self):
    #     return f"Mail: {self.__value}"
    def __str__(self) -> str:
        return f"Mail: {self.__value}"


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            chek_data = datetime.strptime(new_value, "%Y-%m-%d")
            if chek_data:
                self.__value = new_value
        except:
            raise ValueError("Invalid data format")


class Record:
    def __init__(self, name, phone=None, mail=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        # print(self.phones)
        self.mails = [Mail(mail)] if mail else []
        # print(self.mails)

    def add_phone(self, phone):
        new_phone = "".join(filter(str.isdigit, phone))
        # if len(new_phone) != 10:
        #     print(f"Invalid phone length: {new_phone}")
        # try:
        self.phones.append(Phone(new_phone))
        # except:
        #  raise ValueError("Not enough number setter")

    def add_location(self, location):
        self.location = Location(location)

    def add_mail(self, value):
        self.mails.append(Mail(value))

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError(f"The phone {old_phone} is not found.")
            # return f"The phone {old_phone} is not found."

    def edit_mail(self, old_mail, new_mail):
        found = False
        for mail in self.mails:
            if mail.value == old_mail:
                mail.value = new_mail
                found = True
        if not found:
            raise ValueError(f"The mail {old_mail} is not found.")
            # return f"The phone {old_phone} is not found."

    def find_phone(self, phone: str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def remove_phone(self, phone):
        del_phone = None
        for ph in self.phones:
            if ph.value == phone:
                del_phone = ph
        self.phones.remove(del_phone)

    def add_birthday(self, birthday=None):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        today = date.today()
        d_bd = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        if d_bd.month - today.month < 0:
            next_bd = date(2024, d_bd.month, d_bd.day)
            delta_days = next_bd - today
            return delta_days.days
        else:
            if d_bd.day - today.day < 0:
                next_bd = date(2024, d_bd.month, d_bd.day)
                delta_days = next_bd - today
                return delta_days.days
            else:
                next_bd = date(2023, d_bd.month, d_bd.day)
                delta_days = next_bd - today
                if delta_days.days == 0:
                    return "today"
                else:
                    return delta_days.days

    def __str__(self):
        # try:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}, mails: {'; '.join(p.value for p in self.mails)}"
        # except:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}"
        # except:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

        return_res = f"Contact name: {self.name.value}"

        if hasattr(self, "phones") and self.phones:
            return_res += f", phones: {'; '.join(p.value for p in self.phones)}"

        if hasattr(self, "birthday") and self.birthday:
            return_res += f", birthday: {self.birthday}"

        if hasattr(self, "mails") and self.mails:
            return_res += f", mail: {'; '.join(m.value for m in self.mails)}"

        if hasattr(self, "location") and self.location:
            return_res += f", location: {self.location}"

        return return_res


class AddressBook(UserDict):
    def add_record(self, new_contact: Record) -> None:
        self.data[new_contact.name.value] = new_contact
        # print(self.data)
        return f"Contact {new_contact.name.value} added succefully"

    def find(self, name):
        for rec in self.data:
            if rec == name:
                return self.data[rec]
        if not self.data.get(name):
            return None

    def search(self, arg):
        return_str = "didn'd find number or characters"
        for rec, phone in self.data.items():
            # print(rec, phone)
            if arg in str(phone):
                if return_str == "didn'd find number or characters":
                    return_str = ""
                return_str += str(self.data[rec]) + "\n"
            # else:
            #     return "didn'd find number or characters"
        return return_str

    def delete(self, name):
        if not self.data.get(name):
            return f"did't delete contact {name}, not exsist"
        else:
            del self.data[name]
            return f"Contact {name} delete succsefull"

    def iterator(self, n=2):
        self.counter = 0
        self.list = []
        # self.data_list = list(self.data.items())
        if len(self.data) >= 1:
            for _, val in self.data.items():
                self.list.append(str(val))
            while self.counter < len(self.list):
                yield self.list[self.counter : self.counter + n]
                self.counter += n
            raise StopIteration("End of list")
        else:
            raise StopIteration("Empty list")

    def show_all(self, data):
        for name, obj in self.data.items():
            data[name] = obj
        return data

    # def pack_user(self, records):
    #     self.data = records
    #     # print(records.data, records, self.data)
    #     file_name = os.getenv("SystemDrive") + "\\py_robot\\users.bin"
    #     os.makedirs(os.path.dirname(file_name), exist_ok=True)
    #     with open(file_name, "wb") as fh:
    #         # print(self.data)
    #         pickle.dump(self.data, fh)

    # def unpack_user(self):
    #     file_name = os.getenv("SystemDrive") + "\\py_robot\\users.bin"
    #     if exists(file_name):
    #         with open(file_name, "rb") as fh:
    #             unpacked = pickle.load(fh)

    #         for name, object in unpacked.items():
    #             self[name] = object

    #         return self