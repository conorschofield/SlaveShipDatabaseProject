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
change directory to react-server
run the command:
 $ npx nodemon index.js

## Running the frontend (local)
change directory to react-sql
run the command:
$ yarn start

A webpage should open at port 3000 (http://localhost:3000)
I highly suggest you open this in Chrome. Chrome has excellent dev tools that make viewing/editing HTML a breeze right on the browser.

Happy Coding!
