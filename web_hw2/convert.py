import re
from datetime import datetime

def convert_str_dict (data_string_to_convert):
    # Визначте регулярний вираз для вилучення інформації
    pattern = re.compile(r"Contact name: (?P<name>.*?), birthday: (?P<birthday>\d{4}-\d{1,2}-\d{1,2})")

    matches = pattern.finditer(data_string_to_convert)

    # Створіть список словників з вилученою інформацією
    users = []
    for match in matches:
        name = match.group("name")
        birthday_str = match.group("birthday")
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
        user = {"name": name, "birthday": birthday}
        #user = {name: birthday}
        users.append(user)
    return users


if __name__ == "__main__":

    data_string = """
                Contact name: my1, phones: 0934283855; 0934283855, birthday: 1990-12-26
                Contact name: Bill, birthday: 1990-12-26
                Contact name: John, birthday: 1995-12-29
                Contact name: Tilda, birthday: 2000-12-30
                Contact name: Marry, birthday: 2000-1-1
                Contact name: Denis, birthday: 2005-1-2
                Contact name: Alex, birthday: 1990-1-3
                Contact name: JanKoum, birthday: 1976-1-1
                """
    result = convert_str_dict (data_string)
    print(result)

#[{'name': 'Bill', 'birthday': datetime.date(1990, 12, 26)}, 
#{'name': 'John', 'birthday': datetime.date(1995, 12, 29)}, 
#{'name': 'Tilda', 'birthday': datetime.date(2000, 12, 30)},
#{'name': 'Marry', 'birthday': datetime.date(2000, 1, 1)}, 
#{'name': 'Denis', 'birthday': datetime.date(2005, 1, 2)}, 
#{'name': 'Alex', 'birthday': datetime.date(1990, 1, 3)}, 
# {'name': 'JanKoum', 'birthday': datetime.date(1976, 1, 1)}]