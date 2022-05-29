# import modules
from tkinter import *
import hashlib
import random
import pyperclip

# Generate random password for registering
def generate_random_password(length):
    letters = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*?"
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    # print("Random string of length", length, "is:", result_str)

# encrypt with md5 the text to store in database
def encrypt_md5(text):
    hash_object = hashlib.md5(text.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


# Designing window for registration
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Management")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry

    username = StringVar()

    Label(register_screen, text="Please enter username", bg="pink").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Generate Pass", width=10, height=1, bg="pink", command=register_user).pack()

# Implementing event on register button
def register_user():
    username_info = username.get()
    # password length has to be 8 ->req
    password_info = generate_random_password(8)

    if not username_info.isalpha():
        register_error_alpha()
    else:
        file = open('database.txt', "a")  # append to file
        username_encrypted = encrypt_md5(username_info)
        password_encrypted = encrypt_md5(password_info)
        file.write(username_encrypted)
        file.write("\n")
        file.write(password_encrypted)
        file.write("\n")
        pyperclip.copy(password_info)
        file.close()

        username_entry.delete(0, END)

        Label(register_screen, text="Registration Success for:", fg="green", font=("calibri", 11)).pack()
        Label(register_screen, text=username_info, fg="green", font=("calibri", 11)).pack()
        Label(register_screen, text=password_info, fg="green", font=("calibri", 11)).pack()
        Label(register_screen, text="\n", fg="green", font=("calibri", 11)).pack()

# Designing window for login
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login:").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


# def read_database(filename):
#     res = []
#     for line in open(filename, "r"):
#         data = line.strip("\n")
#         res.append(data)


def get_row_number_username_from_file(username_encrypted, password_encrypted):
    file = open('database.txt', "r")
    res = []
    # get values into array
    for line in file:
        data = line.strip('\n')
        res.append(data)

    if len(res) == 2: #only one username
        if (res[0] == username_encrypted) & (res[1] == password_encrypted):
            return 1
        else:
            return 0

    for count, elem in enumerate(res):
        if count % 2 == 0:  #go through usernames
            if elem == username_encrypted: # if matching
                if res[count+1] == password_encrypted: # if matching password
                    return count # return position; be advised that count starts at 0 and row in page starts at 1 => actual position is count+1;
    return 0 # if not returned till now, user not found


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    username1_encrypted = encrypt_md5(username1)
    password1_encrypted = encrypt_md5(password1)

    # print("username encrypted:", username1_encrypted)

    found_username_at_row = get_row_number_username_from_file(username1_encrypted, password1_encrypted) #here
    if found_username_at_row != 0:  # we found the username at a position/row
        print("found at position/row: ")
        print(found_username_at_row)
        login_sucess()   #change here, to change password
    else:
        print("not found, returned: ")
        print(found_username_at_row)
        password_not_recognised()
#
# def get_file(file):
#     result = ""
#     for line in file:
#         result += line
#     return result

def new_password_not_matching():
    global new_password_not_matching_screen
    new_password_not_matching_screen = Toplevel(login_success_screen)
    new_password_not_matching_screen.title("Failed")
    new_password_not_matching_screen.geometry("250x100")
    Label(new_password_not_matching_screen, text="New Password NOT Matching ").pack()
    Button(new_password_not_matching_screen, text="OK", command=delete_new_password_not_matching).pack()

def write_into_file(text_array):
    fout = open('database.txt', 'w')

    for line in text_array:
        fout.write(line)
        fout.write('\n')
    fout.close()

def change_password_funct(username2_encrypted, old_password2_encrypted, new_password2_encrypted):
    file = open('database.txt', "r")
    res = []
    result = []
    found = 0
    exit_with = 0
    # get values into array
    for line in file:
        data = line.strip('\n')
        res.append(data)

    for count, elem in enumerate(res):
        if count % 2 == 0:  # go through usernames
            if elem == username2_encrypted: # if username matching found = 1
                found = 1
            else:
                found = 0
            change_pass_with = elem
        else:
            if (elem == old_password2_encrypted) & (found == 1): # if password matches and the username was found
                change_pass_with = new_password2_encrypted
                exit_with = count
            else:
                change_pass_with = elem
        result.append(change_pass_with)
        print(result)

    write_into_file(result)
    return exit_with

def change_password():
    username2 = username_n_verify.get()
    old_password2 = old_password_verify.get()
    new_password2 = new_password_verify.get()
    confirm_new_password2 = confirm_password_verify.get()

    username_change_pass_entry.delete(0, END)
    old_password_change_pass_entry.delete(0, END)
    new_password_change_pass_entry.delete(0, END)
    confirm_password_change_pass_entry.delete(0, END)

    username2_encrypted = encrypt_md5(username2)
    old_password2_encrypted = encrypt_md5(old_password2)
    new_password2_encrypted = encrypt_md5(new_password2)
    confirm_new_password2_encrypted = encrypt_md5(confirm_new_password2)

    if new_password2_encrypted != confirm_new_password2_encrypted:
        new_password_not_matching()
    else:
        row = change_password_funct(username2_encrypted, old_password2_encrypted, new_password2_encrypted)
        if row != 0:  # we found the username at a position/row
            print("found at position/row: ")
            print(row)
            changed_password_success()  # here make another window to print changed password success
        else:
            print("not found, returned: ")
            print(row)
            password_not_recognised()

# # # Designing popup for changed password success
def changed_password_success():
    global changed_password_success_screen
    changed_password_success_screen = Toplevel(login_screen)
    changed_password_success_screen.title("Success")
    changed_password_success_screen.geometry("250x100")    # width, length
    Label(changed_password_success_screen, text="\n").pack()
    Label(changed_password_success_screen, text="Changed Password Successfully", fg="green").pack()
    Button(changed_password_success_screen, text="OK", command=delete_changed_password_success).pack()   #DELETE SCREEN HERE


# Designing popup for login success
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("250x400")
    Label(login_success_screen, text="Login Success", fg="green").pack()
    Label(login_success_screen, text="\n").pack()
    Label(login_success_screen, text="New password must be created: ", fg="red").pack()
    # Button(login_success_screen, text="OK", command=delete_login_success).pack()

    global username_n_verify
    global old_password_verify
    global new_password_verify
    global confirm_password_verify

    username_n_verify = StringVar()
    old_password_verify = StringVar()
    new_password_verify = StringVar()
    confirm_password_verify = StringVar()

    global username_change_pass_entry
    global old_password_change_pass_entry
    global new_password_change_pass_entry
    global confirm_password_change_pass_entry

    Label(login_success_screen, text="Username * ").pack()
    username_change_pass_entry = Entry(login_success_screen, textvariable=username_n_verify)
    username_change_pass_entry.pack()
    Label(login_success_screen, text="").pack()
    Label(login_success_screen, text="Old Password * ").pack()
    old_password_change_pass_entry = Entry(login_success_screen, textvariable=old_password_verify, show='*')
    old_password_change_pass_entry.pack()
    Label(login_success_screen, text="").pack()
    Label(login_success_screen, text="New Password * ").pack()
    new_password_change_pass_entry = Entry(login_success_screen, textvariable=new_password_verify, show='*')
    new_password_change_pass_entry.pack()
    Label(login_success_screen, text="").pack()
    Label(login_success_screen, text="Confirm Password * ").pack()
    confirm_password_change_pass_entry = Entry(login_success_screen, textvariable=confirm_password_verify, show='*')
    confirm_password_change_pass_entry.pack()
    Label(login_success_screen, text="").pack()
    Button(login_success_screen, text="Change Pass", width=10, height=1, command=change_password).pack()

# Designing popup for login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Failed")
    password_not_recog_screen.geometry("150x100")
    # Label(password_not_recog_screen, text="\n").pack()
    Label(password_not_recog_screen, text="User or password invalid", fg="red").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Designing popup for register username fail / invalid register name, not alphanumeric characters
def register_error_alpha():
    global register_error_alpha_screen
    register_error_alpha_screen = Toplevel(register_screen)
    register_error_alpha_screen.title("Success")
    register_error_alpha_screen.geometry("300x100")
    Label(register_error_alpha_screen, text="Invalid Username, has to be alphanumeric ", fg="red").pack()
    Button(register_error_alpha_screen, text="OK", command=delete_register_error_alpha_screen).pack()


# Deleting popups
def delete_login_success():
    login_success_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

def delete_register_error_alpha_screen():
    register_error_alpha_screen.destroy()

def delete_changed_password_success():
    changed_password_success_screen.destroy()

def delete_new_password_not_matching():
    new_password_not_matching_screen.destroy()

# Designing Main(first) window
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="pink", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Management", height="2", width="30", command=register).pack()

    main_screen.mainloop()


main_account_screen()