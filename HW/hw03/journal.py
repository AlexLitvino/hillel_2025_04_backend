import json
import sys

storage: list[dict] = []  # global variable to keep students list


STUDENT_MANAGEMENT_COMMANDS = ('add', 'show all', 'show', 'remove')
AUXILIARY_COMMANDS = ('help', 'quit')
COMMAND_LIST = ', '.join((*STUDENT_MANAGEMENT_COMMANDS, *AUXILIARY_COMMANDS))


def read_storage_file(file_path):
    with open(file_path, 'r') as f:
        storage_content = json.load(f)
    return storage_content


def save_storage_file(file_path):
    with open(file_path, 'w') as f:
        json.dump(storage, f, indent=4)


def get_next_id():
    """Returns id to assign for the next student"""
    if len(storage) == 0:
        return 1
    else:
        return max([student['id'] for student in storage]) + 1


def get_string_of_marks(student):
    """Returns string of student's marks separated by space"""
    return " ".join([str(i) for i in student["marks"]])


def parse_add_student_input(add_student_input:str):
    if add_student_input.count(';') == 0:
        name = add_student_input
        details = ''
    else:
        name, details = add_student_input.split(';')
    return name.strip(), details.strip()


# ######################################################################################################################
# CRUD
# ######################################################################################################################
def add_student(name: str, marks: list[int], details: str | None):
    student = {"id": get_next_id(),
               "name": name,
               "marks": [],
               "info": details if details else ""}
    storage.append(student)


def show_students():
    if len(storage) > 0:
        for student in storage:
            print('===================\n'
                  f'{student["id"]}. {student["name"]}\n'
                  f'Marks: {get_string_of_marks(student)}')
    else:
        print("No students are added at the moment")
    print()


def show_student(id_: int):
    student = [student for student in storage if student['id'] == id_][0]
    print('===================\n'
          f'{student["name"]}\n'
          f'Marks: {get_string_of_marks(student)}\n'
          f'Information: {student["info"]}\n')

def remove_student(id_: int):
    for index, student in enumerate(storage):
        if student['id'] == id_:
            del storage[index]
            break


# ######################################################################################################################
# Command handlers
# ######################################################################################################################
def help_handler():
    print('This is Digital Journal App\n'
          'It helps to manage students assessment\n')

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


def remove_student_handler():
    try:
        id_ = int(input("Enter student's id to remove: "))
        if id_ in [student["id"] for student in storage]:
            remove_student(id_)
            print()
        else:
            print(f"Student with id={id_} is missing in the students list\n")
    except ValueError:
        print("Entered value is not valid student id. It should be integer\n")


def show_student_info_handler():
    try:
        id_ = int(input("Enter student's id to display info: "))
        if id_ in [student["id"] for student in storage]:
            show_student(id_)
        else:
            print(f"Student with id={id_} is missing in the students list\n")
    except ValueError:
        print("Entered value is not valid student id. It should be integer\n")





def main():
    print("Welcome to DIGITAL JOURNAL APP\n")

    if len(sys.argv) == 1:
        storage_file_path = 'students.json'
    elif len(sys.argv) == 2:
        storage_file_path = sys.argv[1]
    else:
        print('Digital Journal App takes no parameters or 1 parameter for file path')
        sys.exit(1)

    global storage
    try:
        storage = read_storage_file(storage_file_path)
    except FileNotFoundError:
        print("New storage file will be created\n")

    while True:
        command = input(f"Enter one of the commands: {COMMAND_LIST}: ").strip().lower()
        match command:
            case 'quit':
                save_storage_file(storage_file_path)  # TODO: if storage wasn't changed no reason to re-save file
                break
            case 'help':
                help_handler()
            case 'add':
                add_student_handler()
            case 'show':
                show_student_info_handler()
            case 'show all':
                show_students()
            case 'remove':
                remove_student_handler()
            case _:
                print("Unknown command\n")


if __name__ == '__main__':
    main()
