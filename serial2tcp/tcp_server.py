import logging
import asyncore
import socket

__author__ = [
    'parijatmishra <wordpress.com/author/parijatmishra/>',
    'Dmitry Orlov <me@mosquito.su>'
]

log = logging.getLogger('serial2tcp.Server')


class SocketHandler(asyncore.dispatcher):
    SIZE = 1024
    def __init__(self, sock, client_address, server):
        self.server = server
        self.client_address = client_address
        self.buffer = ""

        # We dont have anything to write, to start with
        self.is_writable = False

        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, sock)
        log.debug("Handled created. Waiting for loop")

    def readable(self):
        # We are always happy to read
        return True

    def writable(self):
        # But we might not have
        # anything to send all the time
        return self.is_writable

    def handle_read(self):
        host, port = self.client_address

        data = self.recv(1024)
        l = len(data)
        log.debug("[{0}:{1}] recieved {2} bytes".format(host, port, l))
        if l:
            self.buffer += data
            self.is_writable = True  # sth to send back now
        else:
            log.debug("[{0}:{1}] receiving has been finished.".format(host, port))

    def handle_write(self):
        def cb(data):
            sent = self.send(data)
            self.buffer = self.buffer[sent:]

        if self.buffer:
            self.server.SERIAL.write_async(self.buffer, callback=cb)
        else:
            log.error("Nothing to send")
        if len(self.buffer) == 0:
            self.is_writable = False

    def handle_close(self):
        log.debug("[{0}:{1}] Close connection".format(*self.client_address))
        self.close()


class Server(asyncore.dispatcher):
    SERIAL = None
    def __init__(self, host='0.0.0.0', port=9100, handlerClass=SocketHandler,
                 reuse=True, request_queue_size=5, use_acl=False):
        assert isinstance(port, int)

        self.host = host
        self.port = port
        self.handlerClass = handlerClass
        self.request_queue_size = request_queue_size

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        if reuse:
            self.set_reuse_addr()

        self.server_bind()
        self.server_activate()

        self.use_acl = use_acl
        self.ACL = set([])

    def server_bind(self):
        self.bind((self.host, self.port))

    def server_activate(self):
        self.listen(self.request_queue_size)
        log.info("Listening {0}:{1} with backlog={2}".format(self.host, self.port, self.request_queue_size))

    def fileno(self):
        return self.socket.fileno()

    def serve_forever(self):
        asyncore.loop()

    # TODO: try to implement handle_request()
    # Internal use
    def handle_accept(self):
        conn_sock, client_address = self.accept()
        if self.verify_request(conn_sock, client_address):
            self.process_request(conn_sock, client_address)

    def verify_request(self, conn_sock, client_address):
        if self.use_acl:
            return client_address[0] in self.ACL
        else:
            return True

    def process_request(self, conn_sock, client_address):
        addr, port = client_address
        log.info("Accept connection from {0}:{1}".format(addr, port))
        self.handlerClass(conn_sock, client_address, self)

    def handle_close(self):
        self.close()

