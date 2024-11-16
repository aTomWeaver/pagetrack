import pickle
from datetime import datetime, date
from sys import argv


def main():
    if len(argv) < 2:
        print("Insufficient args.")
        return
    args = argv[1:]
    if len(args) == 1:
        arg = args[0]
        fn, arg = parse_single_arg(arg)
        fn(arg)
    else:
        add_entry(args)


def timestamp() -> str:
    stamp = date.today().isoformat()
    return stamp


def parse_single_arg(arg):
    arg = arg.strip()
    if arg in CMDS:
        return (CMDS[arg], arg)
    elif is_date(arg):
        date = get_date_obj(arg).isoformat()
        return (print_record, date)
    elif arg.isdigit():
        return (add_entry, int(arg))
    else:
        return (print_err("unknown_cmd"), arg)


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
    print(f"Added record with {args} pages.")
    pass


def print_record(args):
    print(f"Printing record from {args}")
    pass


def print_average():
    pass


def dump_to_vimwiki(args):
    print("Dumping to vimwiki")
    pass


def zero_pad(string, total_length):
    while len(string) < total_length:
        string = "0" + string
    return string


def print_err(type_, cmd):
    if type_ == "unknown_cmd":
        print(f"{cmd} is not a recognized command.")


CMDS = {
        "average": print_average,
        "dump": dump_to_vimwiki,
        }

if __name__ == "__main__":
    main()
