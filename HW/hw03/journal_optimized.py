import json
import operator
import sys

storage: dict[str, dict] = {}  # global variable to keep students list


STUDENT_MANAGEMENT_COMMANDS = ('add', 'show all', 'show', 'remove', 'grade', 'update')
AUXILIARY_COMMANDS = ('help', 'quit')
COMMAND_LIST = ', '.join((*STUDENT_MANAGEMENT_COMMANDS, *AUXILIARY_COMMANDS))


# ######################################################################################################################
# Helpers
# ######################################################################################################################

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
        return "1"
    else:
        return str(max([int(key) for key in storage.keys()]) + 1)


def get_string_of_marks(student):
    """Returns string of student's marks separated by space"""
    return " ".join([str(i) for i in student["marks"]])


def parse_add_student_input(add_student_input:str):
    if add_student_input.count(';') == 2:
        raw_name, raw_marks, raw_details = add_student_input.split(';')
        if raw_marks.strip() == '':
            marks = None
        else:
            try:
                marks = [int(mark) for mark in raw_marks.split(',')]
            except ValueError:
                return None
        return raw_name.strip(), marks, raw_details.strip()
    else:
        return None


def search_student(raw_id):
    student = storage.get(raw_id)
    if student is None:
        print(f"Student with id={raw_id} is missing in the students list\n")
        return None
    else:
        return raw_id, student

# ######################################################################################################################
# CRUD
# ######################################################################################################################
def add_student(name: str, marks: list[int] | None, details: str | None):
    student = {"name": name,
               "marks": marks if marks else [],
               "info": details if details else ""}
    storage[get_next_id()] = student


def show_students():
    if len(storage) > 0:
        for key, student in storage.items():
            print('===================\n'
                  f'{key}. {student["name"]}\n'
                  f'Marks: {get_string_of_marks(student)}')
    else:
        print("No students are added at the moment")
    print()


def show_student(student: dict):
    print('===================\n'
          f'{student["name"]}\n'
          f'Marks: {get_string_of_marks(student)}\n'
          f'Information: {student["info"]}\n')


def remove_student(id_: str):
    del storage[id_]


def add_mark(student: dict, mark: int):
    student['marks'].append(mark)


def update_student(student, name=None, info=None):
    if name is not None:
        student['name'] = name
    if info is not None:
        student['info'] = info

# ######################################################################################################################
# Command handlers
# ######################################################################################################################
def help_handler():
    print('This is Digital Journal App\n'
          'It helps to manage students assessment\n')

def add_student_handler():
    ask_prompt = "Enter student's payload data using text template (name is obligatory field, details is optional field)\n" \
                 "John Doe;1,2,3,4,5;Some details about John:\n"
    add_student_input = input(ask_prompt).strip()
    parsed_student_data = parse_add_student_input(add_student_input)
    if parsed_student_data:
        add_student(*parsed_student_data)
        print('New student added\n')
    else:
        print("Input string couldn't be parsed. Please check format\n")
    print()


def remove_student_handler():
    raw_id = input("Enter student's id to remove: ").strip()
    student_pair = search_student(raw_id)
    if student_pair:
        id_, _ = student_pair
        remove_student(id_)
        print('Student was removed\n')


def show_student_info_handler():
    raw_id = input("Enter student's id to display info: ").strip()
    student_pair = search_student(raw_id)
    if student_pair:
        _, student = student_pair
        show_student(student)


def grade_student_handler():
    raw_id = input("Enter student's id to add mark: ").strip()
    student_pair = search_student(raw_id)
    if student_pair:
        _, student = student_pair
        try:
            mark = int(input("Enter new mark for student [1-12]: "))
            if not 1 <= mark <= 12:
                raise ValueError
            add_mark(student, mark)
            print(f"Updated marks for {student['name']}: {get_string_of_marks(student)}")
            print()
        except ValueError:
            print("Mark should be integer from 1 to 12\n")


def update_student_handler():
    raw_id = input("Enter student's id to update: ").strip()
    student_pair = search_student(raw_id)
    if student_pair:
        _, student = student_pair
        name = input(f"Enter new name to update '{student['name']}'. Enter 'no' to skip: ").strip()
        name = None if name.strip().lower() == 'no' else name

        print(f"Current student info: '{student['info']}'")
        info = input("Enter new info to modify. Start with '+' symbol if you want to append. Enter 'no' to skip: ").strip()  # TODO: update with validation logic
        if info.strip().lower() == 'no':
            info = None
        if info is not None and info.startswith('+'):
            info = f"{student['info']} {info[1:]}"  # cut '+' symbol from input

        update_student(student, name, info)
        print()


def main():
    print("Welcome to DIGITAL JOURNAL APP\n")

    if len(sys.argv) == 1:
        storage_file_path = 'students_optimized.json'
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
            case 'grade':
                grade_student_handler()
            case 'update':
                update_student_handler()
            case _:
                print("Unknown command\n")


if __name__ == '__main__':
    main()
