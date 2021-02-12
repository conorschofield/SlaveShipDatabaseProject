# 400Project
 Connecting Heroes to my History DB

## Note that, as it currently sits, you need MySQL on your machine.
The code currently points to a local MySQL server.
To populate your local MySQL with data from the excel files, you will need to run multi-sheet.py:
$ python3 multi-sheet.py

To clear your DB, run:
python3  hist_drop.sql

To recreate your DB before population:
python3 create.sql

## Running the backend (local)
change directory to flask_backend
run the command:
 $ python3 main.py

## Running the frontend (local)
Go to angular-tour-of-heroes (awful name, I know. I did the Angular Tour of Heroes walkthrough to learn Angular and then modified the project to make it fit my needs. I never changed the file names). 

In the root directory of angular-tour-of-heroes, run the command:
$ ng serve

A webpage should open at port 4200 (http://localhost:4200)
I highly suggest you open this in Chrome. Chrome has excellent dev tools that make viewing/editing HTML a breeze right on the browser.

Happy Coding!
