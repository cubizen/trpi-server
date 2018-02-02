import sys
from modules import command_work


def main(argv):
    wk = command_work.CommandWork(argv)

    cmd_list = [
        "help",
        "update",
        "start",
        "config",
    ]

    cmd = None
    try:
        cmd = argv[0]
    except:
        # Null command
        wk.help()
        exit(0)

    if cmd in cmd_list:
        eval("wk." + argv[0])()
        exit(0)
    else:
        wk.help()
        exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
