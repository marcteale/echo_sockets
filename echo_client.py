import socket
import sys


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address),
          file=log_buffer)  # NOQA
    # TODO: connect your socket to the server here.
    streams = [info
               for info in socket.getaddrinfo(*server_address)
               if info[1] == socket.SOCK_STREAM and info[0] == socket.AF_INET]
    info = streams[0]
    sock.connect((info[4]))

    # you can use this as a place to accumulate the entire message echoed back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        buffsize = 16

        print('sending "{0}"'.format(msg), file=log_buffer)
        # TODO: send your message to the server here.
        msg = msg.encode('utf8')
        sock.sendall(msg)

        # TODO: the server should be sending you back your message as a series
        #       of 16-byte chunks. Accumulate the chunks you get to build the
        #       entire reply from the server. Make sure that you have received
        #       the entire message and then you can break the loop.
        #
        #       Log each chunk you receive.  Use the print statement below to
        #       do it. This will help in debugging problems
        while True:
            chunk = sock.recv(buffsize)
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            received_message += chunk.decode('utf8')
            if len(chunk) < buffsize:
                break
    finally:
        # TODO: after you break out of the loop receiving echoed chunks from
        #       the server you will want to close your client socket.
        print('closing socket', file=log_buffer)
        sock.close()

        # TODO: when all is said and done, you should return the reply you got
        # from the server as the value of this function.
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
