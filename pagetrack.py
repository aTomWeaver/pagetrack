import pickle
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


def parse_single_arg(arg):
    pass


def add_entry(args):
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
    main()
