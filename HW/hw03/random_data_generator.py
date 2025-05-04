import json
import random

from faker import Faker


number_of_students = 10
fake = Faker('en_GB')
interests = ["music", "painting", "photo", "cooking", "planting", "dances", "sport"]

students = []
students_optimized = {}

for i in range(number_of_students):
    name = fake.name()
    student = {"id": i + 1,
               "name": name,
               "marks": [random.randint(1, 12) for i in range(random.randint(5, 9))],
               "info": random.choice(['', f'{random.randint(15, 23)} y.o. Interests: {random.choice(interests)}'])}
    students.append(student)
    student.pop('id')
    students_optimized[i+1] = student

if __name__ == '__main__':
    with open('students.json', 'w') as f:
        json.dump(students, f, indent=4)
    with open('students_optimized.json', 'w') as f:
        json.dump(students_optimized, f, indent=4)  # https://stackoverflow.com/questions/17099556/why-do-int-keys-of-a-python-dict-turn-into-strings-when-using-json-dumps
