from relogio_client import Client


def main(args):
    Client(int(args[0]))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
