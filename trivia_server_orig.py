##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import select
import random

# GLOBALS
users = {}
questions = {}
questions_asked = []
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
client_sockets = []
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
MAX_MSG_LENGTH = 1024


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    msg = chatlib.build_message(code, data)
    conn.send(msg.encode())
    print(f'[SERVER]' + msg)


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..

    global client_sockets
    full_msg = conn.recv(1024).decode()
    print(f'[CLIENT]' + full_msg)
    cmd, data = chatlib.parse_message(full_msg)
    if cmd is None or data is None:
        client_sockets.remove(conn)
        conn.close()
    return cmd, data


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    global questions
    questions = {
        1: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        2: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    global users
    users = {
        "udi": {"password": "gal", "score": 10, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", SERVER_PORT))
    server_socket.listen()
    print("Server is up and running")
    return server_socket


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    # Implement code ...
    build_and_send_message(conn, 'ERROR', error_msg)


##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    user_score = users[username]['score']
    build_and_send_message(conn, 'YOUR_SCORE', str(user_score))


def handle_highscore_message(conn):
    user_scores = [(username, user_data["score"]) for username, user_data in users.items()]
    user_scores_sorted_desc = sorted(user_scores, key=lambda x: x[1], reverse=True)
    result_string = '\\'.join([f"{username}:{score}" for username, score in user_scores_sorted_desc])
    build_and_send_message(conn, 'ALL_SCORE', result_string)


def handle_logged_message(conn):
    usernames = [username[0] for username in users.items()]
    result_string = ','.join(usernames)
    build_and_send_message(conn, 'LOGGED_ANSWER', result_string)


def handle_logout_message(conn):
    global logged_users
    global client_sockets

    print(f"Connection closed")
    client_sockets.remove(conn)
    del logged_users[conn]
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users

    user_pass_list = data.split('#')
    if len(user_pass_list) != 2:
        send_error(conn, f': The format of the login message is not correct - {data}')
        return

    if user_pass_list[0] not in users:
        send_error(conn, f': User {user_pass_list[0]} doesn\'t exist')
        return

    if user_pass_list[1] != users[user_pass_list[0]]['password']:
        send_error(conn, ': Incorrect password')
        return

    logged_users[conn] = user_pass_list[0]
    build_and_send_message(conn, 'LOGIN_OK', '')


def create_random_question() -> str:
    if len(questions_asked) == len(questions):
        return 'Done'

    random_integer = random.choice([i for i in range(1, len(questions) + 1) if i not in questions_asked])
    questions_asked.append(random_integer)
    return f'{random_integer}#{questions[random_integer]["question"]}#{"#".join(questions[random_integer]["answers"])}'


def handle_question_message(conn):
    build_and_send_message(conn, 'YOUR_QUESTION', create_random_question())


def handle_answer_message(conn, data):
    ans_list = data.split('#')
    if len(ans_list) != 2:
        send_error(conn, ': Wrong answer format !')

    correct_ans = str(questions[int(ans_list[0])]["correct"])
    if ans_list[1] == correct_ans:
        users[logged_users[conn]]['score'] += 5
        build_and_send_message(conn, 'CORRECT_ANSWER', '')
    else:
        build_and_send_message(conn, 'WRONG_ANSWER', correct_ans)


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users

    if conn not in logged_users:
        if cmd == 'LOGIN':
            handle_login_message(conn, data)
        elif cmd is not None:
            send_error(conn, ': You are not logged in !!!')
        return

    if cmd == 'LOGOUT':
        handle_logout_message(conn)
    elif cmd == 'MY_SCORE':
        handle_getscore_message(conn, logged_users[conn])
    elif cmd == 'HIGHSCORE':
        handle_highscore_message(conn)
    elif cmd == 'LOGGED':
        handle_logged_message(conn)
    elif cmd == 'GET_QUESTION':
        handle_question_message(conn)
    elif cmd == 'SEND_ANSWER':
        handle_answer_message(conn, data)
    else:
        send_error(conn, f': unknown command - {cmd}')


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")

    load_user_database()
    load_questions()
    server_socket = setup_socket()

    global client_sockets
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
            else:
                print("New data from client")
                data = ''
                cmd = ''
                try:
                    cmd, data = recv_message_and_parse(current_socket)
                except ConnectionResetError as e:
                    print(e)
                    current_socket.close()
                except BaseException as baseEx:
                    print(baseEx)
                    current_socket.close()
                if cmd == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    print((cmd, data))
                    handle_client_message(current_socket, cmd, data)


if __name__ == '__main__':
    main()
