import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


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

    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((SERVER_IP, SERVER_PORT))
    except BaseException as e:
        print('Error: No connection to server')
        exit(1)
    return my_socket


def error_and_exit(error_msg):
    # Implement code
    print(error_msg)
    exit(1)


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")

        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username + "#"+password)
        cmd, data = recv_message_and_parse(conn)
        if cmd != chatlib.PROTOCOL_SERVER["login_failed_msg"]:
            return
        else:
            print(data)


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    cmd, data = recv_message_and_parse(conn)


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def get_score(conn):
    cmd, data = build_send_recv_parse(conn, 'MY_SCORE', '')
    if cmd == 'ERROR':
        print('Error: ', data)
    else:
        print(f'Your score is {data}')


def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, 'HIGHSCORE', '')
    if cmd != 'ALL_SCORE':
        print('Error:', data)
    else:
        # Splitting the string by the backslash to get individual user data
        user_data = data.split('\\')

        # Creating a list of tuples from the split data
        user_tuples = [tuple(item.split(':')) for item in user_data]

        # Formatting the tuples into a clear table format
        table_string = "User   | Score\n"  # Header
        table_string += "-------|-------\n"  # Separator
        for user, score in user_tuples:
            table_string += f"{user:<7}| {score}\n"

        print(table_string)


def play_question(conn):
    cmd, data = build_send_recv_parse(conn, 'GET_QUESTION', '')
    if cmd != 'YOUR_QUESTION':
        print('No Questions anymore !!!')
    else:
        if data == 'Done':
            print('No more questions')
            return

        my_list = data.split('#')
        [print(item) for index, item in enumerate(my_list) if index != 0]
        cmd, data = build_send_recv_parse(conn, 'SEND_ANSWER', my_list[0]+'#'+input('Please choose 1, 2, 3 or 4: '))
        if cmd == 'WRONG_ANSWER':
            print(f'Wrong. The correct answer is {data}')
        elif cmd == 'CORRECT_ANSWER':
            print('Correct :)')
        else:
            print('Error')


def get_logged_users(conn):
    cmd, data = build_send_recv_parse(conn, 'LOGGED', '')
    if cmd != 'LOGGED_ANSWER':
        print('Error: ', data)
    else:
        my_list = data.split(',')
        [print(item) for item in my_list]


def main():
    conn = connect()
    login(conn)

    stop_play = False
    while not stop_play:
        user_option = input('Choose:\ns for Score\nh for highscore\np for Play\nu for Users\nq for quit\n')
        if user_option == 's':
            get_score(conn)
        elif user_option == 'h':
            get_highscore(conn)
        elif user_option == 'p':
            play_question(conn)
        elif user_option == 'u':
            get_logged_users(conn)
        elif user_option == 'q':
            stop_play = True
            continue
        else:
            print('Wrong option')


    logout(conn)


if __name__ == '__main__':
    main()

