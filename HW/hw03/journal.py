import json
import sys

storage: list[dict] = []  # global variable to keep students list


STUDENT_MANAGEMENT_COMMANDS = ('add', 'show all', 'show', 'remove', 'grade', 'update')
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


# ######################################################################################################################
# CRUD
# ######################################################################################################################
def add_student(name: str, marks: list[int] | None, details: str | None):
    student = {"id": get_next_id(),
               "name": name,
               "marks": marks if marks else [],
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


def add_mark(id_: int, mark: int):
    student = [student for student in storage if student['id'] == id_][0]
    student['marks'].append(mark)


def update_student(id_, name=None, info=None):
    student = [student for student in storage if student['id'] == id_][0]
    if name:
        student['name'] = name
    if info:
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


def grade_student_handler():
    try:
        id_ = int(input("Enter student's id to add mark: "))
        if id_ in [student["id"] for student in storage]:
            try:
                mark = int(input("Enter new mark for student [1-12]: "))
                if not 1 <= mark <= 12:
                    raise ValueError
                add_mark(id_, mark)
                print()
            except ValueError:
                print("Mark should be integer from 1 to 12\n")
        else:
            print(f"Student with id={id_} is missing in the students list\n")
    except ValueError:
        print("Entered value is not valid student id. It should be integer\n")


def update_student_handler():
    try:
        id_ = int(input("Enter student's id to update: "))
        if id_ in [student["id"] for student in storage]:
            student = [student for student in storage if student['id'] == id_][0]  # TODO: might be removed after refactoring
            name = input(f'Enter new name to update {student["name"]}. Press Enter to skip: ').strip()
            name = name if name else None

            info = input('Enter new info to update. Press Enter to skip: ').strip()  # TODO: update with validation logic
            info = info if info else None

            update_student(id_, name, info)
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
            case 'grade':
                grade_student_handler()
            case 'update':
                update_student_handler()
            case _:
                print("Unknown command\n")


if __name__ == '__main__':
    main()
