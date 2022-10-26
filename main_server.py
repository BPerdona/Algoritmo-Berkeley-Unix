from relogio_server import Server


def main(args):
    Server(int(args[0]))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])