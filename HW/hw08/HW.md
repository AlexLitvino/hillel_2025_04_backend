Imagine that in your Digital Journal Application you have `100.000` students 
(let's say the system is used in many facilities) and MANY MANY students' marks which you process in your application.

I want the application to SEND the EMAIL with REPORT that includes:

- The total number of students
  - every month

- The total average mark
  - every day I wanna see the "Average Mark"
    - only marks from this day should be included in the analytics
    - it means that you have to add `creation_date` to your `mark` instance in the data structure

Sending reports should not block user's input process (must be IO non-blocking)
P.S You can set the `dict` as your simulated storage instead of using files
P.P.S. When you will implement a new feature you may improve the performance with multithreading / multiprocessing / asyncio.
It is optional but preferred. You can decide be yourself what component should be improved.


https://github.com/AlexLitvino/hillel_2025_04_backend/pull/11

Calculating average mark is made for yesterday instead of today, as for today data could be incomplete

random_data_generator.py is updated, so it now creates students with marks in the past upto today (not for all days, for some days marks are missing)

I checked average mark calculation done with one process and with number of CPU processes.

Strange but one process wins for 1000 and 1000_000 students:

Copy code
Users                1000                   1000_000
One process         0.00040449993684887886  0.2397951000602916
CPU# processes      0.7411272999597713      9.727466400014237
I implemented managing many processes manually because I didn't get idea how to start ProcessPoolExecutor with passing iterable and arg (search_date) in target function. Also faced problems that multiprocessing.Manager().dict and list doesn't work in this case (typeerror: cannot pickle 'weakref.referencetype' object).


# COMMENTS
100 балiв
Student creation date is not tracked, so monthly new student reporting cannot be done 😄
- Add and use a creation_date field for each student
