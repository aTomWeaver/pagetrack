import os
from operator import itemgetter
import pickle
from datetime import datetime, date
from sys import argv


LOGFILE = "data/logfile.pickle"


master_list = []


def main():
    if len(argv) < 2:
        print("Insufficient args.")
        return
    args = argv[1:]
    argtype_and_arg_list = []
    for arg in args:
        type_, arg = parse_arg_type(arg)
        argtype_and_arg_list.append((type_, arg))
    exec_dict = get_exec_dict(argtype_and_arg_list)
    print(f"exec dict is {exec_dict}\n\n")
    if exec_dict["command"] is not None:
        CMDS[exec_dict["command"]](exec_dict["command_args"])
    else:
        execute(exec_dict)


def timestamp() -> str:
    stamp = date.today().isoformat()
    return stamp


def get_exec_dict(argtype_and_arg_list):
    d = {
            "command": None,
            "date": None,
            "pagenum": None,
            "title": None,
            "command_args": []
            }
    for arg in argtype_and_arg_list:
        type_, arg = arg
        if type_ == "command":
            d["command"] = arg
        elif type_ == "date":
            d["date"] = arg
        elif type_ == "pagenum":
            d["pagenum"] = arg
        elif type_ == "other":
            if d["command"] is not None:
                # if there is a command, treat strings as args
                d["command_args"].append(arg)
            else:
                # if no command, the string is the title
                d["title"] = arg
    return d


def parse_arg_type(arg) -> tuple:
    arg = arg.strip()
    if arg in CMDS:
        return ("command", arg)
    elif is_date(arg):
        return ("date", get_iso_date(arg))
    elif arg.isdigit():
        return ("pagenum", int(arg))
    else:
        return ("other", arg)


def is_date(string):
    if "-" not in string:
        return False
    split_arg = string.split("-")
    for arg_ in split_arg:
        if not arg_.isdigit() and arg_ != "":
            # if arg_ is "", pass along to faile on get_iso_date
            return False
    return True


def get_iso_date(date_arg):
    arg_list = date_arg.strip().split("-")
    date_list = []
    if len(arg_list) < 3:
        date_list.append(str(date.today().year))
    for num in arg_list:
        date_list.append(zero_pad(num, 2))
    date_string = "-".join(date_list)
    try:
        date_string = date.fromisoformat(date_string).isoformat()
    except ValueError:
        print("Date given is invalid.")
        exit(1)
    return date_string


def execute(exec_dict):
    command, date, pagenum, title = itemgetter(
            "command",
            "date",
            "pagenum",
            "title",
            )(exec_dict)
    if command is not None:
        CMDS[command](exec_dict)
        return
    if pagenum is None:
        if date is not None:
            print_record(date)
            return
        else:
            print("No pages given.")
            exit()
    if title is None:
        # TODO: fetch last title from appdata
        title = "Unknown Title"
    if date is None:
        date = timestamp()
    add_entry(date, pagenum, title)


def add_entry(date, pagenum, title):
    master_list.append((date, title, pagenum))
    print(master_list)


def print_record(args):
    print(f"Printing record from {args}")
    pass


def print_average(exec_dict):
    pass


def dump_to_vimwiki(exec_dict):
    print("Dumping to vimwiki")
    pass


def zero_pad(string, total_length):
    while len(string) < total_length:
        string = "0" + string
    return string


def print_err(type_, cmd):
    if type_ == "unknown_cmd":
        print(f"{cmd} is not a recognized command.")


def load_pickle():
    if not os.path.exists(os.path.realpath(LOGFILE)):
        print(f"No log file at \"{os.path.realpath(LOGFILE)}\".")
        print(f"Creating log file at \"{os.path.realpath(LOGFILE)}\".")
        write_pickle({})
    with open(LOGFILE, "rb") as file:
        log = pickle.load(file)
    return log


def write_pickle(data):
    with open(LOGFILE, "wb") as file:
        pickle.dump(data, file)


CMDS = {
        "average": print_average,
        "dump": dump_to_vimwiki,
        }

if __name__ == "__main__":
    print(load_pickle())
    # main()
