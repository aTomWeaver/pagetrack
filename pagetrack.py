import pickle
from datetime import datetime
from sys import argv


def main():
    if len(argv) < 2:
        print("Insufficient args.")
        return
    args = argv[1:]
    if len(args) == 1:
        parse_single_arg(args[0])
    else:
        add_entry(args)


def timestamp():
    return datetime.strftime(datetime.now(), "%Y-%M-%d")

def parse_single_arg(arg):
    if is_date(arg):
        print_record(date)
    pass


def is_date(string):
    if "-" not in string:
        return False
    split_arg = string.split("-")
    for arg_ in split_arg:
        if not arg_.isdigit():
            return False
    return True


def add_entry(args):
    pass


def print_record(args):
    pass


def print_average(args):
    pass


def dump_to_vimwiki(args):
    pass


CMDS = {
        "average": print_average,
        "dump": dump_to_vimwiki,
        }

if __name__ == "__main__":
    print(parse_single_arg("2024-11-15"))
    # main()
