# storage = [{
#     "name": "Alice Cooper",
#     "marks": [4, 9, 10, 12, 8, 3],
#     "info": "19 y.o. Hobby is music"
# }]

import json

with open('students.json', 'r') as f:
    storage = json.load(f)




"""
  - `main()` - application entrypoint
  - `show_students()` - function to represent all students
  - `show_student(id: int)` - function to show student by `id`
  - `add_student(name: str, marks: list[int], details: str | None)`
"""


def show_students():
    for student in storage:
        print('===================\n'
              f'{student["name"]}\n'
              f'Marks: {" ".join([str(i) for i in student["marks"]])}')


def show_student(id: int):
    pass


def add_student(name: str, marks: list[int], details: str | None):
    pass


STUDENT_MANAGEMENT_COMMANDS = ('add', 'show all', 'show')
AUXILIARY_COMMANDS = ('help', 'quit')


def main():
    print("Welcome to DIGITAL JOURNAL APP\n")

    while True:
        command = input(f"Enter one of the commands: {(*STUDENT_MANAGEMENT_COMMANDS, *AUXILIARY_COMMANDS)}: ")
        match command:
            case 'quit':
                break
            case 'help':
                print('This is Digital Journal App\n'
                      'It helps to manage students assessment')
            case 'add':
                ask_prompt = "Enter student's payload data using text template\n" \
                             "John Doe;1,2,3,4,5\n"
                add_student()
            case 'show': # TODO: id is missing in storage
                id_string = input("Enter student's id to display info: ")
                try:
                    id = int(id_string)
                    show_student(id)
                except ValueError:
                    print("Entered value is not student id")
            case 'show all':
                show_students()
            case _:
                print("Unknown command")


if __name__ == '__main__':
    main()
