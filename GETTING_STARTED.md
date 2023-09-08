# Getting started with the project

## Useful Tools / Tips

- DBeaver database administration tool: https://dbeaver.io/
- If at any point you want to re-start importing and such, run `DROP DATABASE SeniorProject;`
    - This will delete ALL imported data in the SQL database. So only do this if you're just trying to import and haven't made any other important changes directly to the database

## 1. Setting up MySQL

- [Install MySQL on your local machine](https://www.prisma.io/dataguide/mysql/setting-up-a-local-mysql-database)
    - Make sure to set the root password to `SeniorProject2021`
- Open the "MySQL 8.0 Command Line Client" from the start menu (or the equivalent on your OS)
- Log in with the root password `SeniorProject2021` as previously configured
- Type `source <create.sql>`, but using the full file path of create.sql from the root of the filesystem. It should look something like this:
    ```
    mysql> source <FILE>
    Query OK, 1 row affected (0.01 sec)

    Database changed
    Query OK, 0 rows affected (0.02 sec)

    Query OK, 0 rows affected (0.01 sec)

    Query OK, 0 rows affected (0.04 sec)

    Query OK, 0 rows affected (0.02 sec)

    Query OK, 0 rows affected (0.04 sec)

    Query OK, 0 rows affected (0.03 sec)

    Query OK, 0 rows affected (0.02 sec)

    Query OK, 0 rows affected (0.03 sec)

    Query OK, 0 rows affected (0.04 sec)

    mysql>
    ```


## 2. Importing the data into the database

Now, we are ready to start the data import.

- Make sure you have Python 3 and the Pip dependency manager installed. Python 3 can be easily installed on Windows from the Microsoft Store.
- Run the following command: `pip3 install --user mysql-connector-python openpyxl`
- Change your directory to the `excel-import` directory.
- Run `python3 betterimport.py`
- It should import all the data, and display that there were zero errors.

# Starting the backend

- Change your directory to `react-server`
- Install Node.js (LTS version): https://nodejs.org/en/
- Run `npm install`
- Run `npx nodemon index.js`
    - If it prompts you to install nodemon, accept the prompt.
- Make sure the database is running locally - otherwise the web app will fail
    - The reporting isn't great here - this will be worked on

# Starting the frontend

- Change your directory to `react-sql`
- Install Yarn: `npm install --global yarn`
- Run `yarn install`
- Run `yarn start`
- Connect to `localhost:3000`
