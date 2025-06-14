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
