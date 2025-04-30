### Opening existing non-empty storage

Start DJ App without parameters.  
Show all students.  
Verify that names and marks for all students are displayed.  

Show details for specific student with details.  
Verify that name, marks and details are displayed.  

Show details for specific student without details.  
Verify that name, marks and details as empty string are displayed.  

Add new student with details.  
Show details for added student.  
Verify that name, marks and details are displayed.  

Add new student without details.  
Show details for added student.  
Verify that name, marks and details as empty string are displayed.  

Show all students.  
Verify that two new students are displayed.  

Attempt to show details for non-existing student.
Verify that message about missing student is displayed.

Attempt to show details for student with invalid id.
Verify that message that id should be integer is displayed.  

Quit the app.  

Start DJ App without parameters.
Show all students.  
Verify that all students including two newly added are displayed. 


### Start without opening storage 

Start DJ App with one parameter as path to storage.
Verify that message about new file creation is displayed.  

Add new student with details.  
Show all students.  
Verify that added student is displayed.

Show details for added student.  
Verify that name, marks as empty string and details are displayed.  

Quit the app.

Start DJ App with one parameter as path to the same storage.  
Show all students.  
Verify that added student is displayed.

### Invalid number of parameters during start
Start DJ App with one parameter as path to storage.  
Verify that message about valid number of parameters is displayed.
