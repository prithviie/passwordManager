# Password Manager using SQLITE3 in C++ and Python

## About the Project
This is a simple Password Manager implemented using a Database Management library *sqlite3*. The Password Manager creates a database to store all the user passwords. The Password Manager requires a master password to open the application, which will be set by the user during the initial setup.

## File Description
- [password_manager.cpp](https://github.com/prithviie/password-mngr-cpp-py/blob/master/password_manager.cpp): Requirements: **sqlite3**
  - Click [here](https://www.sqlite.org/2021/sqlite-amalgamation-3340100.zip) to download sqlite.
  - Unzip the downloaded file and add **sqlite3.h** and **sqlite3.c** as the source files of your project
(or place them in the same directory as *password_manager.cpp*).
  - Run *password_manager.cpp* to generate a new database in the same directory as this file to save your passwords.

- [password_manager.py](https://github.com/prithviie/password-mngr-cpp-py/blob/master/password_manager.py): Run this file to start the Password Manager. Creates a folder to save your passwords in a database.
