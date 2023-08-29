# =====importing libraries===========
# '''This is the section where you will import libraries'''
import datetime
import time


def get_userinfo():
    """
    This function opens a text file to read the usernames and corresponding passwords.
    The information is then stored in a dictionary.
    :return: login_info
    """
    with open("user.txt", "r", encoding='utf-8-sig') as user_info:
        # Dict    =  {key                : value               looping over file line for key & value}}
        login_info = {user.split(", ")[0]: user.split(", ")[1] for user in user_info.read().splitlines()}

        return login_info


def get_task_info():
    """
    This function reads tasks of users stored in a text file and store them in a 2_D list.
    :return: user_task_info
    """
    with open("tasks.txt", "r", encoding='utf-8-sig') as all_task_info:
        # List         = [    item              looping over file for each item]
        user_task_info = [user_task.split(", ") for user_task in all_task_info.read().splitlines()]

        return user_task_info


def is_yes_no(yes_no):
    """
    This function checks if a string input is either a 'yes' or 'no'.
    The continues to run until one of the options above is true.
    :param yes_no:
    :return: yes_no
    """
    while True:
        if yes_no not in ["yes", "no"]:
            yes_no = input(f"\nIncorrect input: {yes_no} \nPlease enter either 'Yes' or 'No'")
        else:
            break
    return yes_no  # If yes_no is either 'yes' or 'no' then return yes_no as is


def is_valid_user(test_user, log_det):
    """
    This function checks if a username to be added is valid according to the rules below.
    :param test_user:
    :param log_det:
    :return: msg, user_passed
    """
    msg = ""
    user_passed = False
    allow_special = ["@", "."]  # These are the only 2 special characters allowed in making a username
    if test_user in log_det:
        msg = "This username already exist."  # Prevents duplication of usernames
    elif " " in test_user:
        msg = "Username must not contain spaces!"  # Space character cannot be in a username string
    elif test_user == "":
        msg = "Username is empty."  # A username cannot be an empty or null string
    elif len(test_user) < 4:
        msg = "Username must be at least 4 characters long."  # Minimum length of username is 4 characters
    elif len(test_user) > 25:
        msg = "Username must not be more than 25 characters long."  # Maximum length of a username is 25 characters
    elif any((char not in allow_special and not char.isalnum()) for char in test_user):
        msg = f"Username can only have the following special characters:\n {allow_special}"
    else:
        user_passed = True

    return msg, user_passed


def is_valid_pass(test_pass):
    """
    This function checks if a password is valid according to the rules below.
    :param test_pass:
    :return: msg, password_passed
    """
    msg = ""
    password_passed = False
    allow_special = "!@#$%&*-+=|/\\?"  # Allowed special characters for passwords
    if " " in test_pass:
        msg = "Password must not contain spaces!"
    elif test_pass.isnumeric():
        msg = "Password must not contain numbers only"
    elif test_pass == "":
        msg = "Password is empty"
    elif len(test_pass) < 4:
        msg = "Password must be at least 4 characters long."
    elif len(test_pass) > 15:
        msg = "Password must not be more than 15 characters long."
    elif any((char not in allow_special and not char.isalnum()) for char in test_pass):
        msg = f"Password can only have the following special characters:\n {allow_special}"
    else:
        password_passed = True

    return msg, password_passed


def is_leap_year(any_year):
    # Leap year code below adopted from L1T13 task 2 by Fortune Ncube 09 January 2023

    if (any_year % 400 == 0) or (
            any_year % 100 != 0 and any_year % 4 == 0):  # Check leap year conditions
        return True
    else:
        return False


def paragraphing(long_str, len_limit):
    """
    This function takes in an iterable (list, string, etc) and breaks it into a paragraph based on the
    maximum sentence length `len_limit`
    The returned sentence is in multiple lines.
    :param long_str:
    :param len_limit:
    :return: sentence
    """
    sub_length = len(long_str)  # Original length of each of a very long string > 'len_limit'
    if len(long_str) > len_limit:  # Indents text output if text length is longer than a constant 'max_len'
        start_index = 0
        end_index = len_limit
        sentence = []  # Initializing with an empty list

        # Splitting or de-concatenation of a very long string to a paragraph of sentences
        while sub_length > len_limit:  # Keeps indenting until length of last sub string < 'max_len'
            # Splitting string at nearest "space" character immediately before 'max_len'
            if long_str[end_index] == " ":
                # Appending the "next line" character at the end of each split sentence
                sentence.append(long_str[start_index:(end_index + 1)])

                start_index = end_index + 1  # Define new starting index for the next sentence
                sub_length = len(long_str) - start_index  # Reduce original length by the length of 'sentence'

                # Determine 'end_index' based on whether the remaining text length is < 'max_len'
                if sub_length > len_limit:
                    end_index = start_index + len_limit
                else:
                    end_index = len(long_str)
                    sentence.append(long_str[start_index:(end_index + 1)])
            else:
                end_index -= 1  # Decrement 'end_index' by 1 until character at 'end_index' is a "space"
    else:
        sentence = [long_str]  # Creating a singular element list

    return sentence  # The returned sentence is a list of paragraph sentences


def table_display(list_of_user, max_len):
    """
    This function prints to console expected data in table format.
    :param list_of_user:
    :param max_len:
    :return:
    """
    ordered_task = []
    task_details = get_task_info()
    for users_name in list_of_user:  # Creating a list of users with each item being a list of user tasks
        user_tasks = []

        # Grouping user task info based on username that tasks were assigned to
        for j_enum, tasks_info in enumerate(task_details):
            if tasks_info[0] == users_name:
                # Rearranging task columns
                user_tasks.append([tasks_info[3], tasks_info[4], tasks_info[1], tasks_info[5], tasks_info[2]])

        ordered_task.append(user_tasks)

    # Table headings in the order in which a table is created based on task.txt storage format
    table_head = ["Date assigned", "Due date", "Task", "Task Complete?", "Task description"]

    # Creating a list with maximum table column widths of each task info (Vertical Alignment of Table)
    table_col_width = []
    for t, table_heading in enumerate(table_head):
        table_col_width.append(len(table_head[t]))

    # Find the maximum table column widths of a table from all tasks
    for j_enum, users_name in enumerate(list_of_user):  # Iterating over each user from a list of users
        for i_enum, tasks_info in enumerate(ordered_task[j_enum]):  # Iterating over each task from a list of user tasks
            for k_enum, col in enumerate(table_head):  # Iterating over each task contents (Ass. Date, Due Date, Task,.)
                if tasks_info != "" and len(tasks_info[k_enum]) > table_col_width[k_enum]:

                    table_width = len(max(paragraphing(tasks_info[k_enum], max_len), key=len))
                    if table_width > table_col_width[k_enum]:
                        table_col_width[k_enum] = table_width

    vert_table_sep = " \u2502 "  # Character sequence for separating a table (vertical lines)

    # Maximum character length of horizontal line
    hor_line_len = sum(table_col_width) + len(vert_table_sep) * 5 - 1  # There are 5 vertical table lines

    rgb_colour1 = "\033[38;2;0;255;255m"
    rgb_colour2 = "\033[38;2;255;0;255m"
    white_colour = "\033[0m"

    # Creating a table for each user
    for j_enum, users_name in enumerate(list_of_user):  # Iterating over each user
        print(rgb_colour2 + f"\nTASKS ASSIGNED TO : {users_name}" + white_colour)
        print(rgb_colour1 + '_' * hor_line_len + white_colour)  # Print horizontal table line

        headings = []  # Populating table headings and formatting with space characters
        for t, col in enumerate(table_head):
            headings.append(table_head[t] + " " * (table_col_width[t] - len(table_head[t])) + vert_table_sep)

        print("".join(headings).upper())  # Print table headings
        print(rgb_colour1 + '_' * hor_line_len + white_colour)  # Print horizontal table line

        # Setting up each table column
        for i_enum, task_item in enumerate(ordered_task[j_enum]):  # Iterating over each task item of a user
            col_info = []
            for col_num, col in enumerate(table_head):  # Iterating over each table column
                col_info.append(paragraphing(task_item[col_num], max_len))

            max_sent_len = len(max(col_info, key=len))  # Length of the longest paragraph (Max No. of sentences)

            output_row_info = []  # List containing all rows of the output table for user's tasks
            # Setting up each table row with info for all columns in table
            for k_enum in range(0, max_sent_len):  # Populate rows equal to the number of sentences
                row_info = []  # List containing all rows of info for a singe user's task

                # Populate each row according to the order of columns
                for t, col in enumerate(table_head):
                    # Check if column is empty for any row and populate with spaces or column contents
                    if k_enum < len(col_info[t]) <= max_sent_len:  # column not empty (column info + spaces + separator)
                        each_sent = col_info[t][k_enum]
                        sent_str = each_sent + " " * (table_col_width[t] - len(each_sent)) + vert_table_sep
                        row_info.append(sent_str)
                    else:  # column is empty (spaces + separator)
                        row_info.append(" " * table_col_width[t] + vert_table_sep)

                output_row_info.append(row_info)

            # Printing all rows for a user's table
            for row_task in output_row_info:
                print(rgb_colour1 + "".join(row_task) + white_colour)


def list_display(users_tasks, max_len):
    """
    This function takes in data and prints in list format.
    :param users_tasks:
    :param max_len:
    :return:
    """
    table_head = ["Assigned to", "Task", "Task description", "Date assigned", "Due date", "Task Complete?"]
    table_order = [1, 0, 3, 4, 5, 2]
    long_space = len(max(table_head, key=len))  # The maximum length of
    const_space = 4

    free_space = long_space + const_space + 1
    split_at = "\n" + " " * (free_space - 1) + ":"  # Character sequence added between split sub-strings

    rgb_colour1 = "\033[38;2;0;255;255m"
    white_colour = "\033[0m"

    print(rgb_colour1 + "_" * (max_len + free_space) + white_colour)
    for j_enum, tasks_info in enumerate(users_tasks):  # Iterating over each task
        for i_enum in table_order:  # Iterating over each task item

            paragraph = split_at.join(paragraphing(tasks_info[i_enum], max_len))

            space = long_space - len(table_head[i_enum]) + const_space
            print(rgb_colour1 + f"{table_head[i_enum]}" + " " * space + ":" + paragraph + white_colour)

            # Referencing
            # Stake Overflow - How to print RGB colour to the terminal. Accessed on 09 January 2023 from
            # https://stackoverflow.com/questions/74589665/how-to-print-rgb-colour-to-the-terminal
        print(rgb_colour1 + "_" * (max_len + free_space) + white_colour)


def display_format(disp_my_tasks, disp_current_user, disp_sentence_len_limit):
    """
    This function takes sets of data and prints it in the required format.
    :param disp_my_tasks:
    :param disp_current_user:
    :param disp_sentence_len_limit:
    :return:
    """
    while True:
        display_method = input("Please choose '1' or '2' for a display format:"
                               "\n\t 1 : Lists Format"
                               "\n\t 2 : Tabular Format\n")

        if display_method == "1":
            list_display(disp_my_tasks, disp_sentence_len_limit)  # Display all tasks currently assigned to user
            break
        elif display_method == "2":
            table_display(disp_current_user, disp_sentence_len_limit)
            break
        else:
            print(f"{display_method} is out of range!\n")
            continue


# ====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''

login_trials = 3  # Limit number of login attempts for all incorrect login details
administrator = False
usercheck = ""  # The username used to check or validate the one stored in users.txt during login

# Welcome Message
print("\n|-|-|-|-|- Welcome to Task_Manager  -|-|-|-|-|\n")
print("|-|-|-|-|- Please proceed to login. -|-|-|-|-|\n")
# Requesting User to input and validating Username and Password.
while True:
    try:
        # If login_trials are exhausted, user must wait 10 seconds before trying again.
        # This is for security purposes.
        login_delay = 10  # Time to delay login by
        if login_trials == 0:
            print(f"\nYour access is blocked. Please try again after {str(login_delay)} seconds.")
            # Display a count-down timer
            for i in range(login_delay, -1, -1):
                time.sleep(1)
                print("", end=f"\rLogin In {str(i)}")
            print()

        print()
        usercheck = input("Please enter your login username: ")  # Getting Username input from user
        pass_check = input("Please enter your login password: ")  # Getting Password input from user

        login_details = get_userinfo()  # Calling function to retrieve all stored usernames and passwords
        # Check if username exists
        if usercheck in login_details:
            # Check if password corresponds to username
            if pass_check == login_details[usercheck]:
                # Checking if User is Administrator to give access to Admin rigs or deny if otherwise
                print("\nAccess granted to Task_Manager!!!")
                if list(login_details).index(usercheck) == 0:
                    administrator = True
                    print("\nYou are logged in as 'Administrator' with administrative rights.")
                else:
                    print(f"\nYou are logged in as '{usercheck}' with user rights only.")
                break
            else:
                raise KeyError("The username and/or password you entered are incorrect.")
        else:
            raise KeyError("The username and/or password you entered are incorrect.")
    except KeyError as error:
        login_trials -= 1
        print(f"\n%s\nYou have {str(login_trials)} chances left to login." % error)

        # Option to quit login if correct username and password cannot be remembered.
        try_login = input("\nWould you like to try to login again? Enter 'Yes'/'No':")
        if is_yes_no(try_login) == "no":  # If 'yes' the username loop continues or re-runs
            print("\nClosing task_manager.py\nGoodbye!")
            exit()  # Quit the whole registration process and go back to MAIN MENU
        else:
            continue

current_user = usercheck  # Store the username for other validations through the code
# Menu Options
while True:

    # Presenting the menu to the user and prompting for the next user's preferred step.
    if administrator:  # Admin user has a different menu due to their added functionality
        menu = input(
            '''\nSelect one of the following Options below:
            r  - Registering a user
            d  - Unregistering a user
            vs - View Statistics
            c  - Change Password 
            a  - Adding a task
            va - View all tasks
            vm - view my task
            e  - Exit
            :\n'''
        ).lower()
    else:  # Non-admin user has limited functionality
        menu = input(
            '''\nSelect one of the following Options below:
            c  - Change Password
            a  - Adding a task
            va - View all tasks
            vm - view my task
            e  - Exit
            :\n'''
        ).lower()

    task_count = 0  # Used to count the number of tasks
    task_box = []  # A list to store all tasks
    sentence_len_limit = 50  # Limit for character length of a long sentence to be turned into a paragraph

    # This Part is only for the ADMIN user to REGISTER New Users
    if menu == 'r':
        '''In this block you will write code to add a new user to the user.txt file
        - You can follow the following steps:
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the same.
            - If they are the same, add them to the user.txt file,
            - Otherwise you present a relevant message.'''

        # For a user who 'knows' that admin has options (r, d, s, etc.) the user must not have access to them
        if not administrator:  # Limit access of registering users to ADMIN only
            print("\nYou have made a wrong choice, Please Try again")
            continue

        # Username entry code (Only if the logged-in user is Administrator)
        try_user = ""
        try_pass = ""
        registration = True
        login_details = {}
        while registration:  # Registration process stops when False (termination of 'r' option)

            new_user = input("\nPlease enter a Username to register a new User:")

            # Error handling for username
            error_msg, user_name = is_valid_user(new_user, login_details)

            # Go back 1 step and try registering a new user without going all the way back to MAIN MENU
            if not user_name:
                print(f"\n{error_msg}")
                try_user = input("\nWould you like to try a new username? Enter 'Yes'/'No': ").casefold()

                if is_yes_no(try_user) == "no":  # If 'yes' the username loop continues or re-runs
                    registration = False  # Quit the whole registration process and go back to MAIN MENU
                    break
                else:
                    continue

            # Password entry code (Inside the username loop because a password is input only for a valid username)
            while True:
                new_pass = input("\nPlease enter a new Password:\n")
                pass_confirm = input("Please confirm the Password:\n")

                error_msg, pass_word = is_valid_pass(new_pass)

                # Error handling for passwords shorter than a certain length, no password or username, exclude space etc
                if not pass_word:
                    print(f"\n{error_msg}")
                    try_pass = input("\nWould you like to enter another password? 'Yes'/'No': ").casefold()

                    if is_yes_no(try_pass) == "yes":
                        continue
                    else:
                        registration = False  # Go to MAIN MENU
                        break

                # Validate password
                elif new_pass == pass_confirm:
                    with open("user.txt", "a", encoding='utf-8-sig') as user_details:
                        user_details.write(new_user + ", " + new_pass + "\n")
                        break
                # Password validation failed
                else:
                    print("\nYour confirmation password is incorrect: ")
                    try_pass = input("\nWould you like to enter another password? 'Yes'/'No': ").casefold()

                    if is_yes_no(try_pass) == "no":  # if 'yes' the password loop continues or re-runs
                        registration = False  # Go to MAIN MENU
                        break

            if try_pass == "no":  # Quit the whole registration process
                registration = False  # Go to MAIN MENU
                break

            # Register another user without going back to MAIN MENU
            print("\nA new Username and Password have been registered.")
            another_user = input("\nWould you like to register another user? Enter 'Yes'/'No': ").casefold()

            if is_yes_no(another_user) == "yes":
                continue  # Goes back to prompt administrator to register another username and password
            else:
                break
        if try_user or try_pass == "no":  # Quit the whole registration process and go to MAIN MENU
            continue

    # This Part is only for the ADMIN user to DE-REGISTER any of the Existing Users
    elif menu == 'd':
        '''In this block the admin user can de-register any user
        -Print all currently registered users
        -Choose a user to be de-registered
        -Store username and password in txt file for d-users
        -Store assigned task in txt file for d-tasks
        -Delete de-registered user from user txt file and delete tasks assigned to them on tasks txt file
        '''

        if not administrator:  # Limit access to De-Registering only to Administrator
            print("\nYou have made a wrong choice, Please Try again")
            continue

        login_details = get_userinfo()  # Retrieve Usernames and Passwords
        task_details = get_task_info()  # Retrieve All Tasks

        de_reg_usernames = []  # A list of de-registered usernames
        de_reg_tasks = []  # A list of tasks for all de-registered users
        user_count = len(login_details) - 1  # The number of possible users to be de-registered excluding Administrator

        user_options = {}  # A dictionary with numerical str cast keys and usernames as values
        for user_num_opt, username in enumerate(login_details, start=1):
            user_options.update({str(user_num_opt): username})

        # Selecting a username option to de-register and validating it
        while True:

            # Displaying all registered users for selection of de-registering
            print("\nDe-register any of the following users:\n\nOptions : Username")
            for user_num_opt in user_options.keys():
                print(user_num_opt + ". " + "\t" + user_options[user_num_opt])

            user_num = input("\nPlease Select One Option below or enter '0' to quit options:"
                             "\n" + ", ".join(list(user_options.keys())) + "\n")

            #  Validating username
            if user_num == "0":  # Option to quit De-registration before selecting a user to be de-registered
                print("\nDe-registration Cancelled!")
                break
            elif user_num not in user_options:
                print(f"\n\"{user_num}\" Option out of range")
                try_user_num = input("Would you like to enter another option? 'Yes'/'No': ").casefold()

                if is_yes_no(try_user_num) == "no":  # if 'yes' the de-registration loop continues or re-runs
                    # Go to MAIN MENU
                    break
                else:
                    print(f"\nChoose the correct Option from the below: \n{user_options.keys()}\n")
            elif user_options[user_num] == current_user and user_count == 0:
                print("\nERROR : Administrator is currently the only user and cannot be DE-REGISTERED!")
                break
            elif user_options[user_num] == current_user:  # The administrator is a MAIN user and must bot be REMOVED
                print("\nERROR : Administrator cannot be DE-REGISTERED!")
                continue
            elif user_count == 0:  # Quit de-registration if all users have been de-registered
                print("\nERROR : There are no more users to be de-registered!")
                break
            else:
                confirm_de_register = input(f"\nAre you sure you want to de-register {user_options[user_num]}?"
                                            f" Enter a 'Yes' or 'No' : ").casefold()

                if is_yes_no(confirm_de_register) == "yes":
                    print(f"\n{user_options[user_num]} will be de-registered from task_manager.py")

                    de_reg_usernames.append(list(login_details)[int(user_num) - 1])  # De-register a user
                    user_options.pop(user_num)  # Remove the de-registered username option

                    de_register_other = input("\nWould you like to de-register another User? Enter a 'Yes' or 'No' : ")

                    # Error handling for De_register_other variable
                    if is_yes_no(de_register_other) == "yes":
                        user_count -= 1
                        continue
                    else:
                        break
                else:
                    break

        # Save de-registered users information and associated tasks
        if len(de_reg_usernames) >= 1:

            with open("d_users.txt", "a+") as de_reg_users:
                for de_reg_user in de_reg_usernames:
                    # Capturing username and password of users to be de-registered
                    de_reg_users.write(de_reg_user + ", " + login_details[de_reg_user] + "\n")

                    # Removing username and password in user.txt file
                    login_details.pop(de_reg_user)

            with open("d_tasks.txt", "a+") as de_reg_tasks:
                for j, task_info in enumerate(task_details):
                    if task_info[0] == de_reg_user:
                        # Capturing task assigned to de-registered user
                        de_reg_tasks.write(", ".join(task_info) + "\n")

                        # Removing task assigned to the de-registered user
                        task_details.pop(j)

            # Rewrite the remaining registered usernames and passwords
            with open("user.txt", "w+", encoding='utf-8-sig') as user_details:
                for new_user in login_details:
                    user_details.write(new_user + ", " + login_details[new_user] + "\n")

            # Rewrite the remaining registered tasks
            with open("tasks.txt", "w+") as task_write_info:
                for task_info in task_details:
                    task_write_info.write(", ".join(task_info) + "\n")

    # This Part is only for the ADMIN user to View Statistical Data (Tasks and Users)
    elif menu == 'vs':

        if not administrator:  # Only Administrator has access to viewing statistics
            print("\nYou have made a wrong choice, Please Try again")
            continue

        print()
        print("- " * 50)
        print("The following is Statistical Data for all registered Users.\n")

        login_details = get_userinfo()
        task_details = get_task_info()

        num_users = len(login_details)  # Number os registered users
        num_tasks = len(task_details)  # Number of all tasks

        long_username = len(login_details.keys())
        add_space = tittle_space = 0
        if long_username > len("Username"):
            title_space = long_username - len("Username")
        else:
            add_space = len("Username") - long_username

        print("No." + " Username" + " " * (4 + tittle_space) + "Total Tasks")

        # Printing all users with their assigned number of tasks
        for i, username in enumerate(login_details):  # Get username
            task_count = 0
            for j, task_info in enumerate(task_details):  # Get number of tasks for a user
                if username == task_details[j][0]:
                    task_count += 1
            print(f"{i + 1} . {username}" + " " * (4 + long_username + add_space - len(username)) + f": {task_count}")

        print(f"\nThe total number of users is {num_users} with a total number of tasks at {num_tasks}.")
        print("- " * 50)

        # Prompts user to an option to continue using Task_Manager or Exit
        to_continue = input("\nWould you like to continue? Enter a 'Yes' or 'No' : ").casefold()
        if is_yes_no(to_continue) == "yes":
            continue
        else:
            print('\nClosing Task_Manager. \nGoodbye!!!')
            break

    # This Part is for ALL users who wish to CHANGE their Password
    elif menu == 'c':
        '''In this block, a user has a option to change their password
        '''
        # Get login details again in case the current user is ADMIN and had UPDATED users prior to this decision.
        # Otherwise, the updated users' information (usernames, passwords) will be lost.
        login_details = get_userinfo()
        change_in_password = True

        # Change the password of a currently logged-in user
        print("\nTo change your password, please follow the following:")
        while change_in_password:
            current_pass = input("\nPlease enter your Current password: ")

            # Avoid current user's password being changed by another user while current user is away (FRAUD)
            if not current_pass == login_details[current_user]:
                print("\nCurrent password is incorrect.")
                try_pass = input("\nWould you like to enter another password? 'Yes'/'No': ").casefold()

                if is_yes_no(try_pass) == "no":  # if 'yes' the changing password loop continues or re-runs
                    registration = False  # Go to MAIN MENU
                    break
                else:
                    continue

            # changing password after current user has confirmed current password
            while True:
                changed_pass = input("Please enter a New password: ")
                pass_confirm = input("Please confirm the New Password: ")

                error_msg, pass_word = is_valid_pass(changed_pass)

                # New password must not be the same as Current password (Avoid Redundancy)
                if current_pass == changed_pass:
                    print("\nPassword is unchanged.")
                    try_pass = input("\nWould you like to enter another password? 'Yes'/'No': ").casefold()

                    if is_yes_no(try_pass) == "no":  # if 'yes' the password loop continues or re-runs
                        change_in_password = False  # Go to MAIN MENU
                        break

                # Error handling for passwords shorter than a certain length, no password etc.
                elif not pass_word:
                    print(f"\n{error_msg}")
                    try_pass = input("\nWould you like to enter another password? 'Yes'/'No': ").casefold()

                    if is_yes_no(try_pass) == "no":  # if 'yes' the password loop continues or re-runs
                        change_in_password = False  # Go to MAIN MENU
                        break

                # Validating password
                elif changed_pass == pass_confirm:
                    login_details[current_user] = changed_pass

                    # Writing usernames and passwords to a text file
                    with open("user.txt", "w+", encoding='utf-8-sig') as user_details:
                        for username, password in login_details.items():
                            user_details.write(username + ", " + password + "\n")

                    print("\nPassword has been successfully changed!")
                    change_in_password = False
                    break

                # Password validation failed
                else:
                    print("\nYour confirmation password is incorrect: ")
                    try_pass = input("\nWould you like to enter another password? 'Yes'/'No': ").casefold()

                    if is_yes_no(try_pass) == "no":  # if 'yes' the change password loop continues or re-runs
                        change_in_password = False
                        break

        continue  # Go to MAIN MENU

    # This Part is for ALL users who wish to view tasks ASSIGNED to themselves and other users
    elif menu == 'a':
        '''In this block you will put code that will allow a user to add a new task to task.txt file
        - You can follow these steps:
            - Prompt a user for the following: 
                - A username of the person whom the task is assigned to,
                - A title of a task,
                - A description of the task and 
                - the due date of the task.
            - Then get the current date.
            - Add the data to the file task.txt and
            - You must remember to include the 'No' to indicate if the task is complete.'''

        login_details = get_userinfo()  # always get updated login details
        # Selecting a username option to assign a task and validating it
        while True:
            print("\nAssigning a task to Any of the Following users - "
                  "Options : Username")

            # Printing Username Options for Assigning a task
            user_num = 0
            user_options = {str(0): "Quit/Exit"}
            print(str(0) + ". " + "\t" + "Quit/Exit")

            for username in login_details.items():
                user_num += 1
                print(str(user_num) + ". " + "\t" + str(username[0]))
                user_options.update({str(user_num): username})

            user_num = input(f"\nPlease Select One of the Options below: \n{list(user_options.keys())}\n ")

            #  Validating username option
            if user_num == "0":
                print("\nTask assignment terminated.\n")
                break
            elif user_num not in user_options:
                print(f"\n\"{user_num}\" Option out of range")
                try_user_num = input("Would you like to enter another option? 'Yes'/'No': ").casefold()

                if is_yes_no(try_user_num) == "no":  # if 'yes' the assigning task loop continues or re-runs
                    print("\nTask assignment terminated.\n")  # Go to MAIN MENU
                    break
                else:
                    print(f"\nChoose the correct Option from the below: \n{user_options.keys()}\n")

            username = list(login_details)[int(user_num) - 1]
            task_title = input(f"Please enter a Task Title for username without commas (,): {username} \n: ")
            description = input(f"\nPlease enter a Task Description for username without commas (,): {username} \n: ")

            #  Getting Due Date from user and validating it.
            while True:
                # Error Handling for Date Input
                try:
                    inp_due_date = input("\nPlease enter a Due Date in the format: yyyy-mm-dd ")
                    year = int(inp_due_date[0:4])
                    month = int(inp_due_date[5:7])
                    day = int(inp_due_date[8:10])

                    today_date = datetime.date.today()
                    due_date = datetime.date(year, month, day)  # Year, month and day out of range errors are captured

                    if len(inp_due_date[0:4]) != 4 or len(inp_due_date[5:7]) != 2 or len(inp_due_date[8:10]) != 2:
                        raise ValueError("Date format is incorrect.")
                    elif year < 0 or month < 0 or day < 0:
                        raise ValueError("Date format is incorrect.")
                    elif len(inp_due_date) != 10:
                        raise ValueError("Date format is incorrect.")

                    if today_date > due_date:
                        raise ValueError("Due date has passed. Due date must be a future date.")
                except ValueError as error:
                    print("\n%s Please enter date in the correct format: YYYY-MM-DD" % error)
                else:
                    break

            task_complete = "No"

            task_box_row = [username,
                            task_title,
                            description,
                            today_date.strftime("%d %b %Y"),
                            due_date.strftime("%d %b %Y"),
                            task_complete,
                            ]

            task_box.append(task_box_row)
            print("\nTask has been successfully assigned.")

            other_task = input("\nWould you like to assign another task? Enter a 'Yes' or 'No' : ")

            # Error handling for other_task variable
            if is_yes_no(other_task) == "yes":
                task_count += 1
                continue
            else:
                break

        # Writing tasks into text file
        with open("tasks.txt", "a", encoding='utf-8-sig') as task_write_info:
            for row in task_box:
                task_line = ", ".join(row)
                task_write_info.write(task_line + "\n")

    # This Part is for ALL users who wish to view tasks for ALL users
    elif menu == 'va':
        '''In this block you will put code so that the program will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the L1T19 pdf file page 6
         You can do it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 in L1T19 pdf
            - It is much easier to read a file using a for loop.'''
        task_details = get_task_info()  # A 2-D List of lists
        login_details = get_userinfo()

        user_list = list(login_details.keys())  # Creating a list of usernames

        # Call displaying function to output information onto console
        display_format(task_details, user_list, sentence_len_limit)

        # Prompts user to an option to continue using Task_Manager or Exit
        to_continue = input("\nWould you like to continue? Enter a 'Yes' or 'No' : ").casefold()
        if is_yes_no(to_continue) == "yes":
            continue
        else:
            print('\nClosing Task_Manager. \nGoodbye!!!')
            break

    # This Part is for ALL users who wish to view ONLY their tasks
    elif menu == 'vm':
        '''In this block you will put code the that will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the L1T19 pdf
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the username you have
            read from the file.
            - If they are the same you print the task in the format of output 2 shown in L1T19 pdf '''
        task_details = get_task_info()
        login_details = get_userinfo()

        rgb_colour3 = "\033[38;2;0;255;255m"
        white_colour3 = "\033[0m"

        my_tasks = []  # A list containing only the current user's tasks
        my_login_details = []
        for task_info in task_details:
            if task_info[0] == current_user:
                my_tasks.append(task_info)

        if not my_tasks:
            print(rgb_colour3 + "You do not have any tasks assigned to you." + white_colour3)
        else:
            print("\nYou have the following tasks assigned to you.\n")

            list_current_user = [current_user]
            display_format(my_tasks, list_current_user, sentence_len_limit)

        # Prompts user with an option to continue using Task_Manager or Exit
        to_continue = input("\nWould you like to continue? Enter a 'Yes' or 'No' : ").casefold()
        if is_yes_no(to_continue) == "yes":
            continue
        else:
            print('\nClosing Task_Manager. \nGoodbye!!!')
            break

    elif menu == 'e':
        print('\nClosing Task_Manager. \nGoodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
