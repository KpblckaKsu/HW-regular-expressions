import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

for contact in contacts_list:
    if len(contact) > 7 and len(contact[7:]) <= 1:
        del(contact[7:])

# Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
for contact in contacts_list:
    name = []
    if len(contact[0].split(' ')) == 3:
        pattern = r"(\w+)(\s|,)(\w+)(\s|,)(\w+|,)"
        phones_list = re.findall(pattern, contact[0])
        result = re.sub(pattern, r"\1,\3,\5", contact[0])
        name.extend(result.split(','))
        del(contact[0:3])
        contact.insert(0, name[0])
        contact.insert(1, name[1])
        contact.insert(2, name[2])
    elif len(contact[0].split(' ')) == 2:
        pattern = r"(\w+)\s(\w+)"
        phones_list = re.findall(pattern, contact[0])
        result = re.sub(pattern, r"\1, \2", contact[0])
        name.extend(result.split(','))
        del(contact[0:2])
        contact.insert(0, name[0])
        contact.insert(1, name[1])
    elif len(contact[1].split(' ')) == 2:
        pattern = r"(\w+)\s(\w+)"
        phones_list = re.findall(pattern, contact[1])
        result = re.sub(pattern, r"\1,\2", contact[1])
        name.extend(result.split(','))
        del(contact[1:3])
        contact.insert(1, name[0])
        contact.insert(2, name[1])

# Привести все телефоны в формат +7(999)999-99-99.
# Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999
def phone_number(pattern, new_s, contacts_list):
    for contact in contacts_list:
        re.findall(pattern, contact[5])
        result = re.sub(pattern, new_s, contact[5])
        del (contact[5])
        contact.insert(5, result)

phone_number(r"(\+7)(\d+)(\d+\d+\d+)(\d+\d+)(\d+\d+)", r"+7(\2)\3-\4-\5", contacts_list)

phone_number(r"(8|\+7)(\s\(|\s|\()(\d+)(\)\s|\-|\))(\d+)\-(\d{2})\-?(\d{2})(\s\(|\s)?(доб.\s\d+)?\)?",
             r"+7(\3)\5-\6-\7 \9", contacts_list)

# Удаляем лишние пробелы в строках
new_contacts_list = []
for contact in contacts_list:
    new_contact = []
    for i in contact:
        k = i.strip()
        new_contact.append(k)
    new_contacts_list.append(new_contact)

#print(new_contacts_list)

cont_dict = {}
cont_dict_2 = {}
for contact in new_contacts_list:
    cont_dict = {}
    key = (contact[0], contact[1])
    value = contact[2:]
    cont_dict[key] = value
    for keys, values in cont_dict.items():
        if keys not in cont_dict_2.keys():
            cont_dict_2[keys] = value
        else:
            for i, val in enumerate(cont_dict_2[keys]):
                if len(val) == 0:
                    cont_dict_2[keys][i] = values[i]

# pprint(cont_dict_2)
new_list = []
for k, v in cont_dict_2.items():
    new_contact = []
    new_contact.extend(k)
    new_contact.extend(v)
    new_list.append(new_contact)
# pprint(len(new_list))

for contact in new_list:
    print(len(contact))
    print(contact)

with open("phonebook.csv", "w", encoding='UTF-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_list)
