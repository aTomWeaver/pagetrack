import pickle
from datetime import datetime, date
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


def timestamp() -> str:
    stamp = date.today().isoformat()
    return stamp


def parse_single_arg(arg):
    if is_date(arg):
        date = get_date_obj(arg).isoformat()
        print(date)
    pass


def is_date(string):
    if "-" not in string:
        return False
    split_arg = string.split("-")
    for arg_ in split_arg:
        if not arg_.isdigit():
            return False
    return True


def get_date_obj(date_arg):
    arg_list = date_arg.strip().split("-")
    date_list = []
    if len(arg_list) < 3:
        date_list.append(str(date.today().year))
    for num in arg_list:
        date_list.append(zero_pad(num, 2))
    date_string = "-".join(date_list)
    return date.fromisoformat(date_string)



def add_entry(args):
    pass


def print_record(args):
    pass


def print_average(args):
    pass


def dump_to_vimwiki(args):
    pass


def zero_pad(string, total_length):
    while len(string) < total_length:
        string = "0" + string
    return string


CMDS = {
        "average": print_average,
        "dump": dump_to_vimwiki,
        }

if __name__ == "__main__":
    main()
