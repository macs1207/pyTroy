
import sys


def main():
    try:
        file_name = sys.argv[1]
        name_list = []

        with open(file_name, "r") as f:
            name_list = f.readlines()

        name_list.reverse()

        with open(file_name, "w") as f:
            for name in name_list:
                f.write(name)
    except IndexError:
        print("Usage: python ch03-file.py {file_name}")


if __name__ == "__main__":
    main()
