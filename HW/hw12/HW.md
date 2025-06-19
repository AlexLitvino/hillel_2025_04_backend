You client came to you and asked to mark orders as archived if they are already finished for 10 seconds.

P.S. The task from client is based on the project from lesson 13 (placed in `main.py` on github)
P.P.S. This homework does not have other details. You can discuss them either in private or in Telegram Group with other students.

# COMMENTS:
- I see your point when you change the data structure from list to tuple in your _archive() function

    - but I WOULDN'T recommend that in general

    - making this structure POLIMORPHIC from the complexity point of view is more DANGEROUS than you think 😄 

    - what if you would like to UNARCHIVE your delivery order in some day amd mark as DELETED (another yet status)

    - remember that STORAGE nowadays is THE CHEAPEST RESOURCE that we can use, so no worries if list takes too much
