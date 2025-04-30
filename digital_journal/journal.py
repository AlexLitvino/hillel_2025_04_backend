import json

with open('students.json', 'r') as f:
    storage: list[dict] = json.load(f)

STUDENT_MANAGEMENT_COMMANDS = ('add', 'show all', 'show')
AUXILIARY_COMMANDS = ('help', 'quit')
COMMAND_LIST = ', '.join((*STUDENT_MANAGEMENT_COMMANDS, *AUXILIARY_COMMANDS))


def get_max_id():
    return max([student['id'] for student in storage])


def get_string_of_marks(student):
    return " ".join([str(i) for i in student["marks"]])


def print_help():
    print('This is Digital Journal App\n'
          'It helps to manage students assessment\n')


def parse_add_student_input(add_student_input:str):
    if add_student_input.count(';') == 0:
        name = add_student_input
        details = ''
    else:
        name, details = add_student_input.split(';')
    return name.strip(), details.strip()


def add_student(name: str, marks: list[int], details: str | None):
    student = {"id": get_max_id() + 1,
               "name": name,
               "marks": [],
               "info": details if details else ""}
    storage.append(student)


def add_student_handler():
    ask_prompt = "Enter student's payload data using text template (name is obligatory field, details is optional field)\n" \
                 "John Doe;Some details about John:\n"
    add_student_input = input(ask_prompt).strip()
    if add_student_input.count(';') > 1:
        print("Student's payload data could contain one or zero semicolon")
    else:
        name, details = parse_add_student_input(add_student_input)
        add_student(name, marks=None, details=details)  # TODO: no need to pass marks?
    print()


def show_student(id_: int):
    student = [student for student in storage if student['id'] == id_][0]
    print('===================\n'
          f'{student["name"]}\n'
          f'Marks: {get_string_of_marks(student)}\n'
          f'Information: {student["info"]}\n')


def show_student_info_handler():
    try:
        id_ = int(input("Enter student's id to display info: "))
        if id_ in [student["id"] for student in storage]:
            show_student(id_)
        else:
            print(f"Student with id={id_} is missing in the students list\n")
    except ValueError:
        print("Entered value is not valid student id. It should be integer\n")


def show_students():
    for student in storage:
        print('===================\n'
              f'{student["id"]}. {student["name"]}\n'
              f'Marks: {get_string_of_marks(student)}')
    print()


def main():
    print("Welcome to DIGITAL JOURNAL APP\n")

    while True:
        command = input(f"Enter one of the commands: {COMMAND_LIST}: ").strip().lower()
        match command:
            case 'quit':
                break
            case 'help':
                print_help()
            case 'add':
                add_student_handler()
            case 'show':
                show_student_info_handler()
            case 'show all':
                show_students()
            case _:
                print("Unknown command\n")


if __name__ == '__main__':
    main()
