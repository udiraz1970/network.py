# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chatlib import *
import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


import os


def rename_files_in_folder(folder_path):
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    rand_list = []

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Construct the full file path
        old_file_path = os.path.join(folder_path, filename)

        # Ensure it is a file (not a directory)
        if os.path.isfile(old_file_path):
            try:
                # Create the new file name by removing the first 3 characters
                #new_filename = filename[:len(filename)-4]
                #tmp = new_filename.split(' - ')
                #tmp[0] = tmp[0].strip()
                #tmp[1] = tmp[1].strip()
                #new_one = tmp[1] + ' - ' + tmp[0] + '.mp3'
                rnd = random.randint(1, 209)
                while rnd in rand_list:
                    rnd = random.randint(1, 209)
                rand_list.append(rnd)
                new_one = str(rnd) + " _ " + filename
            except BaseException as e:
                print(e)
            new_file_path = os.path.join(folder_path, new_one)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_one}'")


# Example usage
folder_path = '/path/to/your/folder'
rename_files_in_folder(folder_path)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename_files_in_folder('D:\\')


    print(join_data([1,'hello',2.6]))
    print(split_data('1#b#2.6', 2))
    print(build_message('LOGIN', 'a#b#c'))
    print(parse_message('LOGIN     |0005|a#b#c'))
    print(parse_message('LOGIN           |0005|a#b#c'))
    print(parse_message('LOGIN           |   5|a#b#c'))
    print(parse_message('LOGIN           |  05|a#b#c'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
