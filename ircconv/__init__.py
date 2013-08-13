# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from ircconv.net import ProxyServer


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('listen', help='listen address and port (host:port)')
    parser.add_argument('upstream', help='upstream server (host:port)')
    args = parser.parse_args()

    for name in ('listen', 'upstream'):
        value = getattr(args, name)
        parts = value.split(':')
        setattr(args, name, (parts[0], int(parts[1])))

    return args


def main():
    args = parse_args()
    server = ProxyServer(args.listen, args.upstream)
    server.daemon = True
    try:
        server.start()
        while True:
            server.join(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
