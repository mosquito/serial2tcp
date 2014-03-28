serial2tcp
==========

Instalation
-----------
You can install from pip:

    # pip install serial2tcp

or manual:

    git clone git://github.com/mosquito/serial2tcp.git
    cd serial2tcp
    python setup.py install

Redirect USB-Serial
-------------------
For redirect /dev/ttyUSB0 with baudrate 9600 bps and 192.168.2.1 can connect to that:

    # serial2tcp -p /dev/ttyUSB0 -b 9600 -l 0.0.0.0 --allow-list='192.168.2.1'

Help
----
    Usage: serial2tcp [options]

    Simple Serial to Network (TCP/IP) redirector.

    WARNING: You have to allow connections only from the addresses in the
    "--allow-list" option. e.g. --allow-list='10.0.0.1, 172.16.0.1, 192.168.0.1'
    NOTICE: This service supports only one tcp connection per instance.

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -p SERIAL, --port=SERIAL
                            Serial port, a number, defualt = '/dev/tty0'
      -b BAUDRATE, --baud=BAUDRATE
                            Baudrate, default 115200
      -r, --rtscts          Enable RTS/CTS flow control (default off)
      -x, --xonxoff         Enable software flow control (default off)
      -P PORT, --localport=PORT
                            TCP/IP port on which to run the server (default 9100)
      -l LISTEN, --listen=LISTEN
                            Listen address on which to run the server (default
                            '127.0.0.1')
      --access-list=ACL     List of IP addresses e.g '127.0.0.1, 192.168.0.2'

Based on: http://www.cs.earlham.edu/~charliep/ecoi/serial/pyserial-2.2/examples/tcp_serial_redirect.py
