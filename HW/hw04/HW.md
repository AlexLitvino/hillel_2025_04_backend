## HW02
- Project from the lesson is set up
- `students: list[dict]` global variable exists to simulate the database (_the simulated storage for all the students_)
  - The `Student` data structure has next fields
    - `id: int` - unique identifier of the student
    - `name: str` - student's name
    - `marks: list[int]` - list of marks
    - `info: str` - detailed information of the student
- Next functions are added to the application:
  - `main()` - application entrypoint
  - `show_students()` - function to represent all students
  - `show_student(id: int)` - function to show student by `id`
  - `add_student(name: str, marks: list[int], details: str | None)` - function to add new student.
    - The `name` is required but the `details` is optional.
    - if `details` is optional - it is saved as empty string to the storage
    - The `marks` is always created as empty list
    - Yes, there is no way to add a mark after user is added (this is left for the next lessons)


## HW03
- "Add Student" feature is updated
  - USER can set `info` along with `name` and `marks`
  - `info` is OPTIONAL
- "Add Mark" must be implemented.
  - Detailed: You have to create User Interface for that feature in existing CLI application. Turn on your imagination
- "Smart Update" feature is implemented.
  - Instead of updating the whole user all the time (`name` and `info` fields) now the UPDATE FEATURE allows user to update only specified fields (`name` of `info` or both)
  - IF USER entered `info` the SYSTEM performs next validation
    - IF USER entered a string that is completely DIFFERENT FROM what we CURRENTLY have in storage - AUGMENT entered information to the existing value in storage
    - IF USER entered a string that INCLUDES the information, that exists in storage - REPLACE (update) it the storage
  - You have to THINK about the BEST UI/UX implementation


## HW04
- Persistent storage (as FILE) is added (or plugged) to the project
- All USER OPERATIONS now work with persistent storage instead of in-memory object
- Data must be stored in `.csv` format
- `class Repository` is responsible for the next operations:
    - reading `.csv` file content into local variable `students` to operate in application on startup
    - writing to the `.csv` file the content of `students` that is currently active in the state of this class
    - the `students` variable could be optimized to `dict` representation for optimization (P.S. might be better solution if you don't wanna refactor your existing solution too much)
    - `.add_student(student: dict)` to add student to the storage
    - `.get_student(id_: int)` to add student to the storage
    - `.update_student(id_: int, data: dict)` to partially update student (meaning that `data.keys()` must be appropriate student fields)
    - `.delete_student(id_: int)` to remove student from the storage
    - `.add_mark(id_: int, mark: int)` quickly add mark to specified user
- Repository object could be injected to each place of usage. P.S. If you prefer different way - please, go ahead
