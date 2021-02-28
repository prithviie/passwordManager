import re
import os
import getpass
import sqlite3
from time import sleep


def description():
    '''Greeting stuff for the user, printed only first time'''

    confirm = open_file()
    if confirm:
        print('Greetings!\nDescription:\nThis is a simple Password Manager where you can save your passwords for various online/offline accounts.\nAll you have to do is set up a Master Password for this application and once done you are good to go.\nYou can add as many services as you like (eg. Google, Instagram, etc).\nYour passwords are encrypted and safe on your computer.\nAll you have to remember is your Master Password.\nAnytime you need a password for a service, you can log into the Password Manager using the Master Password, and ask for the password for a particular service.\nYou have several options available that you can use:\nYou can add a service, update the password for a service, remove the data for a service, etc. You can also reset your Master Password.\nResetting your Master Password does not delete your data.\nCheers!')
        print()


def open_file():
    '''Opens a file and a folder to save all details, if file exists no new file is created'''
    # in append mode
    if not os.path.isfile(dbfile):
        os.mkdir(path)
        con = sqlite3.connect(dbfile)
        cursor = con.cursor()

        cursor.executescript('''DROP TABLE IF EXISTS Details;

        CREATE TABLE Details(
            ref TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL
        );''')

        # for README file
        create_readme_file()
        return True

    else:
        return False


def create_readme_file():
    '''Creates a README file in the folder'''
    with open(rfile, 'w+') as fh:
        fh.write("This folder is created to save your passwords.\n"
                 "Do not tamper with the files in this folder or else you could lose your passwords.\n")


def clear():
    ''' to clear the terminal screen'''
    g = os.system('cls')


def encrypt(text):
    '''Given a string, returns an encrypted string'''

    text = str(text)
    key = 15
    rval1 = 7
    rval2 = 5
    s = ''
    for ch in text:
        asci_val = ord(ch)
        inc1 = abs(asci_val - key)
        inc2 = abs(asci_val + key)
        inc3 = abs(asci_val - key - rval1)
        inc4 = abs(asci_val + key + rval2)

        if inc1 <= 32:
            inc1 = 32
        if inc2 >= 126:
            inc2 = 126
        if inc3 <= 32:
            inc3 = 32
        if inc4 >= 126:
            inc4 = 126

        # print(inc1, inc2, inc3, inc4, ch)
        # print(chr(inc1), chr(inc2), chr(inc3), chr(inc4), ch)

        cha = chr(inc1) + chr(inc2) + chr(inc3) + chr(inc4)
        s += cha

    # print(s)
    # print(len(s))
    return s


def decrypt(text):
    '''Given an encrypted string, returns a decrypted string'''

    text = str(text)

    def get_ascii_value_from_part(part):
        '''private method for decryption method
        returns the ascii value of string from from characters'''
        key = 15
        rval1 = 7
        rval2 = 5

        inc1 = ord(part[0])  # =  asci_val - 7
        inc2 = ord(part[1])  # =  asci_val + 7
        inc3 = ord(part[2])  # =  asci_val - 7 - 5
        inc4 = ord(part[3])  # =  asci_val + 7 + 5

        asci_val1 = inc1 + key
        asci_val2 = inc2 - key
        asci_val3 = inc3 + key + rval1
        asci_val4 = inc4 - key - rval2

        if asci_val1 == asci_val2 == asci_val3 == asci_val4:
            return asci_val1
        else:
            if inc1 == 32:
                return asci_val2
            elif inc2 == 126:
                return asci_val1
            elif inc3 == 32:
                return asci_val4
            elif inc4 == 126:
                return asci_val3

    length = len(text)
    s = ''
    for i in range(0, int(length / 4)):
        part = text[:4]
        asci_val_of_char = get_ascii_value_from_part(part)
        s += chr(asci_val_of_char)
        text = text[4:]
        # print(text)
    # print(s)
    return s


def add_ref_content(ref, content):
    try:
        con = sqlite3.connect(dbfile)
        cursor = con.cursor()
        # cursor.execute('INSERT INTO Details (ref, content) VALUES (?, ? )', (ref, content))
        cursor.execute('INSERT OR IGNORE INTO Details (ref, content) VALUES (?, ? )',
                       (ref, encrypt(encrypt(content))))
        con.commit()
        return True
    except Exception as error:
        return False


def get_content_by_ref(ref):
    try:
        con = sqlite3.connect(dbfile)
        cursor = con.cursor()
        cursor.execute('SELECT content FROM Details WHERE ref = ?', (ref,))
        ans = cursor.fetchone()[0]
        # return ans
        return decrypt(decrypt(ans))
    except:
        message = "The given service name is not in the list"
        return message


def check_if_ref_exists(ref):
    '''Returns true if ref exists in refs, else False'''
    con = sqlite3.connect(dbfile)
    cursor = con.cursor()

    cursor.execute('SELECT * FROM Details')
    refs = cursor.fetchall()
    for item in refs:
        if ref == item[0]:
            return True

    return False


def add_service():
    '''Lets the user to add a new service data only if the service name does not exist'''
    # prompting the user to add proper names
    service_name = input('Service name: ').lower()
    if len(service_name) > 1:
        proceed = check_if_ref_exists(service_name)
        if proceed is False:
            try:
                add_ref_content(service_name, add_password(service_name))
            except:
                print('The given service data already exists')

        else:
            print('The given service data already exists')

    else:
        print('Enter a service name')


def add_password(ref):
    ''' To add password for a given service name(ref) '''

    # prompting twice to confirm password
    while True:
        print(' ')
        print("You can use pins as passwords too using the 'pin' keyword before your pin. Eg - 'pin 1234'.")
        pw = getpass.getpass(prompt="Enter password/pin: ").strip()
        if pw.startswith('pin'):
            if len(pw) <= 3:
                print('Enter a pin')
                break
            idx = pw.index('n')
            pw = pw[idx + 1:]
            # print(pw)
            passwd = re.findall('[0-9A-Za-z].+', pw)[0]
            # print(passwd)
            if len(passwd) < 4:
                print('Pin too short. Use at least 4 characters.')
                print(' ')
            else:
                pw2 = getpass.getpass(
                    prompt="Re-enter the pin without the 'pin' keyword: ").strip()
                passwd2 = re.findall('[0-9A-Za-z].+', pw2)[0]
                if passwd2 == passwd:
                    print("Saved")
                    return passwd
                else:
                    print("Pins do not match")
                    break

        else:
            if len(pw) < 8:
                print('Set a stronger password (at least 8 characters long)')
                print(' ')
            else:
                pw2 = getpass.getpass(prompt='Re-type password: ')
                if pw == pw2:
                    print('Saved')
                    return pw
                else:
                    print('Passwords do not match')
                    break


def show_services():
    '''To print all the previously saved services, returns True if refs exist else False'''
    con = sqlite3.connect(dbfile)
    cursor = con.cursor()
    # if any more refs/contents to be added then change the conditions here
    cursor.execute('SELECT * FROM Details WHERE ref != ?', ('maspw',))
    refs = cursor.fetchall()

    final_refs = list()

    for ref in refs:
        final_refs.append(ref[0])

    if len(final_refs) < 1:
        print('No services are added')
        return False

    else:
        # printing services for the user
        print('Services:', end=' ')
        print(*final_refs, sep=', ')
        print(' ')
        return True


def remove_service(ref):
    '''Lets the user to remove any service data after entering the master pw'''

    proceed = check_if_ref_exists(ref)
    if proceed is True:
        # prompting the user to input the master pw to remove any service data
        maspw = getpass.getpass(prompt='Enter Master password: ')
        # if correct then

        if maspw == get_content_by_ref('maspw'):

            con = sqlite3.connect(dbfile)
            cursor = con.cursor()
            cursor.execute('DELETE FROM Details WHERE ref = ?', (ref,))
            con.commit()

            print(ref + ' service data removed')

        # if wrong
        else:
            print('Incorrect password')

    else:
        print('The given service name is not in the list')


def get_pw_for_service():
    service_name = input('Enter service name: ').lower()

    # if any more refs/contents to be added then change the conditions here
    if service_name == 'maspw':
        print('The given service name is not in the list')

    elif len(service_name) > 1:
        res = get_content_by_ref(service_name)
        if res is not None:
            print(res)
    else:
        print('The given service name is not in the list')


def update_pw(ref, new_pw):
    try:
        con = sqlite3.connect(dbfile)
        cursor = con.cursor()
        cursor.execute('UPDATE Details SET content = (?) WHERE ref = (?)',
                       (encrypt(encrypt(new_pw)), ref))
        con.commit()

    except:
        print('Update unsuccessful')


def update_pw_initiate():
    ref = input('Enter the service name: ').lower()

    # if any more refs/contents to be added then change the conditions here
    if ref == 'maspw':
        print('The given service name is not in the list')

    elif len(ref) > 1:

        proceed = check_if_ref_exists(ref)
        if proceed is True:

            maspw = getpass.getpass(prompt='Enter Master password: ')
            if maspw == get_content_by_ref('maspw'):
                updated_pw = add_password(ref)
                update_pw(ref, updated_pw)

            else:
                print('Incorrect password')

        else:
            print('The given service name is not in the list')

    else:
        print('The given service name is not in the list')


def update_master_pw():
    '''Lets the user reset the Master pw'''

    proceed = check_if_ref_exists('maspw')
    if proceed is True:

        maspw = getpass.getpass(prompt='Enter current Master password: ')

        if maspw == get_content_by_ref('maspw'):

            con = sqlite3.connect(dbfile)
            cursor = con.cursor()
            cursor.execute('DELETE FROM Details WHERE ref = ?', ('maspw',))
            con.commit()

            set_master_pw()

        else:
            print('Incorrect password')

    else:
        print('Master password is not set')


def set_master_pw():
    ''' Asks the user to set the Master pw. if already set then does nothing'''

    # reading all refs to check if master pw is set
    proceed = check_if_ref_exists('maspw')
    # print(proceed)
    # if master pw is not set then:

    if proceed is False:
        while True:
            # inputting master pws
            # condition checking for length
            # checking twice to confirm master pw
            maspw = getpass.getpass(prompt='Set Master password: ')
            if len(maspw) < 8:
                print('Set a stronger password (at least 8 characters long)')
                continue
            else:
                maspw2 = getpass.getpass(prompt='Re-type Master password: ')
                if maspw == maspw2:
                    break
                else:
                    print('The passwords do not match')
                    continue
        add_ref_content('maspw', maspw)
        print('Master password set')
        print()

        return True
    else:
        return False


def enter_master_pw():
    '''Asking user to enter master pw to log in into the pw manager,
    returns True if pw entered is right, else False'''

    maspw = getpass.getpass(prompt='Enter Master password to login: ')
    if maspw == get_content_by_ref('maspw'):
        return True
    else:
        return False


def prompt_options():
    '''Prompting the user to choose any options in the pw manager,
     accordingly this function calls another function to complete the tasks'''
    print()
    print('********************** Choose any *************************')
    print("1. Add service:                                  1 or a")
    print("2. Get password for a service:                   2 or p")
    print("3. Show added services:                          3 or s")
    print("4. Update password for a service:                4 or u")
    print("5. Remove a service data:                        5 or r")
    print("6. Reset Master password:                        6 or m")
    print("7. Quit:                                         7 or q")
    print('***********************************************************')
    print()
    prompt = input('Enter: ')

    # for adding a new service
    if prompt == '1' or prompt == 'a':
        add_service()
        return True

    # to get pw for a service
    elif prompt == '2' or prompt == 'p':
        further = show_services()
        if further:
            get_pw_for_service()
        return True

    # shows all the saved services
    elif prompt == '3' or prompt == 's':
        show_services()
        return True

    # update pw for a service
    elif prompt == '4' or prompt == 'u':
        further = show_services()
        if further:
            update_pw_initiate()
        return True

    # remove a service data
    elif prompt == '5' or prompt == 'r':
        further = show_services()
        if further:
            remove = input('Enter service name: ').lower()
            if not remove == 'maspw':
                remove_service(remove)
            else:
                print('The given service name is not in the list')

        return True

    # update master pw
    elif prompt == 'm' or prompt == '6':
        update_master_pw()
        return True

    # quit the manager
    elif prompt == 'q' or prompt == '7':
        print('Changes saved')
        sleep(1)
        clear()
        quit()

    # clear screen
    elif prompt == 'cls':
        clear()
        return False

    # if any other character except the specified ones are entered then call the same function
    else:
        prompt_options()
        return False


def main():
    # open a dbfile
    description()

    # set master pw
    set_master_pw()

    # enter master pw to login
    proceed = enter_master_pw()

    # if entered master pw is correct then:
    while True:
        if proceed:
            while True:
                wait = prompt_options()
                # send_mail_initiate()
                if wait:
                    sleep(1.5)

        # if entered master pw is incorrect
        else:
            print('Incorrect password')
            print()

            proceed = enter_master_pw()
            continue


path = './Pass/'
dbfile = path + '/queries.sqlite'
rfile = path + '/README.txt'

main()
