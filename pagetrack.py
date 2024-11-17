import os
import csv
import pickle
import statistics
from sys import argv
from operator import itemgetter
from datetime import date, timedelta


LOGFILE = os.path.realpath("data/logfile.pickle")
CACHE = os.path.realpath("data/cache.pickle")
CSV_OUT = os.path.realpath("out")
VIMWIKI_LOC = os.path.realpath("out/vimwiki")


APPDATA_MOCK = {
        "last_read": "Capital",
        "last_action": {
            "command": "",
            "title": "",
            "pagenum": "",
            "date": ""
            }
        }



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
    # print(f"exec dict is {exec_dict}\n\n")
    if exec_dict["command"] is not None:
        CMDS[exec_dict["command"]](exec_dict["command_args"])
    else:
        print(exec_dict)
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
                d["title"] = arg.lower()
    return d


def parse_arg_type(arg) -> tuple:
    arg = arg.strip()
    if arg in CMDS:
        return ("command", arg)
    elif is_date(arg):
        return ("date", get_iso_date(arg))
    elif arg.isdigit():
        return ("pagenum", int(arg))
    elif arg[0] == "-":
        try:
            # negative value interpreted as x days ago
            arg = int(arg)
            return ("date", get_iso_date(arg))
        except Exception:
            return ("other", arg)
    else:
        return ("other", arg)


def is_date(string):
    if "-" not in string or not string[0].isdigit():
        return False
    split_arg = string.split("-")
    for arg_ in split_arg:
        if not arg_.isdigit() and arg_ != "":
            # if arg_ is "", pass along to fail on get_iso_date
            return False
    return True


def get_iso_date(date_arg):
    if type(date_arg) is int:
        date_string = date.today() - timedelta(abs(date_arg))
        return date_string.isoformat()
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
        title = "unknown title"
    if date is None:
        date = timestamp()
    add_entry(date, pagenum, title)


def add_entry(date, pagenum, title):
    print("Adding")
    log = read_log()
    if date not in log:
        log[date] = {}
    if title not in log[date]:
        log[date][title] = pagenum
    else:
        log[date][title] += pagenum
    write_log(log)
    print(read_log())


def print_record(date_):
    log = read_log()
    if date_ not in log:
        print(f"No records from {date_}.")
        return
    max_title_len = get_max_length(log[date_])
    total_pages = 0
    for title, pages in log[date_].items():
        spacing = (max_title_len - len(title) + 2) * " "
        print(f"{title}{spacing}{pages}")
        total_pages += pages
    divider = "-" * max_title_len
    spacing = (max_title_len - len("total:") + 2) * " "
    print(divider)
    print(f"\ntotal:{spacing}{total_pages}")


def get_max_length(day_entry):
    titles = set()
    for title in day_entry.keys():
        titles.add(title)
    return len(max(titles, key=len))


def dump_to_vimwiki(exec_dict):
    export_csv([VIMWIKI_LOC])


def export_csv(args=[]):
    log = read_log()
    header = get_header_row(log)
    final_csv = [header]
    for date_, day_log in log.items():
        row = [date_]
        for title in header:
            if title == "date":
                continue
            elif title in day_log:
                row.append(day_log[title])
            else:
                row.append("")
        final_csv.append(row)
    path = args[0] if args else None
    write_csv(final_csv, path)


def get_index_dict(header):
    index_dict = {}
    for idx, title in enumerate(header):
        if idx == 0:
            continue
        else:
            index_dict[title] = idx
    return index_dict


def get_header_row(log):
    titles = ["date"]
    for day in log.values():
        for title in day.keys():
            if title in titles and title != "date":
                continue
            titles.append(title)
    return titles


def default_cache():
    default = {
        "last_read": "unknown title",
        "last_action": {
            "command": None,
            "title": None,
            "pagenum": None,
            "date": None
            }
        }
    return default


def zero_pad(string, total_length):
    while len(string) < total_length:
        string = "0" + string
    return string


def print_err(type_, cmd):
    if type_ == "unknown_cmd":
        print(f"{cmd} is not a recognized command.")


def print_average(exec_dict):
    log = read_log()
    all_pages = []
    for _, day_log in log.items():
        pages_on_day = 0
        for _, pages in day_log.items():
            pages_on_day += pages
        all_pages.append(pages_on_day)
    avg = int(statistics.fmean(all_pages))
    print(f"You read an average of {avg} pages a day.")


################
# COMMANDS MAP #
################


CMDS = {
        "average": print_average,
        "dump": dump_to_vimwiki,
        "export-csv": export_csv
        }

###################
# READING/WRITING #
###################


def read_pickle(path, create_if_not_exist=True, default_data={}):
    if not os.path.exists(path):
        print(f"\"{path}\" does not exist.")
        if not create_if_not_exist:
            return
        print(f"Writing new \"{path}\".")
        write_pickle(path, {})
    with open(path, "rb") as file:
        unpickled = pickle.load(file)
    return unpickled


def write_pickle(path, data):
    '''Write `data` to pickle file at `path`.'''
    with open(path, "wb") as file:
        pickle.dump(data, file)


def read_log():
    '''Convenience wrapper for read_pickle(log).'''
    path = os.path.realpath(LOGFILE)
    return read_pickle(path)


def read_cache():
    '''Convenience wrapper for read_pickle(cache).'''
    path = os.path.realpath(CACHE)
    default = default_cache()
    return read_pickle(path, default_data=default)


def write_log(data):
    '''Convenience wrapper for write_pickle(log).'''
    path = os.path.realpath(LOGFILE)
    write_pickle(path)


def write_cache(data):
    '''Convenience wrapper for write_pickle(cache).'''
    path = os.path.realpath(CACHE)
    write_pickle(path)


def write_csv(rows, path=None):
    filename = f"{timestamp()}_reading_stats.csv"
    if path is None:
        path = os.path.join(CSV_OUT, filename)
    else:
        path = os.path.join(path, filename)
    with open(path, "w+") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


if __name__ == "__main__":
    main()
