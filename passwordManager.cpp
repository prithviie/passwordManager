#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "sqlite3.h"
using namespace std;

// main passwd manager file to run the password manager

string values[2];

bool create_db(const char *db_filepath)
{
    // create a database file at given path, if it doesn't exist
    sqlite3 *db;
    int exit = sqlite3_open(db_filepath, &db);
    if (exit != SQLITE_OK)
    {
        cerr << "Error creating database" << endl;
        sqlite3_free(db);
        return false;
    }
    else
    {
        // cout << "Database created succesfully" << endl;
        sqlite3_close(db);
        return true;
    }
}

bool create_table(const char *db_filepath)
{
    // creating a table - Passwords - with two columns - service and password
    sqlite3 *db;

    string execute =
        "DROP TABLE IF EXISTS Passwords;"
        "CREATE TABLE Passwords("
        "service TEXT NOT NULL,"
        "password TEXT NOT NULL"
        ");";
    int exit = 0;
    try
    {
        exit = 0;
        exit = sqlite3_open(db_filepath, &db);
        char *messageError;
        exit = sqlite3_exec(db, execute.c_str(), NULL, 0, &messageError);

        if (exit != SQLITE_OK)
        {
            cerr << "Error Create Table" << endl;
            sqlite3_free(db);
            return false;
        }
        else
        {
            // cout << "Table created succesfully" << endl;
            sqlite3_close(db);
            return true;
        }
        sqlite3_close(db);
    }

    catch (const exception &e)
    {
        cerr << e.what();
    }
}

bool check_length(char arr[], int min_length)
{
    // checks if the input char array has length > min_length
    int i = 0;
    while (arr[i] != '\0')
    {
        i++;
    }
    if (i < min_length)
    {
        return false;
    }
    return true;
}

string add_service()
{
    // promts the user to enter service name and return the service name
    char service_name[30];

    cout << "Enter the service name: ";
    cin >> service_name;

    return string(service_name);
}

string add_password()
{
    // promts the user to enter password and returns the password
    char password[30];

    cout << "Enter password: ";
    cin >> password;

    if (!check_length(password, 8))
    {
        cout << "Password too short (use at-least 8 characters long) " << endl;
        string ans = add_password();
    }
    else
    {
        return string(password);
    }
}

int callback(void *NotUsed, int argc, char **argv, char **azColName)
{
    // to retrieve queried items
    for (int i = 0; i < argc; i++)
    {
        // cout << azColName[i] << ": " << argv[i] << endl;
        cout << argv[i] << endl;
    }
    return 0;
}

bool add_service_passwd(string service_name, string passwd, const char *db_filepath)
{
    // Inserting into the database - credentials - service and password
    const char *path = db_filepath;
    sqlite3 *db;
    char *messageError;

    int exit = sqlite3_open(db_filepath, &db);

    string execute = "INSERT OR IGNORE INTO Passwords (service, password) VALUES ('" + service_name + "', '" + passwd + "');";

    exit = sqlite3_exec(db, execute.c_str(), NULL, 0, &messageError);

    if (exit != SQLITE_OK)
    {
        cerr << "Error insert" << endl;
        sqlite3_free(db);
        return false;
    }
    else
    {
        // cout << "Record created succesfully" << endl;
        sqlite3_close(db);
        return true;
    }
    sqlite3_close(db);
}

int get_passwd_by_service_name(string service_name, const char *db_filepath)
{
    // get password for a given service name
    sqlite3 *db;
    int exit = sqlite3_open(db_filepath, &db);
    string execute = "SELECT password FROM Passwords WHERE service = '" + service_name + "';";

    try
    {
        sqlite3_exec(db, execute.c_str(), callback, NULL, NULL);
    }
    catch (...)
    {
        cout << "No such service exists" << endl;
        sqlite3_close(db);
    }

    return 0;
}

int show_services(const char *db_filepath)
{
    // prints all the added services
    sqlite3 *db;
    int exit = sqlite3_open(db_filepath, &db);
    string execute = "SELECT service FROM Passwords WHERE service != 'master'";

    try
    {
        sqlite3_exec(db, execute.c_str(), callback, NULL, NULL);
    }
    catch (...)
    {
        cout << "No services are added" << endl;
        sqlite3_close(db);
    }

    return 0;
}

bool update_data(string service, string new_pass, const char *db_file)
{
    // update password for a service name
    sqlite3 *db;
    char *messageError;

    int exit = sqlite3_open(db_file, &db);
    string execute = "UPDATE Passwords SET password = '" + new_pass + "' WHERE service = '" + service + "';";

    exit = sqlite3_exec(db, execute.c_str(), NULL, 0, &messageError);

    if (exit != SQLITE_OK)
    {
        cerr << "Error insert" << endl;
        sqlite3_free(db);
        return false;
    }
    else
    {
        // cout << "records updated succesfully" << endl;
        return true;
    }

    sqlite3_close(db);
    return false;
}

bool delete_data(string service, const char *db_file)
{
    // delete the data for a given service name
    sqlite3 *db;

    int exit = sqlite3_open(db_file, &db);
    string execute = "DELETE FROM Passwords WHERE service = '" + service + "';";

    try
    {
        sqlite3_exec(db, execute.c_str(), callback, NULL, NULL);
        return true;
    }
    catch (...)
    {
        cout << "No such service data" << endl;
        sqlite3_close(db);
        return false;
    }
    return false;
}

void set_master_pw(const char *path)
{
    // set master password if not set
    string service = "master";
    char master_pw[30];

    cout << "Set Master password: ";
    cin >> master_pw;

    if (!check_length(master_pw, 8))
    {
        cout << "Password too short (use at-least 8 characters long) " << endl;
        set_master_pw(path);
    }

    bool ok = add_service_passwd(service, string(master_pw), path);
    if (ok)
    {
        cout << "Master password set." << endl;
    }
}

int callback2(void *NotUsed, int argc, char **argv, char **azColName)
{
    for (int i = 0; i < argc; i++)
    {
        // cout << azColName[i] << ": " << argv[i] << endl;
        values[i] = argv[i];
        // cout << argv[i] << endl;
    }
    return 0;
}

bool verify_master_pw_for_login(const char *db_filepath)
{
    // verification to open the main password manager using the master password
    char input[30];
    cout << "Enter Master password to login: ";
    cin >> input;

    sqlite3 *db;
    int exit = sqlite3_open(db_filepath, &db);
    string execute = "SELECT password FROM Passwords WHERE service = 'master';";

    sqlite3_exec(db, execute.c_str(), callback2, NULL, NULL);

    int len = values[0].length();

    char char_arr[len + 1];
    strcpy(char_arr, values[0].c_str());

    if (strcmp(char_arr, input) == 0)
    {
        return true;
    }
    return false;
}

bool prompt(const char *path)
{
    // prompting for various options
    char input;

    cout << endl;
    cout << "********************** Choose any *************************" << endl;
    cout << "  1. Add service:                                  1 or a" << endl;
    cout << "  2. Get password for a service:                   2 or p" << endl;
    cout << "  3. Show added services:                          3 or s" << endl;
    cout << "  4. Update password for a service:                4 or u" << endl;
    cout << "  5. Remove a service data:                        5 or r" << endl;
    cout << "  6. Reset Master password:                        6 or m" << endl;
    cout << "  7. Quit:                                         7 or q" << endl;
    cout << "***********************************************************" << endl;
    cout << endl;
    cout << "Enter choice: ";

    cin >> input;

    if (input == '1' || input == 'a')
    {
        // add new service data
        string service_name = add_service();
        string password = add_password();

        cout << service_name << endl;
        cout << password << endl;

        bool ok = add_service_passwd(service_name, password, path);
        if (ok)
        {
            cout << "Service data added." << endl;
        }

        return true;
    }

    else if (input == '2' || input == 'p')
    {
        // get password for a service
        string service_name;
        show_services(path);
        cout << "Enter service name: ";
        cin >> service_name;

        get_passwd_by_service_name(service_name, path);

        return true;
    }

    else if (input == '3' || input == 's')
    {
        // show added services
        show_services(path);
        return true;
    }

    else if (input == '4' || input == 'u')
    {
        // update password for a service
        show_services(path);
        string service_name = add_service();
        string new_pass = add_password();

        bool ok = update_data(service_name, new_pass, path);
        if (ok)
        {
            cout << "Service data updated." << endl;
        }

        return true;
    }

    else if (input == '5' || input == 'r')
    {
        // remove a service data
        show_services(path);
        string service_name = add_service();

        bool ok = delete_data(service_name, path);
        if (ok)
        {
            cout << "Service data removed." << endl;
        }

        return true;
    }

    else if (input == '6' || input == 'm')
    {
        //reset master password
        char input[30];
        cout << "Enter the Master password: ";
        cin >> input;

        sqlite3 *db;
        int exit = sqlite3_open(path, &db);
        string execute = "SELECT password FROM Passwords WHERE service = 'master';";

        sqlite3_exec(db, execute.c_str(), callback2, NULL, NULL);

        int len = values[0].length();

        char char_arr[len + 1];
        strcpy(char_arr, values[0].c_str());

        bool verified = false;

        if (strcmp(char_arr, input) == 0)
        {
            verified = true;
        }

        if (verified)
        {
            string new_pass = add_password();

            bool ok = update_data("master", new_pass, path);
            if (ok)
            {
                cout << "Master password updated." << endl;
            }
        }
        else
        {
            cout << "Incorrect password" << endl;
        }

        return true;
    }

    else if (input == '7' || input == 'q')
    {
        return false;
    }
}

int main()
{
    const char *path = "passes.db";

    FILE *file;
    if (file = fopen(path, "r"))
    {
        fclose(file);
    }
    else
    {
        create_db(path);
        create_table(path);
        set_master_pw(path);
    }

    bool run = verify_master_pw_for_login(path);
    if (!run)
    {
        cout << "Wrong password" << endl;
    }

    while (run)
    {
        run = prompt(path);
    }

    return 0;
}
