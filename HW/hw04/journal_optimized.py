from abc import ABC, abstractmethod
import csv
from pathlib import Path
import sys

from colorama import Fore, init, Style


STUDENT_MANAGEMENT_COMMANDS = ('add', 'show all', 'show', 'remove', 'grade', 'update')
AUXILIARY_COMMANDS = ('help', 'quit')
COMMAND_LIST = ', '.join((*STUDENT_MANAGEMENT_COMMANDS, *AUXILIARY_COMMANDS))


# ######################################################################################################################
# Infrastructure
# ######################################################################################################################

class AbstractRepository(ABC):

    @abstractmethod
    def _read_storage(self):
        pass

    @abstractmethod
    def _write_storage(self):
        pass

    @abstractmethod
    def add_student(self, student: dict):
        pass

    @abstractmethod
    def get_all_students(self):
        pass

    @abstractmethod
    def get_student(self, id_: int):
        pass

    @abstractmethod
    def update_student(self, id_: int, data: dict):
        pass

    @abstractmethod
    def delete_student(self, id_: int):
        pass

    @abstractmethod
    def add_mark(self, id_: int, mark: int):
        pass


class Repository(AbstractRepository):

    def __init__(self, file_path):
        self.file_path = file_path
        self.students = {}
        self._read_storage()

    def get_next_id(self):
        """Returns id to assign for the next student"""
        if len(self.students) == 0:
            return 1
        else:
            return max([int(key) for key in self.students.keys()]) + 1

    def _read_storage(self):
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.students[int(row['id'])] = {'name': row['name'],
                                                 'info': row['info'],
                                                 'marks': [int(mark) for mark in row['marks'].split(',') if mark]}

    def _write_storage(self):
        with open(self.file_path, 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'info', 'marks']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for key, student in self.students.items():
                writer.writerow({'id': key,
                                 'name': student['name'],
                                 'info': student['info'],
                                 'marks': ','.join(str(mark) for mark in student['marks'])})

    def add_student(self, student: dict):
        key = self.get_next_id()
        self.students[key] = student
        with open(self.file_path, 'a', newline='') as csvfile:
            fieldnames = ['id', 'name', 'info', 'marks']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': key,
                             'name': student['name'],
                             'info': student['info'],
                             'marks': ','.join([str(mark) for mark in student['marks']])})

    def get_all_students(self):
        self._read_storage()
        return self.students

    def get_student(self, id_: int):
        self._read_storage()
        return self.students[id_]

    def update_student(self, id_: int, data: dict):
        self.students[id_].update(data)
        self._write_storage()

    def delete_student(self, id_: int):
        del self.students[id_]
        self._write_storage()

    def add_mark(self, id_: int, mark: int):
        self.students[id_]['marks'].append(mark)
        self._write_storage()

    def __len__(self):
        return len(self.students)

# ######################################################################################################################
# Helpers
# ######################################################################################################################
def get_string_of_marks(student: dict):
    """Returns string of student's marks separated by space"""
    return " ".join([str(i) for i in student["marks"]])


def parse_add_student_input(add_student_input: str):
    if add_student_input.count(';') == 2:
        raw_name, raw_marks, raw_details = add_student_input.split(';')
        if raw_marks.strip() == '':
            marks = None
        else:
            try:
                marks = [int(mark) for mark in raw_marks.split(',')]
            except ValueError:
                return None
        return {'name': raw_name.strip(), 'marks': marks, 'info': raw_details.strip()}
    else:
        return None

def print_error(text):
    print(Fore.RED + text + Style.RESET_ALL)

def print_success(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

# ######################################################################################################################
# CRUD
# ######################################################################################################################
class StudentService:

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def add_student(self, name: str, marks: list[int] | None, details: str | None):
        student = {"name": name,
                   "marks": marks if marks else [],
                   "info": details if details else ""}
        self.repository.add_student(student)

    def get_students(self):
        return self.repository.get_all_students()

    def get_student_info(self, id_: int):
        return self.repository.get_student(id_)

    def remove_student(self, id_: int):
        self.repository.delete_student(id_)

    def add_mark(self, id_: int, mark: int):
        self.repository.add_mark(id_, mark)

    def update_student(self, id_: int, name: str|None=None, info: str|None=None):
        data = {}
        if name is not None:
            data['name'] = name
        if info is not None:
            data['info'] = info
        self.repository.update_student(id_, data)

    def number_of_students(self):
        return len(self.repository)

# ######################################################################################################################
# Command handlers
# ######################################################################################################################
def help_handler():
    print('Welcome to DIGITAL JOURNAL APP\n'
          'It helps to manage students assessment\n\n'
          'The following commands are available:\n'
          '\tshow all - lists all students (only names and marks will be displayed)\n'
          '\tshow - shows record for specific student (all information will be displayed)\n'
          '\tadd - adds new student to journal (it is required to enter name and optionally marks from paper journal and information about student could be entered)\n'
          '\tremove - removes student from journal\n'
          '\tgrade - adds new mark for student\n'
          '\tupdate - updates name or/and information about student\n'
          '\thelp - displays this help\n'
          '\tquit - quit the application\n')


def search_student_handler(student_service: StudentService, raw_id: str):
    try:
        id_ = int(raw_id)
        student = student_service.get_student_info(int(raw_id))
    except ValueError:
        print_error('Student id should be integer\n')
        return
    except KeyError:
        print_error(f"Student with id={raw_id} is missing in the students list\n")
        return
    return id_, student


def add_student_handler(student_service: StudentService):
    ask_prompt = "Enter student's payload data using text template (name is obligatory field, details is optional field)\n" \
                 "John Doe;1,2,3,4,5;Some details about John:\n"
    add_student_input = input(ask_prompt).strip()
    parsed_student_data = parse_add_student_input(add_student_input)
    if parsed_student_data:
        answer = input('Would you like to add new student? [y|yes / n|no]: ').strip().lower()
        if answer in ('y', 'yes'):
            student_service.add_student(parsed_student_data['name'], parsed_student_data['marks'], parsed_student_data['info'])
            print_success('New student added\n')
        else:
            print_error('Action was cancelled\n')
    else:
        print_error("Input string couldn't be parsed. Please check format\n")


def remove_student_handler(student_service: StudentService):
    raw_id = input("Enter student's id to remove: ").strip()
    student_pair = search_student_handler(student_service, raw_id)
    if student_pair:
        id_, _ = student_pair
        answer = input('Would you like to remove student? [y|yes / n|no]: ').strip().lower()
        if answer in ('y', 'yes'):
            student_service.remove_student(id_)
            print_success('Student was removed\n')
        else:
            print_error('Action was cancelled\n')


def show_student_info_handler(student_service: StudentService):
    raw_id = input("Enter student's id to display info: ").strip()
    student_pair = search_student_handler(student_service, raw_id)
    if student_pair:
        id_, student = student_pair
        student_service.get_student_info(id_)
        print('===================\n'
              f'{student["name"]}\n'
              f'Marks: {get_string_of_marks(student)}\n'
              f'Information: {student["info"]}\n')


def show_students_handler(student_service: StudentService):
    if student_service.number_of_students() > 0:
        for key, student in student_service.get_students().items():
            print('===================\n'
                  f'{key}. {student["name"]}\n'
                  f'Marks: {get_string_of_marks(student)}')
    else:
        print("No students are added at the moment")
    print()


def grade_student_handler(student_service: StudentService):
    raw_id = input("Enter student's id to add mark: ").strip()
    student_pair = search_student_handler(student_service, raw_id)
    if student_pair:
        id_, student = student_pair
        try:
            mark = int(input("Enter new mark for student [1-12]: "))
            if not 1 <= mark <= 12:
                raise ValueError('Entered mark not in a range 1-12')

            answer = input('Would you like to add new mark for student? [y|yes / n|no]: ').strip().lower()
            if answer in ('y', 'yes'):
                student_service.add_mark(id_, mark)
                print_success(f"Updated marks for {student['name']}: {get_string_of_marks(student)}\n")
            else:
                print_error('Action was cancelled\n')

        except ValueError:
            print_error("Mark should be integer from 1 to 12\n")


def update_student_handler(student_service: StudentService):
    raw_id = input("Enter student's id to update: ").strip()
    student_pair = search_student_handler(student_service, raw_id)
    if student_pair:
        id_, student = student_pair
        name = input(f"Enter new name to update '{student['name']}'. Enter 'no' to skip: ").strip()
        name = None if name.strip().lower() == 'no' else name

        print(f"Current student info: '{student['info']}'")
        info = input("Enter new info to modify. Start with '+' symbol if you want to append. Enter 'no' to skip: ").strip()  # TODO: update with validation logic
        if info.strip().lower() == 'no':
            info = None
        if info is not None and info.startswith('+'):
            info = f"{student['info']} {info[1:]}"  # cut '+' symbol from input

        answer = input("Would you like to update student's name/info? [y|yes / n|no]: ").strip().lower()
        if answer in ('y', 'yes'):
            student_service.update_student(id_, name, info)
            print_success(f"Student record was updated\n")
        else:
            print_error('Action was cancelled\n')


def main():
    init()  # colorama initialization
    help_handler()

    if len(sys.argv) == 1:
        storage_file_path = 'students.csv'
    elif len(sys.argv) == 2:
        storage_file_path = sys.argv[1]
    else:
        print('Digital Journal App takes no parameters or 1 parameter for file path')
        sys.exit(1)

    if not Path(storage_file_path).exists():
        Path(storage_file_path).touch()
        print("New storage file is created\n")

    repository = Repository(storage_file_path)
    student_service = StudentService(repository)


    while True:
        command = input(f"Enter one of the commands: {COMMAND_LIST}: ").strip().lower()
        match command:
            case 'quit':
                print("Thank you for using Digital Journal App")
                break
            case 'help':
                help_handler()
            case 'add':
                add_student_handler(student_service)
            case 'show':
                show_student_info_handler(student_service)
            case 'show all':
                show_students_handler(student_service)
            case 'remove':
                remove_student_handler(student_service)
            case 'grade':
                grade_student_handler(student_service)
            case 'update':
                update_student_handler(student_service)
            case _:
                print_error("Unknown command\n")


if __name__ == '__main__':
    main()
