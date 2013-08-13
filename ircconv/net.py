# -*- coding: utf-8 -*-

import socket
from threading import Thread

from ircconv.codecs import jis_to_utf8


class ProxyServer(Thread):
    def __init__(self, listen, upstream):
        super(ProxyServer, self).__init__()
        self.listen_addr = listen
        self.upstream_addr = upstream
        self.socket = None

    def _listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.listen_addr)
        self.socket.listen(5)

    def _make_upstream(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.upstream_addr)
        return sock

    def run(self):
        self._listen()
        # The server cannot stop because accept is blocking operation
        while True:
            (client, address) = self.socket.accept()
            upstream = self._make_upstream()
            ProxyConnection(client, upstream)


class ProxyConnection(object):
    def __init__(self, client, upstream):
        self.upstream = Connection(client, upstream, utf8_to_jis)
        self.downstream = Connection(upstream, client, jis_to_utf8)
        self.upstream.daemon = True
        self.downstream.daemon = True
        self.upstream.start()
        self.downstream.start()

    def stop(self):
        self.upstream.stop()
        self.downstream.stop()

    def join(self):
        self.upstream.join()
        self.downstream.join()


class Connection(Thread):
    def __init__(self, inbound, outbound, hook):
        super(Connection, self).__init__()
        self.canceled = False
        self.inbound = inbound
        self.outbound = outbound
        self.hook = hook
        self.rfile = inbound.makefile('rb')

    def stop(self):
        self.canceled = True

    def run(self):
        while not self.canceled:
            line = self.rfile.readline()
            if not line:
                break

            self.outbound.send(self.hook(line))


def utf8_to_jis(text):
    return text.decode('utf-8').encode('iso-2022-jp')
