import csv
import datetime
import random

from faker import Faker


number_of_students = 10
fake = Faker('en_GB')
interests = ["music", "painting", "photo", "cooking", "planting", "dances", "sport"]

students = []

for i in range(number_of_students):
    name = fake.name()

    marks = []
    number_of_marks = random.randint(5, 9)
    for j in range(number_of_marks):
        if random.random() > 0.5:  # add if random > 0.5
            date = now = datetime.date.today() - datetime.timedelta(days=number_of_marks - j - 1)
            mark = random.randint(1, 12)
            marks.append((date, mark))

    student = {"id": i + 1,
               "name": name,
               "marks": marks,
               "info": random.choice(['', f'{random.randint(15, 23)} y.o. Interests: {random.choice(interests)}'])}
    students.append(student)

if __name__ == '__main__':
    with open('students.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'info', 'marks']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for student in students:
            writer.writerow({'id': student['id'],
                             'name': student['name'],
                             'info': student['info'],
                             'marks': ','.join(f"{date_mark[0].strftime('%Y-%m-%d')}|{date_mark[1]}" for date_mark in student['marks'])})