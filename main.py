from collections import UserDict
from collections.abc import Iterator
from datetime import datetime, timedelta
import re
import pickle


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


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) > 17:
            return "Invalid phone number format"
        else:
            res = re.findall("\+\d{3} \d{2} \d{3}-\d{2}-\d{2}", value)
            if res == []:
                return "Invalid phone number format"
            else:
                Field.value.fset(self, value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        Field.value.fset(self, value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if type(value) == str:
            if len(value) > 10:
                return "Invalid date format"
            else:
                res = re.findall("\d{0,4}-\d{1,2}-\d{1,2}", value)
                if res == []:
                    return "Invalid date format"
                else:
                    Field.value.fset(self, value)
        else:
            return "Invalid date format"


class Record:
    def __init__(self, name: Name, phone=None, birthday=Birthday):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def find_phone(self, value):
        pass

    def days_to_birthday(self):
        if self.birthday != None:
            date_of_birth = datetime.strptime(self.birthday, '%Y-%m-%d').date()

            current_data = datetime.now().date()
            diff = (date_of_birth - current_data).days
            return diff
        else:
            return "No date of birth"


class Iterator():
    def __init__(self, value_to_show, length_of_AddressBook, data):
        self.value_to_show = value_to_show
        self.length_of_AddressBook = length_of_AddressBook
        self.end = value_to_show
        self.data = data
        self.dict = {}
        self.count = 0
        count = 0
        for key in self.data.keys():
            self.dict[count] = key
            count += 1
        self.flag = True
        self.first_itteration = True

    def __next__(self):
        list_to_show_1 = []
        list_to_show_2 = []

        if self.flag:
            if self.end <= self.length_of_AddressBook:
                for _ in range(0, self.value_to_show):
                    key = self.dict.get(self.count)
                    temp_dict = {}
                    temp_list_phones = []
                    temp_dict['Name'] = key
                    for phone in self.data[key].phones:
                        temp_list_phones.append(phone.value)
                    temp_dict['Contact'] = temp_list_phones, self.data[key].birthday.value
                    list_to_show_1.append(temp_dict)
                    self.count += 1
                if self.end == self.length_of_AddressBook:
                    self.flag = False
                self.end += self.value_to_show
                self.first_itteration = False
                return list_to_show_1
            else:
                if self.first_itteration:
                    self.end = self.end - \
                        (self.end - self.length_of_AddressBook)
                else:
                    self.end = self.end - self.value_to_show
                    self.end = self.length_of_AddressBook - self.end
                for f in range(0, self.end):
                    key = self.dict.get(self.count)
                    temp_dict = {}
                    temp_list_phones = []
                    temp_dict['Name'] = key
                    for phone in self.data[key].phones:
                        temp_list_phones.append(phone.value)
                    temp_dict['Contact'] = temp_list_phones, self.data[key].birthday.value
                    list_to_show_2.append(temp_dict)
                    self.count += 1
                self.flag = False
                return list_to_show_2
        else:
            raise StopIteration


class AddressBook(UserDict):
    file_name = 'data.bin'

    def __iter__(self) -> Iterator:
        return Iterator(self.value_to_show, len(self.data), self.data)

    def how_many_to_show(self, value):
        self.value_to_show = value

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, values):
        list_to_show = []
        if values == []:
            return "Nothing to search."
        else:
            print("An example of how to find correctly: 'Name' 'phone'")
        values = values.split()
        for person in self.data:
            for value in values:
                if value.lower() in person.lower():
                    temp_list_phones = []
                    temp_dict = {}
                    temp_dict['Name'] = person
                    for phone in self.data[person].phones:
                        temp_list_phones.append(phone.value)
                    temp_dict['Contact'] = temp_list_phones, self.data[person].birthday.value
                    list_to_show.append(temp_dict)

                for phone in self.data[person].phones:
                    if value.lower() in phone.value:
                        temp_list_phones = []
                        temp_dict = {}
                        temp_dict['Name'] = person
                        for phone in self.data[person].phones:
                            temp_list_phones.append(phone.value)
                        temp_dict['Contact'] = temp_list_phones, self.data[person].birthday.value
                        list_to_show.append(temp_dict)
        return list_to_show

    def save_to_file(self):
        with open(AddressBook.file_name, 'wb') as fh:
            pickle.dump(self.data, fh)

    def reed_from_file(self):
        with open(AddressBook.file_name, 'rb') as fh:
            content = pickle.load(fh)
        return content


if __name__ == "__main__":
    name = Name('Oleksii')
    phone = Phone('+380 98 323-55-17')
    birthday = Birthday('1985-07-02')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 67 598-22-36')
    ab = AddressBook()
    ab.add_record(rec)

    name = Name('Egor')
    phone = Phone('+380 63 453-54-22')
    birthday = Birthday('1979-11-24')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 93 541-81-12')
    ab.add_record(rec)

    name = Name('Andrii')
    phone = Phone('+380 96 290-05-57')
    birthday = Birthday('1993-10-17')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 93 865-67-31')
    ab.add_record(rec)

    name = Name('Vlad')
    phone = Phone('+380 66 771-94-15')
    birthday = Birthday('1989-07-21')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 50 590-89-67')
    ab.add_record(rec)

    ab.save_to_file()
    contacts_from_file = ab.reed_from_file()

    print(ab.find_record('Ole'))
