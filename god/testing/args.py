import sys
import os


def modify_osm(file_path: str, match_path: str, replace_path: str):
    # file_path = 'god/testing/txt.c'
    if len(file_path) == 0 or len(match_path) == 0 or len(replace_path) == 0:
        print('args invalid!')
        sys.exit(1)

    match_content = ""
    replace_content = ""

    with open(match_path, 'r') as match_file:
        match_content = match_file.read()

    with open(replace_path, 'r') as replace_file:
        replace_content = replace_file.read()

    with open(file_path, 'r+') as modify_file:
        modify_content = modify_file.read()
        if match_content in modify_content:
            index = modify_content.find(match_content)
            new_content = modify_content[:index] + replace_content + \
                modify_content[len(match_content)+index:]
            modify_file.seek(0)
            modify_file.write(new_content)
        else:
            print('========find match_content fail===========')
            exit(1)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3:
        print("args invalid!")
        exit(1)

    modify_osm(args[0], args[1], args[2])
