# @author Venu Gopal Jilla


import socket
import threading
import random

host = '127.0.0.1'
port = 8888
server_port = (host, port)

details = {}
user_details = {}

def start_information(connection):
    message = 'Welcome to the Game Hangman.....!!!!!!!' + '\n'
    message += ' 1 . Sign Up ' + '\n'
    message += ' 2 . Sign In ' + '\n'
    connection.sendall(message.encode('utf-8'))
    login_register = connection.recv(1024).decode()
    if login_register == str(1):
        user_name = signup(connection)
        if user_name == 0:
            connection.close()
            return
    elif login_register == str(2):
        user_name = login(connection)
        if user_name == 0:
            connection.close()
            return
    else:
        wrong_choice = "Wrong choice"
        connection.sendall(wrong_choice.encode('utf-8'))
        connection.close()
        return
    hangman(connection, user_name)
    leaderboard()


def signup(connection):

    user_name = "Please enter your user name :"
    connection.sendall(user_name.encode('utf-8'))
    user_name = connection.recv(1024).decode()
    if user_name in user_details:
        alreadyPresent = "User already present \n Please Sign In"
        connection.sendall(alreadyPresent.encode('utf-8'))
        connection.close()
        return 0
    password = "Please enter your password :"
    connection.sendall(password.encode('utf-8'))
    password = connection.recv(1024).decode()
    details[user_name] = password
    user_details[user_name] = list()
    user_details[user_name].append(0)
    connection.sendall("valid".encode('utf-8'))
    return user_name


def login(connection):
    user_name = "Please enter your user name :"
    connection.sendall(user_name.encode('utf-8'))
    user_name = connection.recv(1024).decode()

    password = "Please enter your password :"
    connection.sendall(password.encode('utf-8'))
    password = connection.recv(1024).decode()

    if user_name in details and details[user_name] == password:
        valid_details = "valid" + "\n"
        connection.sendall(valid_details.encode('utf-8'))
    else:
        invalid_details = "invalid"
        connection.sendall(invalid_details.encode('utf-8'))
        connection.close()
        return 0
    return user_name

def server_run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_port)
    server_socket.listen(5)
    print("Welcome to the Game Hangman.....!!! ")

    while True:
        connection, addr = server_socket.accept()
        t1 = threading.Thread(target=start_information, args=(connection,))
        t1.start()


def secret_word():
    '''This Function is used to generate a secret word
       from a word list'''
    file = open("words.txt", 'r')
    inp1 = file.read()
    inp = list(inp1.split())
    sec_word = random.choice(inp)
    return sec_word


def guessed_word(letter, secret_wor, guess_wd,):
    ''' This function takes a letter as an input and gives a string as an output.
        It checks whether the letter is in the secretword or not.
        If yes it will append the letter at the specific position
        (where the letter is present in the secretword) into another list.'''
    res = []
    if letter in secret_wor:
        for i in range(len(secret_wor)):
            if secret_wor[i] == letter:
                res.append(i)
        for j in res:
            guess_wd[j] = letter
    guess_wd_st = "".join(guess_wd)
    return guess_wd_st


def is_word_guessed(guess_st, secret_wor):
    ''' This function two strings as input.
        The first string is User's guessed String and the other is the secretword.
        If the User's guessed string is same as Secretword ,
        it returns True else it returns False. '''
    if guess_st == secret_wor:
        return True
    return False


def get_available(gavailable, guessed_letter):
    ''' This Function takes a string and a character as an input
        and gives a string as an output.
        It removes each guessed letter from alphabets string
        and returns the remaining string.'''
    string_list = list(gavailable)
    if guessed_letter in gavailable:
        string_list.remove(guessed_letter)
    gt_available = "".join(string_list)
    return gt_available


def is_letter_guessed(guessed_letter, secret_wor):
    ''' This Function takes a character as an input
        and returns a Boolean value as an output.
        It checks whether the given letter is in secretword or not.
        If yes it returns True,else it returns False.'''
    if guessed_letter in secret_wor:
        return True
    return False


def is_alphabet(guessed_letter):
    '''This Function takes a character as an input
       and it checks whether the given character is
       an alphabet or not.If it is an alphabet, it
       returns True, else False'''
    if guessed_letter >= 'a' and guessed_letter <= 'z':
        return True
    return False


def hangman(connection, user_name):
    ''' hangman is a game where user should guess a word which is hidden
        in 8 chances.'''
    

    print("*************" , user_name, "***********************")

    secret_wor = secret_word()
    user_details[user_name].append(secret_wor)
    user_details[user_name].append(0)

    print(secret_wor)
    swl = len(secret_wor)

    intro = "Welcome to the Game Hangman..!!" + "\n"
    intro += "I am thinking of a word that is "+str(swl)+" letters long." + "\n"
    intro += "------------------------------------------------------------"

    connection.sendall(intro.encode("utf-8"))

    gavailable = "abcdefghijklmnopqrstuvwxyz"
    total_guesses = 6
    score = 0
    guesses = 6
    guess_wd = ["_ "]*swl
    guessed_letter = ''
    guess_let_wd = []
    guess_st = "".join(guess_wd)

    while guesses > 0:
       
        game_str = "You have " + str(guesses) + " guesses left" + "\n"
        game_str += "Available Letters : " + gavailable + "\n"
        game_str += "Please guess a letter: "

        connection.sendall(game_str.encode("utf-8"))

        guessed_letter = connection.recv(1024).decode().lower()

        if is_alphabet(guessed_letter):
            if len(guessed_letter) > 1:
                
                game_str1 = "Please enter a single letter" + "\n"
                game_str1 += "-------------------------------------------------------" + "\n"

                connection.sendall(game_str1.encode("utf-8"))

            elif guessed_letter in guess_let_wd:
                
                game_str2 = "Oops! You have already guessed the letter." + "\n"
                game_str2 += "-------------------------------------------------------" + "\n"

                connection.sendall(game_str2.encode("utf-8"))

                continue
            elif not is_letter_guessed(guessed_letter, secret_wor):
                guesses -= 1
                
                game_str3 = "Oops! The given letter is not in my word :" + guess_st + "\n"
                game_str3 += "-------------------------------------------------------" + "\n"

                connection.sendall(game_str3.encode("utf-8"))
            else:
                guess_st = guessed_word(guessed_letter, secret_wor, guess_wd)
                guess_let_wd.append(guessed_letter)
                
                game_str4 = "Good Guess : " + guess_st + "\n"
                game_str4 += "-------------------------------------------------------" + "\n"

                connection.sendall(game_str4.encode("utf-8"))

                if is_word_guessed(guess_st, secret_wor):
                    score = (10 * swl)  + guesses
                    score += user_details[user_name][-1]
                    user_details[user_name][-1] = score

                    game_str5 = "Congratulations, You won..!!!"
                    
                    connection.sendall(game_str5.encode("utf-8"))
                    break
            gavailable = get_available(gavailable, guessed_letter)
        else:
            
            game_str6 = "Please enter an alphabet" + "\n"
            game_str6 += "-------------------------------------------------------" + "\n"

            connection.sendall(game_str6.encode("utf-8"))
        guess_let_wd.append(guessed_letter)

    if not is_word_guessed(guess_st, secret_wor):

        game_str7 = "Oops! You lost the game" + "\n"
        game_str7 += secret_wor + "\n"
        connection.sendall(game_str7.encode("utf-8"))

def leaderboard():
    print()
    print("**************************************************************")
    print("*-*-*-*-leaderboard-*-*-*-*-*")
    
    leaderboard = sorted(user_details.items(),
                         key=lambda x: x[-1][-1], reverse=True)
    # print(user_details)
    # print(user_details.items())
    # print(leaderboard)
    for name, score in leaderboard:
        print("        ", name, score[-1])

    pass

server_run()
