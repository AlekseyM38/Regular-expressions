import re
from pprint import pprint
import csv
from collections import defaultdict


pattern = r'(?:\+?([0-9]{1,3})[\s\-]?)?(\(?\d{3}\)?)[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})(?:[\s\-]?(?:доб\.?\s|\(доб\.?\s|\(доб\s)?(\d+))?\)?'

# Функция для замены формата телефонных номеров
def replace_phone(match):
    country_code = '+7'
    area_code = match.group(2).strip('()')
    main_number = match.group(3) + match.group(4) + match.group(5)
    extension = ' доб.' + match.group(6) if match.group(6) else ''

    if len(main_number) > 7:
        formatted_main_number = f'{main_number[:3]}-{main_number[3:5]}-{main_number[5:7]}-{main_number[7:]}'
    else:
        formatted_main_number = f'{main_number[:3]}-{main_number[3:5]}-{main_number[5:7]}'

    if formatted_main_number.endswith(')'):
        formatted_main_number = formatted_main_number[:-1]

    formatted_phone = f'{country_code}({area_code}){formatted_main_number}{extension}.'

    return formatted_phone


with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)
for contact in contacts_list[:len(contacts_list)]:
    print(contact)

for contact in contacts_list:
    name_parts = contact[0].split()

    if len(name_parts) > 1:
        contact[0] = name_parts[0]
        contact[1] = ' '.join(name_parts[1:])

    first_name_parts = contact[1].split()
    if len(first_name_parts) > 1:
        contact[1] = first_name_parts[0]
        contact[2] = ' '.join(first_name_parts[1:])

    for i in range(len(contact)):
        if re.match(pattern, contact[i]):
            contact[i] = re.sub(pattern, replace_phone, contact[i])

# pprint(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list)

contacts_dict = defaultdict(list)

with open("phonebook.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        if len(row) >= 2:
            full_name = (row[0], row[1])
            contacts_dict[full_name].append(row)

merged_contacts = []

for full_name, records in contacts_dict.items():
    merged_record = [full_name[0], full_name[1]]
    if records:
        for i in range(2, len(records[0])):
            merged_data = max((record[i] for record in records if record[i]), key=len, default='')
            merged_record.append(merged_data)
    else:
        merged_record.extend([''] * (len(records[0]) - 2))
    merged_contacts.append(merged_record)

with open("merged_phonebook.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["lastname", "firstname", "surname", "organization", "position", "phone", "email"])  # Заголовок
    writer.writerows(merged_contacts)

print("Объединенный файл сохранен как 'merged_phonebook.csv'")

