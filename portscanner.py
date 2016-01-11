import socket
import sys


def usage(error=''):
    '''
    Print an optional error message and usage, then exit unsuccessfully.
    '''
    if error != '':
        error += "\n\n"
    print('{}Usage: python portscanner.py [IP] [start] [end]'.format(error))
    print('Ports must be integers between 0-65535.')
    sys.exit(1)


def validate_int(argument):
    '''
    Takes one argument and returns it as an integer if possible.  Exits on
    failure.
    '''
    try:
        return int(argument)
    except ValueError:
        usage()


def validate_args(ip, start, end):
    start = validate_int(start)
    end = validate_int(end)
    if start > end:
        usage('Start port must be less than end port.')
    if start < 0 or end > 65535:
        usage()
    try:
        socket.inet_aton(ip)
    except socket.error:
        usage('Invalid IP.')
    return (ip, start, end)


def check_port(ip, port):
    '''
    Takes an IP and port and attempts to connect on IPv4, TCP.  Prints out the
    result of the attempted connection.
    '''
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)
    # try:
    try:
        sock.connect((ip, port))
        return "OPEN"
    except ConnectionRefusedError:  # NOQA
        return None


def portscanner(ip, start, end):
    '''
    Takes an IP and two port values.  Prints the port, service, and OPEN if the
    port responds.
    '''
    print('Scanning ports {}-{} on {}...\n'.format(start, end, ip))
    valid_args = validate_args(ip, start, end)
    ip = valid_args[0]
    start = valid_args[1]
    end = valid_args[2] + 1
    for i in range(start, end):
        try:
            nicename = socket.getservbyport(i)
        except OSError:
            nicename = ''
        status = check_port(ip, i)
        if status:
            print('Port {}, service {}: {}'.format(i, nicename, status))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()

    ip = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    portscanner(ip, start, end)
