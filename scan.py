import os
import sys
import re
import magic

# blacklist = ["keyword1", "keyword2", "keyword3"]

exclude_folders = ['.git']


def is_text_file(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type.startswith('text')

def scan_file(file_path, blacklist):
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, 1):
            for keyword in blacklist:
                pattern = rf'\b{re.escape(keyword)}\b'
                if re.search(pattern, line):
                    print(f'File: {file_path}, Line: {line_number}, Keyword: {keyword}')

def scan_directory(directory, blacklist):
    for root, dirs, files in os.walk(directory):
        for exclude in exclude_folders:
            if exclude in dirs:
                dirs.remove(exclude)

        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and is_text_file(file_path):
                scan_file(file_path, blacklist)


def read_blacklist():
    blacklist = []
    with open('blacklist.txt', 'r') as file:
        for line in file:
            word = line.strip()
            blacklist.append(word)
    return blacklist


if __name__ == "__main__":
    directory = os.getcwd()
    if len(sys.argv) == 2:
        directory = sys.argv[1]

    blacklist = read_blacklist()
    scan_directory(directory, blacklist)
